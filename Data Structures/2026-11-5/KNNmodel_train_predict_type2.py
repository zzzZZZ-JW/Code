import csv
import math
import time


TRAIN_FILE = "diabetes_imb_train.csv"
TEST_FILE = "diabetes_imb_test.csv"
K=5

TRAIN_SAMPLE_COUNT = 10000
TEST_SAMPLE_COUNT = 500


FEATURE_COUNTS = (21, 5)


class Node:
    """KD树节点"""
    def __init__(self, point, axis, left=None, right=None):
        self.point = point    # 坐标点，tuple/list
        self.axis = axis      # 分割维度
        self.left = left      # 左子树
        self.right = right    # 右子树


class KDTree:
    def __init__(self, points):
        self.dim = len(points[0]) if points else 0
        self.root = self.build(points, depth=0)
        self.visited = 0

    def build(self, points, depth):
        if not points:
            return None
        axis = depth % self.dim
        points_sorted = sorted(points, key=lambda x: x[axis])
        mid = len(points_sorted) // 2
        median_point = points_sorted[mid]
        left = self.build(points_sorted[:mid], depth + 1)
        right = self.build(points_sorted[mid+1:], depth + 1)
        return Node(median_point, axis, left, right)

    def distance(self, p1, p2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

    def knn_search(self, target, k):
        knn_list = []
        def rec(node):
            if node is None:
                return
            self.visited += 1      # 【新增】每访问一个节点计数 +1
            dist = self.distance(node.point, target)
            knn_list.append((node.point, dist))
            knn_list.sort(key=lambda x: x[1])
            if len(knn_list) > k:
                knn_list.pop()
            axis = node.axis
            if target[axis] < node.point[axis]:
                rec(node.left)
                if abs(target[axis] - node.point[axis]) < knn_list[-1][1]:
                    rec(node.right)
            else:
                rec(node.right)
                if abs(target[axis] - node.point[axis]) < knn_list[-1][1]:
                    rec(node.left)
        rec(self.root)
        return knn_list


class LabeledPoint(list):

    def __init__(self, values, label):
        super().__init__(values)
        self.label = label


def majority_vote(neighbors):

    votes = {}
    for point, _ in neighbors:
        label = point.label
        if label in votes:
            votes[label] += 1
        else:
            votes[label] = 1

    predicted_label = None
    max_votes = 0
    for label, count in votes.items():
        if count > max_votes:
            predicted_label = label
            max_votes = count
    return predicted_label


class KNNClassifier:

    def __init__(self, k=5):
        self.k = k

    def fit(self, features, labels):
        points = [
            LabeledPoint(point, label)
            for point, label in zip(features, labels)
        ]
        self.tree = KDTree(points)
        return self

    def predict_one(self, features):
        neighbors = self.tree.knn_search(features, self.k)
        return majority_vote(neighbors)

    def predict(self, features):
        return [self.predict_one(row) for row in features]

class BruteForceKNNClassifier:
    def __init__(self, k=5):
        self.k = k

    def fit(self, features, labels):
        self.points = [
            LabeledPoint(point, label)
            for point, label in zip(features, labels)
        ]
        return self

    def distance(self, p1, p2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

    def predict_one(self, features):
        dists = [
            (point, self.distance(point, features))
            for point in self.points
        ]
        dists.sort(key=lambda x: x[1])
        neighbors = dists[:self.k]
        return majority_vote(neighbors)

    def predict(self, features):
        return [self.predict_one(row) for row in features]

# =================================================================


def load_dataset(csv_path):
    features = []
    labels = []
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        feature_names = [
            name for name in reader.fieldnames if name != "Diabetes_binary"
        ]
        for row in reader:
            features.append([float(row[name]) for name in feature_names])
            labels.append(int(float(row["Diabetes_binary"])))
    return features, labels, feature_names


def evaluate_binary(y_true, y_pred):
    tp = sum(true == 1 and pred == 1 for true, pred in zip(y_true, y_pred))
    tn = sum(true == 0 and pred == 0 for true, pred in zip(y_true, y_pred))
    fp = sum(true == 0 and pred == 1 for true, pred in zip(y_true, y_pred))
    fn = sum(true == 1 and pred == 0 for true, pred in zip(y_true, y_pred))

    accuracy = (tp + tn) / len(y_true)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * precision * recall / (precision + recall)
    return {
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def print_evaluation(metrics, sample_count):
    print(f"\n评测样本数：{sample_count}")
    print("混淆矩阵（行=真实类别，列=预测类别）：")
    print("              预测 0    预测 1")
    print(f"    真实 0  {metrics['tn']:>8d}  {metrics['fp']:>8d}")
    print(f"    真实 1  {metrics['fn']:>8d}  {metrics['tp']:>8d}")
    print(f"准确率 Accuracy ：{metrics['accuracy']:.4f}")
    print(f"精确率 Precision：{metrics['precision']:.4f}")
    print(f"召回率 Recall   ：{metrics['recall']:.4f}")
    print(f"F1 值           ：{metrics['f1']:.4f}")


def run_experiment(model, train_x, train_y, test_x, test_y, model_name):
    print(f"\n========== {model_name} ==========")
    print("正在训练……")

    t0 = time.time()
    model.fit(train_x, train_y)
    train_time = time.time() - t0
    print(f"训练完成，耗时 {train_time:.4f} 秒，正在预测……")

    t0 = time.time()
    predictions = model.predict(test_x)
    predict_time = time.time() - t0
    print(f"预测完成，耗时 {predict_time:.4f} 秒")

    if hasattr(model, "tree"):
        dist_calls = model.tree.visited
    else:
        dist_calls = len(train_x) * len(test_x)

    metrics = evaluate_binary(test_y, predictions)
    print_evaluation(metrics, len(test_y))
    return metrics, train_time, predict_time, predictions, dist_calls


def compare_and_print(train_x, test_x, kd_result, bf_result):
    (kd_m, kd_tt, kd_pt, kd_pred, kd_calls) = kd_result
    (bf_m, bf_tt, bf_pt, bf_pred, bf_calls) = bf_result

    diff_count = sum(a != b for a, b in zip(kd_pred, bf_pred))
    kd_total, bf_total = kd_tt + kd_pt, bf_tt + bf_pt
    kd_ratio = kd_calls / bf_calls

    print("\n========== 对比汇总 ==========")
    print(f"{'':>16}{'KD 树版':>14}{'暴力版':>14}")
    print(f"{'训练耗时(s)':>16}{kd_tt:>14.4f}{bf_tt:>14.4f}")
    print(f"{'预测耗时(s)':>16}{kd_pt: >14.4f}{bf_pt:>14.4f}")
    print(f"{'总耗时(s)':>16}{kd_total:>14.4f}{bf_total:>14.4f}")
    print(f"{'距离计算次数':>16}{kd_calls:>14d}{bf_calls:>14d}")
    print(f"{'准确率':>16}{kd_m['accuracy']:>14.4f}{bf_m['accuracy']:>14.4f}")
    print(f"{'F1 值':>16}{kd_m['f1']:>14.4f}{bf_m['f1']:>14.4f}")
    print(f"\nKD 树距离计算次数仅为暴力版的 {kd_ratio:.1%}")
    print(f"两种方法预测不一致的样本数：{diff_count}")


def main():
    train_x, train_y, train_feature_names = load_dataset(TRAIN_FILE)
    test_x, test_y, test_feature_names = load_dataset(TEST_FILE)

    train_x = train_x[:TRAIN_SAMPLE_COUNT]
    train_y = train_y[:TRAIN_SAMPLE_COUNT]
    test_x = test_x[:TEST_SAMPLE_COUNT]
    test_y = test_y[:TEST_SAMPLE_COUNT]

    print(f"训练集：{TRAIN_FILE}")
    print(f"测试集：{TEST_FILE}")
    print(f"训练样本：{len(train_x)}，测试样本：{len(test_x)}，"
          f"全部特征数：{len(train_feature_names)}，K={K}")

    for n_features in FEATURE_COUNTS:
        print("\n" + "#" * 50)
        print(f"### 使用特征数量：{n_features}（只取每条数据的前 {n_features} 列）")
        print("#" * 50)
        tr_x = [row[:n_features] for row in train_x]
        te_x = [row[:n_features] for row in test_x]

        kd_result = run_experiment(
            KNNClassifier(k=K), tr_x, train_y, te_x, test_y,
            f"KD 树版 KNN（{n_features} 维）",
        )
        bf_result = run_experiment(
            BruteForceKNNClassifier(k=K), tr_x, train_y, te_x, test_y,
            f"暴力搜索版 KNN（{n_features} 维）",
        )
        compare_and_print(tr_x, te_x, kd_result, bf_result)


if __name__ == "__main__":
    main()
