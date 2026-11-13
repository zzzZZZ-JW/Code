"""根据逐轮实测 CSV 生成题 21 的记录表、折线图和实验报告。

运行 python3 plot_feature_efficiency.py，默认读取同目录的“题21_实验结果”。
绘图依赖 matplotlib，所有图表数据均来自 run_feature_experiments.py 的输出。
"""

import argparse
import csv
import json
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import PercentFormatter


ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", nargs="?", type=Path, default=ROOT / "题21_实验结果")
    args = parser.parse_args()
    metadata = json.loads((args.results / "运行环境与来源.json").read_text())
    if metadata["status"] != "completed":
        raise ValueError("请等待全部计时完成后再绘图。")
    with (args.results / "逐轮推理时间.csv").open(encoding="utf-8-sig", newline="") as file:
        records = list(csv.DictReader(file))

    # 字典按实际执行顺序分组，每组包含同一遍、同一维度的两种模型。
    groups = {}
    for record in records:
        key = (int(record["pass"]), int(record["features"]))
        groups.setdefault(key, {})[record["model"]] = record
    pairs = []
    for (repeat, dimension), models in groups.items():
        kd, brute = models["KDTree"], models["BruteForce"]
        kd_calls, brute_calls = int(kd["distance_calls"]), int(brute["distance_calls"])
        assert brute_calls == metadata["train_samples"] * metadata["test_samples"]
        pairs.append({
            "round": len(pairs) + 1,
            "repeat": repeat,
            "features": dimension,
            "kd_calls": kd_calls,
            "bf_calls": brute_calls,
            "kd_ratio": kd_calls / brute_calls,
            "kd_train_seconds": float(kd["train_seconds"]),
            "kd_predict_seconds": float(kd["predict_seconds"]),
            "kd_total_seconds": float(kd["train_seconds"]) + float(kd["predict_seconds"]),
            "bf_train_seconds": float(brute["train_seconds"]),
            "bf_predict_seconds": float(brute["predict_seconds"]),
            "bf_total_seconds": float(brute["train_seconds"]) + float(brute["predict_seconds"]),
        })
    with (args.results / "题21_逐轮记录.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(pairs[0]))
        writer.writeheader()
        writer.writerows(pairs)

    dimensions = sorted({row["features"] for row in pairs})
    summaries = []
    for dimension in dimensions:
        rows = [row for row in pairs if row["features"] == dimension]
        assert len(rows) == metadata["repeats"]
        assert len({row["kd_ratio"] for row in rows}) == 1
        summaries.append({
            "features": dimension,
            "kd_calls": rows[0]["kd_calls"],
            "kd_ratio": rows[0]["kd_ratio"],
            "kd_predict": statistics.median(row["kd_predict_seconds"] for row in rows),
            "bf_predict": statistics.median(row["bf_predict_seconds"] for row in rows),
            "kd_total": statistics.median(row["kd_total_seconds"] for row in rows),
            "bf_total": statistics.median(row["bf_total_seconds"] for row in rows),
        })

    available_fonts = {font.name for font in font_manager.fontManager.ttflist}
    chinese_fonts = [name for name in ["PingFang SC", "Heiti TC", "STHeiti", "Arial Unicode MS",
                                       "Noto Sans CJK SC", "Microsoft YaHei", "SimHei"]
                     if name in available_fonts]
    if not chinese_fonts:
        raise RuntimeError("需要可显示中文的字体，请安装 Noto Sans CJK SC 后重试。")
    plt.rcParams.update({"font.family": chinese_fonts + ["DejaVu Sans"],
                         "axes.unicode_minus": False, "font.size": 11})
    ratios = [row["kd_ratio"] for row in summaries]
    fig, ax = plt.subplots(figsize=(9.6, 5.7), layout="constrained")
    ax.plot(dimensions, ratios, color="#177A87", linewidth=2.6,
            marker="o", markersize=7, markeredgecolor="white", markeredgewidth=1.4)
    for dimension, ratio in zip(dimensions, ratios):
        ax.annotate(f"{ratio:.2%}", (dimension, ratio), xytext=(0, 12),
                    textcoords="offset points", ha="center", color="#15515A", fontsize=11)
    ax.set_title("题21  特征维数与 KD 树检索效率", loc="left", fontsize=18, pad=35)
    ax.text(0, 1.035,
            f"训练 {metadata['train_samples']:,} 条  ·  测试 {metadata['test_samples']:,} 条  ·  "
            f"K={metadata['k']}  ·  每维重复 {metadata['repeats']} 次，kd_ratio 一致",
            transform=ax.transAxes, color="#536471", fontsize=10)
    ax.set_xlabel("特征维数", labelpad=10)
    ax.set_ylabel("kd_ratio（KD 树距离计算次数 / 暴力法距离计算次数）", labelpad=12)
    ax.set_xticks(dimensions)
    ax.set_xlim(min(dimensions) - 0.8, max(dimensions) + 0.8)
    ax.set_ylim(0, min(1.08, max(ratios) * 1.28))
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.grid(axis="y", color="#DDE3E8", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#BAC5CD")
    image_path = args.results / "特征维数与kd_ratio.png"
    fig.savefig(image_path, dpi=200, facecolor="white")
    plt.close(fig)

    lines = [
        "# 题21 特征维数与 KD 树检索效率", "",
        "本次按题目指定的 2、7、10、15、17 个特征进行实验，每个维度重复 3 次，共完成 15 轮对照、30 次模型运行。", "",
        "## 实验设置", "",
        "```python", "TRAIN_SAMPLE_COUNT = 10000", "TEST_SAMPLE_COUNT = 500",
        "K = 5", "FEATURE_COUNTS = (2, 7, 10, 15, 17)", "```", "",
        "每组取数据集的前 d 个特征。训练样本和测试样本分别取原 CSV 的前 10,000 条、500 条，沿用教师实现。",
        "每次重新建立模型并累计该批测试样本的距离计算次数。暴力法每轮计算 10,000 × 500 = 5,000,000 次距离。", "",
        "```text", "kd_ratio = KD 树距离计算次数 / 暴力法距离计算次数",
        "         = model.tree.visited / 5,000,000", "```", "",
        "kd_ratio 越小，表示 KD 树访问的训练点越少，剪枝节省的距离计算越多。", "",
        "运行时间使用 time.perf_counter 测量。分别记录训练、500 条样本的整批预测以及两者之和。读取 CSV、计算指标和绘图均在计时区间外。汇总表使用三次时间的中位数。", "",
        f"本机环境为 {metadata.get('cpu', metadata['machine'])}，Python {metadata['python'].split()[0]}。",
        f"实验开始于 {metadata['started_at']}，结束于 {metadata['ended_at']}，含加载和记录共 {metadata['elapsed_seconds']:.2f} 秒。", "",
        "## 逐轮记录", "",
        "下表按实际执行顺序排列，时间单位为秒。逐轮训练耗时和两模型总耗时另存于 `题21_逐轮记录.csv`。", "",
        "| 轮次 | 重复遍数 | 特征维数 | kd_ratio | KD 预测时间 | 暴力预测时间 |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in pairs:
        lines.append(f"| {row['round']} | {row['repeat']} | {row['features']} | "
                     f"{row['kd_ratio']:.7f} | {row['kd_predict_seconds']:.6f} | {row['bf_predict_seconds']:.6f} |")
    lines += ["", "## 汇总与折线图", "",
              "| 特征维数 | KD 距离计算次数 | kd_ratio | KD 预测中位数/s | 暴力预测中位数/s | KD 总时间中位数/s | 暴力总时间中位数/s |",
              "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for row in summaries:
        lines.append(f"| {row['features']} | {row['kd_calls']:,} | {row['kd_ratio']:.7f} | "
                     f"{row['kd_predict']:.6f} | {row['bf_predict']:.6f} | "
                     f"{row['kd_total']:.6f} | {row['bf_total']:.6f} |")
    first, last = summaries[0], summaries[-1]
    lines += ["", f"![特征维数与 kd_ratio 折线图](<{image_path.resolve()}>)", "",
              "## 观察与解释", "",
              f"1. 特征维数从 {first['features']} 增加到 {last['features']} 时，kd_ratio 从 "
              f"{first['kd_ratio']:.7f}（{first['kd_ratio']:.2%}）上升到 "
              f"{last['kd_ratio']:.7f}（{last['kd_ratio']:.2%}）。本次五个采样维度的比例逐步升高，说明需要访问的节点增加，剪枝效果减弱。",
              f"2. KD 树整批预测时间的中位数从 {first['kd_predict']:.6f} 秒上升到 "
              f"{last['kd_predict']:.6f} 秒。维度增加既使单次距离计算更费时，也伴随更多节点访问。",
              f"3. 暴力法的距离计算次数始终为 5,000,000，但预测时间的中位数从 "
              f"{first['bf_predict']:.6f} 秒上升到 {last['bf_predict']:.6f} 秒，因为每次距离计算需要处理更多分量。",
              f"4. 暴力预测时间与 KD 预测时间的中位数之比，从约 "
              f"{first['bf_predict']/first['kd_predict']:.2f} 倍下降到约 "
              f"{last['bf_predict']/last['kd_predict']:.2f} 倍。KD 树在本次较低维配置中的耗时优势更大。",
              "5. kd_ratio 反映距离计算次数的比例，运行时间还包含递归、候选排序、投票等开销，因此耗时比与 kd_ratio 通常有差别。同一配置三次的 kd_ratio 一致，耗时受系统调度等影响有少量波动。", "",
              "本实验同时改变了特征数量和输入列的内容，上述趋势来自当前数据及实现。教师 KD 树在候选不足 K 个时可能过早剪枝，等距离点的取舍也会造成预测分歧，这些问题会影响结果解释。", "",
              "2 维时两模型全部预测为 0，原评估函数出现除零。记录脚本保存异常并按零分母指标取 0 的约定继续，计时在评估前结束。", "",
              "## 复现命令", "", "```bash",
              f'cd "{ROOT}"',
              'python3 run_feature_experiments.py --repeats 3 --out "题21_再次运行"',
              'python3 plot_feature_efficiency.py "题21_再次运行"', "```", "",
              "绘图使用 matplotlib。原始时间、预测一致性、评估异常和运行环境分别保存在同目录的 CSV、日志和 JSON 中。", ""]
    report_path = args.results / "题21_实验报告.md"
    report_path.write_text("\n".join(lines))
    print(report_path)
    print(image_path)


if __name__ == "__main__":
    main()
