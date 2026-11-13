"""逐轮运行注释副本中的 KNN 算法，保存真实耗时；只依赖 Python 标准库。

运行：python3 run_feature_experiments.py
计时范围：fit 和 predict 分开，排除读文件、截取特征、指标计算和文件写入。
教师的搜索算法不变；此脚本对评估的零分母额外记录错误并按 0 报告，避免实验中断。
"""

import argparse
import csv
import gc
import hashlib
import json
import math
import platform
import statistics
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import KNNmodel_train_predict_annotated as lesson


ROOT = Path(__file__).resolve().parent
TZ = ZoneInfo("Asia/Shanghai")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_evaluate(y_true, y_pred):
    """优先使用教师评估函数；保留零除异常信息，并明确零分母约定。"""
    try:
        return lesson.evaluate_binary(y_true, y_pred), ""
    except ZeroDivisionError as error:
        tp = sum(t == 1 and p == 1 for t, p in zip(y_true, y_pred))
        tn = sum(t == 0 and p == 0 for t, p in zip(y_true, y_pred))
        fp = sum(t == 0 and p == 1 for t, p in zip(y_true, y_pred))
        fn = sum(t == 1 and p == 0 for t, p in zip(y_true, y_pred))
        return {
            "tn": tn, "fp": fp, "fn": fn, "tp": tp,
            "accuracy": (tp + tn) / len(y_true),
            "precision": tp / (tp + fp) if tp + fp else 0.0,
            "recall": tp / (tp + fn) if tp + fn else 0.0,
            "f1": 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0,
        }, f"{type(error).__name__}: {error}; zero_division=0"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--out", type=Path, default=ROOT / "实验结果_20261105")
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats 必须大于 0")
    # 不覆盖旧记录；重跑请用 --out 指定另一个目录。
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    metadata = {
        "status": "running",
        "started_at": datetime.now(TZ).isoformat(),
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "timer": "time.perf_counter; fit/predict only",
        "repeats": args.repeats,
        "feature_counts": list(lesson.FEATURE_COUNTS),
        "k": lesson.K,
        "sampling": "first rows in each teacher CSV, no shuffle or scaling",
        "order": "reverse feature order on even passes; alternate model order",
        "warmup": "no separate warm-up; all measured passes retained",
        "metric_policy": "original evaluator; on ZeroDivisionError record error and use zero_division=0",
        "data_source": "/Users/zhangjiawei/Library/CloudStorage/OneDrive-个人/资料/数据结构/2026-10-15",
        "files_sha256": {},
    }
    if sys.platform == "darwin":
        metadata["cpu"] = subprocess.check_output(
            ["sysctl", "-n", "machdep.cpu.brand_string"], text=True
        ).strip()
    for name in [lesson.TRAIN_FILE, lesson.TEST_FILE,
                 "KNNmodel_train_predict_need_comment.py", "KNNmodel_train_predict_type2.py",
                 "KNNmodel_train_predict_annotated.py", Path(__file__).name]:
        metadata["files_sha256"][name] = sha256(ROOT / name)

    train_x, train_y, names = lesson.load_dataset(ROOT / lesson.TRAIN_FILE)
    test_x, test_y, test_names = lesson.load_dataset(ROOT / lesson.TEST_FILE)
    metadata["full_rows"] = {"train": len(train_x), "test": len(test_x)}
    assert names == test_names, "训练集、测试集的特征顺序不一致"
    assert len(train_x) >= lesson.TRAIN_SAMPLE_COUNT
    assert len(test_x) >= lesson.TEST_SAMPLE_COUNT
    train_x, train_y = train_x[:lesson.TRAIN_SAMPLE_COUNT], train_y[:lesson.TRAIN_SAMPLE_COUNT]
    test_x, test_y = test_x[:lesson.TEST_SAMPLE_COUNT], test_y[:lesson.TEST_SAMPLE_COUNT]
    assert all(1 <= n <= len(names) for n in lesson.FEATURE_COUNTS)
    assert all(len(row) == len(names) and all(math.isfinite(v) for v in row)
               for row in train_x + test_x)
    assert set(train_y + test_y) <= {0, 1}
    metadata.update({"train_samples": len(train_x), "test_samples": len(test_x),
                     "feature_names": names,
                     "train_labels": dict(Counter(train_y)),
                     "test_labels": dict(Counter(test_y))})
    meta_path = args.out / "运行环境与来源.json"
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2))

    records = []
    fields = ["sequence", "pass", "features", "model", "started_at", "train_seconds",
              "predict_seconds", "ms_per_sample", "distance_calls", "distance_ratio",
              "tn", "fp", "fn", "tp", "accuracy", "precision", "recall", "f1",
              "prediction_sha256", "evaluation_note"]
    comparisons = []
    with (args.out / "逐轮推理时间.csv").open("w", encoding="utf-8-sig", newline="") as csvfile, \
         (args.out / "运行日志.txt").open("w", encoding="utf-8") as logfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        def log(message):
            print(message, flush=True)
            logfile.write(message + "\n")
            logfile.flush()

        log(f"K={lesson.K}; train={len(train_x)}; test={len(test_x)}; features={lesson.FEATURE_COUNTS}")
        pair_index = 0
        for pass_number in range(1, args.repeats + 1):
            feature_counts = list(lesson.FEATURE_COUNTS)
            if pass_number % 2 == 0:
                feature_counts.reverse()
            for dimension in feature_counts:
                pair_index += 1
                tr_x = [row[:dimension] for row in train_x]
                te_x = [row[:dimension] for row in test_x]
                models = [("KDTree", lesson.KNNClassifier),
                          ("BruteForce", lesson.BruteForceKNNClassifier)]
                if pair_index % 2 == 0:
                    models.reverse()
                predictions = {}
                for model_name, classifier in models:
                    gc.collect()
                    model = classifier(k=lesson.K)
                    started_at = datetime.now(TZ).isoformat()
                    log(f"START pass={pass_number} features={dimension} model={model_name}")
                    t0 = time.perf_counter()
                    model.fit(tr_x, train_y)
                    train_seconds = time.perf_counter() - t0
                    t0 = time.perf_counter()
                    predicted = model.predict(te_x)
                    predict_seconds = time.perf_counter() - t0
                    assert len(predicted) == len(test_y)
                    metrics, note = safe_evaluate(test_y, predicted)
                    calls = model.tree.visited if hasattr(model, "tree") else len(tr_x) * len(te_x)
                    row = {"sequence": len(records) + 1, "pass": pass_number,
                           "features": dimension, "model": model_name, "started_at": started_at,
                           "train_seconds": train_seconds, "predict_seconds": predict_seconds,
                           "ms_per_sample": predict_seconds * 1000 / len(te_x),
                           "distance_calls": calls, "distance_ratio": calls / (len(tr_x) * len(te_x)),
                           **metrics,
                           "prediction_sha256": hashlib.sha256(bytes(predicted)).hexdigest(),
                           "evaluation_note": note}
                    records.append(row)
                    writer.writerow(row)
                    csvfile.flush()
                    predictions[model_name] = predicted
                    log(f"DONE  pass={pass_number} features={dimension} model={model_name} "
                        f"train={train_seconds:.6f}s predict={predict_seconds:.6f}s "
                        f"calls={calls} accuracy={metrics['accuracy']:.4f} f1={metrics['f1']:.4f}"
                        + (f" NOTE={note}" if note else ""))
                    del model
                differences = sum(a != b for a, b in zip(predictions["KDTree"], predictions["BruteForce"]))
                comparisons.append({"pass": pass_number, "features": dimension,
                                    "prediction_differences": differences})
                log(f"COMPARE pass={pass_number} features={dimension} prediction_differences={differences}")

    summary = []
    for dimension in lesson.FEATURE_COUNTS:
        for model_name in ["KDTree", "BruteForce"]:
            rows = [r for r in records if r["features"] == dimension and r["model"] == model_name]
            times = [r["predict_seconds"] for r in rows]
            summary.append({"features": dimension, "model": model_name, "repeats": len(rows),
                            "mean_predict_seconds": statistics.mean(times),
                            "median_predict_seconds": statistics.median(times),
                            "min_predict_seconds": min(times), "max_predict_seconds": max(times),
                            "stdev_predict_seconds": statistics.stdev(times) if len(times) > 1 else 0.0,
                            "mean_train_seconds": statistics.mean(r["train_seconds"] for r in rows),
                            "distance_calls": rows[0]["distance_calls"],
                            "accuracy": rows[0]["accuracy"], "f1": rows[0]["f1"],
                            "predictions_identical_across_repeats": len({r["prediction_sha256"] for r in rows}) == 1})
    for filename, rows in [("耗时汇总.csv", summary), ("预测差异.csv", comparisons)]:
        with (args.out / filename).open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    metadata.update({"status": "completed", "ended_at": datetime.now(TZ).isoformat(),
                     "elapsed_seconds": time.perf_counter() - start, "measurement_count": len(records)})
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2))
    print(f"实验完成：{args.out}；共 {len(records)} 条模型计时记录。", flush=True)


if __name__ == "__main__":
    main()
