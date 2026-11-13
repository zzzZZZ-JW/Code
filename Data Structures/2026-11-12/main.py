"""数据结构实践：评分数据划分、训练矩阵、基本统计和 NumPy 操作。"""

from pathlib import Path

import numpy as np


BASE_DIR = Path(__file__).resolve().parent
RANDOM_SEED = 42
TRAIN_RATIO = 0.8


def load_ratings(path):
    """读取四列整数：用户 ID、电影 ID、评分、时间戳。"""
    # loadtxt 的分隔符只能是单个字符，先把 :: 替换为空格。
    with path.open(encoding="utf-8") as file:
        ratings = np.loadtxt(
            (line.replace("::", " ") for line in file),
            dtype=np.int64,
            ndmin=2,
        )
    if ratings.size == 0 or ratings.shape[1] != 4:
        raise ValueError("ratings.dat 应为非空的四列评分记录。")
    if not np.all((ratings[:, 2] >= 1) & (ratings[:, 2] <= 5)):
        raise ValueError("评分必须在 1～5 之间；0 留作未评分标记。")
    return ratings


def split_ratings(ratings, train_ratio=TRAIN_RATIO, seed=RANDOM_SEED):
    """任务 1：打乱记录的行号，按 8:2 划分训练集和测试集。"""
    if not 0 < train_ratio < 1:
        raise ValueError("训练集比例必须在 0 和 1 之间。")
    rng = np.random.default_rng(seed)
    indices = rng.permutation(len(ratings))
    split_at = int(len(ratings) * train_ratio)
    train = ratings[indices[:split_at]]
    test = ratings[indices[split_at:]]
    return train, test


def build_train_matrix(train, user_ids, movie_ids):
    """任务 2：构建 ndarray 训练矩阵，未评分位置保持为 0。"""
    # user_ids、movie_ids 是完整数据中排序后的唯一 ID。
    # 电影编号不连续，不能直接用电影 ID - 1 作为列号。
    rows = np.searchsorted(user_ids, train[:, 0])
    cols = np.searchsorted(movie_ids, train[:, 1])
    Rtr = np.zeros((len(user_ids), len(movie_ids)), dtype=np.float32)
    Rtr[rows, cols] = train[:, 2]
    return Rtr


def calculate_means(Rtr):
    """任务 3：按用户和电影统计均值，排除表示未评分的 0。"""
    user_count = np.count_nonzero(Rtr, axis=1)
    movie_count = np.count_nonzero(Rtr, axis=0)

    # 行表示用户，列表示电影。不能直接 Rtr.mean()，否则会计入 0。
    # 没有训练评分时均值无定义，用 NaN 表示，避免除零及测试集泄漏。
    u_mean = np.divide(
        Rtr.sum(axis=1, dtype=np.float64),
        user_count,
        out=np.full(Rtr.shape[0], np.nan),
        where=user_count > 0,
    )
    i_mean = np.divide(
        Rtr.sum(axis=0, dtype=np.float64),
        movie_count,
        out=np.full(Rtr.shape[1], np.nan),
        where=movie_count > 0,
    )
    return u_mean, i_mean


def numpy_practice():
    """任务 4（选做）：用小矩阵演示 NumPy，避免对大矩阵做昂贵运算。"""
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    examples = [
        ("数组 A", A),
        ("数组 B", B),
        ("加法 A + B", A + B),
        ("减法 A - B", A - B),
        ("逐元素乘法 A * B", A * B),
        ("逐元素除法 A / B", A / B),
        ("矩阵乘法 A @ B（行与列相乘后求和）", A @ B),
        ("转置 A.T", A.T),
        ("取模 A % 2", A % 2),
        ("矩阵求逆 np.linalg.inv(A)", np.linalg.inv(A)),
        ("切片 A[:, 0]（第一列）", A[:, 0]),
        ("改变形状 A.reshape(1, 4)", A.reshape(1, 4)),
        ("按列求和 A.sum(axis=0)", A.sum(axis=0)),
        ("按行求均值 A.mean(axis=1)", A.mean(axis=1)),
    ]
    return "\n\n".join(f"{name}：\n{value}" for name, value in examples)


def main():
    data_path = BASE_DIR / "ratings.dat"
    if not data_path.is_file():
        raise FileNotFoundError(f"请将 ratings.dat 放在程序同目录：{BASE_DIR}")

    ratings = load_ratings(data_path)
    user_ids = np.unique(ratings[:, 0])
    movie_ids = np.unique(ratings[:, 1])
    if (len(user_ids), len(movie_ids)) != (6040, 3706):
        raise ValueError("本题要求的数据应包含 6040 名用户和 3706 部电影。")

    # 一名用户对一部电影应只有一条评分，否则矩阵赋值会覆盖旧值。
    all_rows = np.searchsorted(user_ids, ratings[:, 0])
    all_cols = np.searchsorted(movie_ids, ratings[:, 1])
    pair_keys = all_rows * len(movie_ids) + all_cols
    if len(np.unique(pair_keys)) != len(ratings):
        raise ValueError("发现重复的用户—电影评分，请先明确重复记录处理规则。")

    train, test = split_ratings(ratings)
    Rtr = build_train_matrix(train, user_ids, movie_ids)
    u_mean, i_mean = calculate_means(Rtr)

    # 两组对应位置的含义由 user_ids、movie_ids 决定，一起保存便于查阅。
    output_dir = BASE_DIR / "results"
    output_dir.mkdir(exist_ok=True)
    np.savez_compressed(
        output_dir / "results.npz",
        train=train,
        test=test,
        Rtr=Rtr,
        u_mean=u_mean,
        i_mean=i_mean,
        user_ids=user_ids,
        movie_ids=movie_ids,
        seed=RANDOM_SEED,
        train_ratio=TRAIN_RATIO,
    )

    np.set_printoptions(precision=4, suppress=True)
    report = "\n".join([
        "任务 1：数据集划分",
        f"总记录数：{len(ratings):,}",
        f"随机种子：{RANDOM_SEED}",
        f"训练集：{len(train):,} 条；测试集：{len(test):,} 条",
        "划分方式：随机打乱全部记录，训练集数量向下取整为总数的 80%",
        "",
        "任务 2：矩阵构建",
        f"Rtr 类型：{type(Rtr).__name__}；形状：{Rtr.shape}；数据类型：{Rtr.dtype}",
        f"已评分位置：{np.count_nonzero(Rtr):,}；其余位置为 0",
        f"前 5 个用户 ID：{user_ids[:5]}",
        f"前 5 个电影 ID：{movie_ids[:5]}",
        "",
        "任务 3：基本统计（仅使用训练评分）",
        f"u_mean 形状：{u_mean.shape}；前 5 项：{u_mean[:5]}",
        f"i_mean 形状：{i_mean.shape}；前 5 项：{i_mean[:5]}",
        f"无训练评分的用户：{np.isnan(u_mean).sum()}；电影：{np.isnan(i_mean).sum()}",
        "无训练评分时，均值保存为 NaN（未定义），不使用测试评分填补。",
        "",
        "任务 4：NumPy 基本操作（选做）",
        numpy_practice(),
        "",
        f"完整数组已保存至：{output_dir / 'results.npz'}",
    ])
    (output_dir / "运行结果.txt").write_text(report + "\n", encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
