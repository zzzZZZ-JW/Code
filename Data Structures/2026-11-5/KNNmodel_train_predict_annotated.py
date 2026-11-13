# 数据结构课堂实验：KD 树 KNN 与暴力搜索 KNN 对比
# 从教师的 need_comment.py 复制，完成 Q1～Q5 并补充关键步骤说明。
# 本副本仅增加注释、说明文字，并把 FEATURE_COUNTS 扩展为五组；搜索逻辑未修改。
# 已发现的剪枝和评估边界问题见《实验记录与代码改进.md》。
# 请在本文件所在目录运行，训练、测试 CSV 放在同一目录。

import csv
import math
import time


# CSV 中 Diabetes_binary 是分类标签：0/1；其余列为输入特征。
TRAIN_FILE = "diabetes_imb_train.csv"
TEST_FILE = "diabetes_imb_test.csv"
K=5  # 对最近的 5 个训练样本投票，决定测试样本的类别。

# 只使用文件开头的这些样本；没有随机抽样，也没有标准化特征。
TRAIN_SAMPLE_COUNT = 10000
TEST_SAMPLE_COUNT = 500


# 每个数字表示取前多少个特征，不包含标签列；不是选取“最重要”的特征。
FEATURE_COUNTS = (2, 7, 10, 15, 17)


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
        '''
        Q1：visited 的作用是什么？
        visited 统计 KD 树搜索累计访问的节点数。
        每访问一个节点，就计算一次该节点与目标点的欧氏距离，因此也代表距离计算次数。
        它在建树后置 0，在每次递归访问时加 1；不是每预测一个样本就自动清零。
        本程序每组实验重新 fit，因此统计的是这组全部测试样本的累计次数。
        与暴力法的“训练样本数 × 测试样本数”比较，可以观察剪枝节省了多少计算。
        '''
        self.visited = 0

    def build(self, points, depth):

        '''
        Q2：如何构建 KD 树？
        1. 空点集返回 None，作为递归终止条件。
        2. 用 depth % self.dim 轮流选择分割维度，如二维时依次选第 0、1、0、1 维。
        3. 按选定维度排序，取中位数位置的点作为当前节点。
        4. 中位数左侧的点递归建左子树，右侧的点递归建右子树。
        5. 返回保存当前点、分割维度和两个子节点的 Node。
        按中位数分割使左右子树的节点数量接近，树高约为 O(log n)。
        本实现每层对子集重新排序，建树时间上界为 O(n log² n)，并有切片复制开销。
        '''
        if not points:
            return None
        axis = depth % self.dim  # depth 从 0 开始，维度编号也从 0 开始。
        points_sorted = sorted(points, key=lambda x: x[axis])
        mid = len(points_sorted) // 2
        median_point = points_sorted[mid]  # 取排序后居中的样本，而非坐标的平均数。
        left = self.build(points_sorted[:mid], depth + 1)
        right = self.build(points_sorted[mid+1:], depth + 1)
        return Node(median_point, axis, left, right)

    # 欧氏距离：对应维度的差值平方求和，再开平方；输入应维度一致。
    def distance(self, p1, p2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

    def knn_search(self, target, k):
        '''
        Q3：如何实现 KD 树搜索？
        用内部递归函数 rec 深度优先搜索，以 knn_list 保存当前至多 k 个最近候选。
        访问节点时：累计 visited、计算距离、加入候选、按距离升序排列；超过 k 个则删掉最远的。
        再根据目标点在当前分割维度的坐标，优先搜索目标所在一侧的子树。
        回溯时，将“目标到分割平面的距离”与“当前候选中最远距离”比较。
        若另一侧可能存在更近点，就继续搜索；否则跳过该子树，实现剪枝。
        注意：下面忠实保留教师代码。候选不足 k 个时，也必须继续搜索另一侧；
        原条件缺少 len(knn_list) < k，可能漏找邻居。距离相等时也需明确统一的取舍规则。
        '''
        knn_list = []  # 每次查询新建；与累计的 visited 不同。
        def rec(node):
            if node is None:
                return
            self.visited += 1  # 当前节点发生一次距离计算。
            dist = self.distance(node.point, target)
            knn_list.append((node.point, dist))
            knn_list.sort(key=lambda x: x[1])
            if len(knn_list) > k:
                knn_list.pop()  # 删除升序列表末尾，也就是当前最远的候选。
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


# 继承 list 保存特征向量；label 作为额外属性保存，不参与距离计算。
class LabeledPoint(list):

    def __init__(self, values, label):
        super().__init__(values)
        self.label = label


# 统计近邻标签的出现次数，票数最多的类别作为预测结果。
# 票数相同时，当前实现保留字典中先出现的类别，因而受近邻遍历顺序影响。
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


# KD 树分类器：fit 建立搜索索引；predict 查询近邻并投票。
# KNN 不像线性模型那样通过 fit 学出一组权重，主要工作在保存样本/建索引。
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
        neighbors = self.tree.knn_search(features, self.k)  # 查询单条测试样本的近邻。
        return majority_vote(neighbors)

    def predict(self, features):
        return [self.predict_one(row) for row in features]  # 按顺序逐条预测。

# 暴力分类器：fit 只保存样本；每次预测都遍历全部训练样本。
class BruteForceKNNClassifier:
    def __init__(self, k=5):
        self.k = k

    def fit(self, features, labels):
        self.points = [
            LabeledPoint(point, label)
            for point, label in zip(features, labels)
        ]
        return self

    # 欧氏距离：对应维度的差值平方求和，再开平方；输入应维度一致。
    def distance(self, p1, p2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

    def predict_one(self, features):
        '''
        Q4：如何实现暴力搜索？
        对当前测试样本，逐个计算它到所有训练样本的欧氏距离。
        将所有“样本、距离”二元组按距离从小到大排序，取前 k 个，再调用多数投票。
        没有剪枝，因此 n 个训练样本、m 个测试样本总共计算 n × m 次距离。
        设特征数为 d，一次预测的距离计算为 O(nd)，全排序为 O(n log n)。
        这个版本在距离相同时保留训练样本原有次序，因为 Python 排序是稳定的。
        '''
        dists = [
            (point, self.distance(point, features))
            for point in self.points
        ]
        dists.sort(key=lambda x: x[1])
        neighbors = dists[:self.k]
        return majority_vote(neighbors)

    def predict(self, features):
        return [self.predict_one(row) for row in features]  # 按顺序逐条预测。

# =================================================================


# DictReader 按表头访问各列；utf-8-sig 同时兼容带 BOM 的 UTF-8 文件。
# 返回特征矩阵、标签列表和特征列名。当前实现先读取全文件，main 再截取前若干行。
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


# 二分类评估：TP 真正例、TN 真负例、FP 假正例、FN 假负例。
# Accuracy=(TP+TN)/总数；Precision=TP/(TP+FP)；Recall=TP/(TP+FN)。
# F1 是精确率和召回率的调和平均。原公式没有处理分母为 0 的情况。
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


# 输出混淆矩阵及四项分类指标；类别不均衡时不能只看准确率。
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


# 一轮模型实验：训练计时 → 预测计时 → 读取距离计算次数 → 评估。
# predict_time 只覆盖整批测试样本的 model.predict，不包含 CSV 读取、训练或打印。
# 教师代码使用 time.time；配套批量记录脚本使用适合测量耗时的 time.perf_counter。
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


# 解包两种模型的结果，比较训练/预测时间、距离计算次数、指标及预测分歧。
# 分歧不一定全部是错误：还可能来自第 k 个近邻边界处的等距离取舍差异。
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

    # 对每一种特征数量重新创建模型，保证不同维度的树互不混用。
    for n_features in FEATURE_COUNTS:
        print("\n" + "#" * 50)
        print(f"### 使用特征数量：{n_features}（只取每条数据的前 {n_features} 列）")
        print("#" * 50)
        tr_x = [row[:n_features] for row in train_x]
        te_x = [row[:n_features] for row in test_x]
        '''
        Q5：run_experiment 的调用过程是什么？
        本轮先从训练集和测试集截取前 n_features 个特征，标签保持不变。
        第一次调用：创建 KNNClassifier(k=K)，传入训练特征/标签、测试特征/标签和名称。
        函数内部调用 fit 建树并记录训练时间，再调用 predict 预测全部测试样本并记录推理时间。
        之后统计距离计算次数，计算并打印分类指标。
        返回 (metrics, train_time, predict_time, predictions, dist_calls)，保存为 kd_result。
        第二次调用：换成 BruteForceKNNClassifier，其余输入相同，返回值保存为 bf_result。
        最后 compare_and_print 对照两个结果；外层循环进入下一种特征数量。
        '''
        kd_result = run_experiment(
            KNNClassifier(k=K), tr_x, train_y, te_x, test_y,
            f"KD 树版 KNN（{n_features} 维）",
        )
        bf_result = run_experiment(
            BruteForceKNNClassifier(k=K), tr_x, train_y, te_x, test_y,
            f"暴力搜索版 KNN（{n_features} 维）",
        )
        compare_and_print(tr_x, te_x, kd_result, bf_result)


# 直接运行本文件时执行 main；被其他脚本 import 时只加载定义，不自动实验。
if __name__ == "__main__":
    main()
