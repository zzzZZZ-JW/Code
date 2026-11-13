"""用极小输入验证改进建议，不运行数据集耗时实验，也不修改教师代码。"""

from pathlib import Path
import ast

import KNNmodel_train_predict_need_comment as teacher


def main():
    # 反例 1：有 5 个训练样本，k=5，正确近邻集应包含全部样本。
    features = [[0.0], [1.0], [2.0], [3.0], [4.0]]
    labels = [1, 1, 1, 0, 0]
    model = teacher.KNNClassifier(k=5).fit(features, labels)
    neighbors = model.tree.knn_search([4.0], 5)
    kd_prediction = teacher.majority_vote(neighbors)
    brute_prediction = teacher.BruteForceKNNClassifier(k=5).fit(features, labels).predict_one([4.0])
    assert len(neighbors) == 3 and kd_prediction == 0 and brute_prediction == 1
    print("已复现：k=5 时仅返回 3 个邻居，KD 树预测 0，暴力法预测 1。")
    print("KD 树返回的坐标：", [list(point) for point, _ in neighbors])

    # 仅在内存加载一份修正条件的源码，验证改进建议；原始文件完全不变。
    root = Path(__file__).resolve().parent
    source = (root / "KNNmodel_train_predict_need_comment.py").read_text()
    old = "if abs(target[axis] - node.point[axis]) < knn_list[-1][1]:"
    new = "if len(knn_list) < k or abs(target[axis] - node.point[axis]) <= knn_list[-1][1]:"
    assert source.count(old) == 2
    scope = {"__name__": "boundary_demo"}
    exec(compile(source.replace(old, new), "<in-memory-pruning-demo>", "exec"), scope)
    fixed = scope["KNNClassifier"](k=5).fit(features, labels)
    fixed_neighbors = fixed.tree.knn_search([4.0], 5)
    assert len(fixed_neighbors) == 5 and scope["majority_vote"](fixed_neighbors) == 1
    print("条件修正验证：返回 5 个邻居、预测 1；此修正未加入正式计时。")

    # 反例 2：k=1，没有“候选不足”的问题，等距离取舍仍会导致两个实现预测不同。
    features, labels = [[-1.0], [1.0]], [0, 1]
    kd = teacher.KNNClassifier(k=1).fit(features, labels).predict_one([0.0])
    bf = teacher.BruteForceKNNClassifier(k=1).fit(features, labels).predict_one([0.0])
    fixed = scope["KNNClassifier"](k=1).fit(features, labels).predict_one([0.0])
    assert kd == 1 and bf == 0 and fixed == 1
    print("已复现：等距离时 KD 树预测 1，暴力法预测 0；仅修正剪枝仍不足以统一结果。")

    for truth, prediction, reason in [
        ([0, 0], [0, 0], "没有预测正例，Precision 分母为 0"),
        ([0, 1], [1, 0], "Precision、Recall 均为 0，F1 分母为 0"),
    ]:
        try:
            teacher.evaluate_binary(truth, prediction)
        except ZeroDivisionError:
            print("已复现评估除零：" + reason)
        else:
            raise AssertionError("预期复现的评估异常未发生")

    # 注释副本除参数 FEATURE_COUNTS 外必须保持原执行逻辑。
    class Normalize(ast.NodeTransformer):
        def visit_Expr(self, node):
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                return None
            return self.generic_visit(node)

        def visit_Assign(self, node):
            if any(isinstance(target, ast.Name) and target.id == "FEATURE_COUNTS" for target in node.targets):
                node.value = ast.parse("(21, 5)", mode="eval").body
            return self.generic_visit(node)

    annotated = (root / "KNNmodel_train_predict_annotated.py").read_text()
    assert ast.dump(Normalize().visit(ast.parse(source))) == ast.dump(Normalize().visit(ast.parse(annotated)))
    print("已验证：注释副本与原版语法树等价（忽略说明字符串及 FEATURE_COUNTS 参数）。")


if __name__ == "__main__":
    main()
