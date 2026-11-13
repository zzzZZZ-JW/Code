# 2026-11-12 数据结构实践

按课堂图片完成三项必做任务和一项 NumPy 选做任务。

## 运行

```bash
cd '/Users/zhangjiawei/Class Code/Data Structures/2026-11-12'
python3 main.py
```

也可以在 VS Code 中打开 `main.py`，选择“运行 Python 文件”。程序使用自身所在目录定位数据，不受终端当前目录影响。

如果所选 Python 环境缺少 NumPy，运行 `python3 -m pip install -r requirements.txt`。当前实际验证环境为 Python 3.13.9、NumPy 2.2.6。

## 四项任务

1. **数据集划分**：读取 `ratings.dat` 的全部记录，用随机种子 `42` 打乱行号；前 `int(总数 × 0.8)` 条作为训练集，其余作为测试集。每行保留用户 ID、电影 ID、评分、时间戳四列，重复运行使用相同输入、种子和环境可复现划分。
2. **矩阵构建**：创建形状为 `(6040, 3706)` 的 NumPy `ndarray`，变量名为 `Rtr`，只填入训练集评分，其他位置为 `0`。
3. **基本统计**：按行计算用户平均分 `u_mean`，按列计算电影平均分 `i_mean`，长度分别为 `6040` 和 `3706`。计算时排除未评分的 `0`；没有训练评分的行或列使用 `NaN`，表示均值未定义。
4. **NumPy 选做**：演示数组加减、逐元素乘除、矩阵乘法、转置、取模、求逆、切片、改变形状及按轴统计。`A * B` 是逐元素相乘，`A @ B` 才是矩阵乘法。

电影编号并不连续，3,706 部电影的最大编号是 3,952，因此不能使用 `movie_id - 1` 直接定位列。程序将完整数据中排序后的电影 ID 映射为连续列号；全量数据只用于确定用户和电影的坐标，测试集评分不参与 `Rtr` 和均值的计算。

## 文件与结果

- `main.py`：可直接运行的完整程序，含中文注释。
- `ratings.dat`：从同课程 `../2026-9-10/ratings.dat` 原样复制的输入数据，原文件未修改。
- `requirements.txt`：Python 依赖。
- `results/运行结果.txt`：本次运行的数量、形状、均值示例和 NumPy 运算输出。
- `results/results.npz`：压缩保存的完整数组，仅在本地生成，不纳入 Git；运行程序会更新本目录内这两个结果文件。

`results.npz` 包含下列数组：

| 名称 | 内容 |
| --- | --- |
| `train`、`test` | 训练集、测试集，均保留原始四列记录 |
| `Rtr` | 训练评分矩阵，`float32` 类型 |
| `u_mean`、`i_mean` | 用户和电影的平均分 |
| `user_ids`、`movie_ids` | 每一行、每一列对应的原始 ID |
| `seed`、`train_ratio` | 本次使用的随机种子和训练集比例 |

例如，`Rtr[r, c]` 表示用户 `user_ids[r]` 对电影 `movie_ids[c]` 的训练评分。`i_mean[c]` 对应的也是该电影，不是电影编号 `c + 1`。

可以在本目录下用 Python 读取保存的结果：

```python
import numpy as np

with np.load("results/results.npz") as result:
    print(result["Rtr"].shape)
    print(result["train"].shape, result["test"].shape)
    print(result["u_mean"][:5])
    print(result["movie_ids"][:5], result["i_mean"][:5])
```

## 本次完成及验证记录（2026-11-12）

四项任务均已实现，并使用完整数据执行 `main.py`，生成上述两个结果文件。

| 项目 | 实际结果 |
| --- | --- |
| 总评分数 | 1,000,209 |
| 训练集记录数 | 800,167 |
| 测试集记录数 | 200,042 |
| `Rtr.shape` | `(6040, 3706)` |
| 训练矩阵非零数 | 800,167 |
| `u_mean.shape` | `(6040,)` |
| `i_mean.shape` | `(3706,)` |
| 无训练评分的用户 / 电影 | 0 / 37 |

37 部电影的全部记录被随机分到了测试集，因此它们在训练矩阵中对应整列为 0，`i_mean` 对应项为 `NaN`。这是按记录随机划分的正常结果；没有为消除 `NaN` 而改动划分或使用测试评分。

已通过以下本地检查：

- 输入副本与原文件的 SHA-256 一致。
- 拼接训练集和测试集、重新排序后，四列记录与输入逐条一致；两组用户—电影对没有交集。
- 使用相同种子再次划分，训练集和测试集分别完全一致。
- 所有训练评分都在矩阵的正确位置，所有测试评分对应的矩阵位置均为 0。
- 独立从训练记录按 ID 汇总，核对全部用户均值和电影均值。
- 使用人工可算的小数据验证非连续电影 ID、未评分的 0，以及空行、空列的 `NaN` 处理。

代码、数据和结果均留在本目录；未进行 Git 提交或推送。已在当前 VS Code 工作区通过右上角运行按钮验证。

## VS Code 运行路径排查（2026-11-12）

- 在 `Class Code` 工作区的“运行 Python 文件”按钮复现了路径重复加引号：文件名参数成为包含双引号字符的 `"/Users/.../main.py"`，Python 因而报告找不到文件。
- 11 月 9 日的修复保留在 `Data Structures/.vscode/settings.json`，但本次打开的是上一级 `Class Code` 工作区，子目录配置未作为当前工作区配置加载。
- 已在 `Class Code/.vscode/settings.json` 增补 `"python.useEnvironmentsExtension": false` 并重载窗口，使用 Python 扩展原有运行方式；其他原有设置保留。
- 重载后，原有 Python 扩展读到了以前缓存的 `Class Code/.venv/bin/python`。这是指向已不存在的 Homebrew Python 的软链接；用户本次使用且可运行本程序的解释器为 `/usr/local/bin/python3`。
- 用户反馈快捷键无响应后，已通过“查看 → 命令面板…”执行 `Python: Select Interpreter`，实际选中 `/usr/local/bin/python3`（Python 3.13.9）。状态栏已确认该解释器，NumPy 缺失警告已消失。
- 同时在 `Class Code/.vscode/settings.json` 设置 `"python.defaultInterpreterPath": "/usr/local/bin/python3"`，作为未来首次选择解释器时的默认值。该设置不能代替当前工作区实际选择解释器，因此两步均已完成。
- 已点击同一 `main.py` 的右上角“运行 Python 文件”按钮：终端命令只保留正确的一层路径引号，程序完整运行，更新结果文件并返回 shell 提示符。实际结果仍为训练集 800,167 条、测试集 200,042 条、矩阵 `(6040, 3706)`。
- 未发现用户或扩展重映射命令面板快捷键的配置；没有修改快捷键。此前无响应的具体原因未确定，本次通过菜单已完成配置和按钮验证。
- 修复范围是当前 `Class Code` 工作区；旧 `.venv` 未修改，其他 Python 环境和全局设置未修改。若以后以其他目录作为工作区打开，应核查该工作区实际生效的设置与所选解释器。

在本目录的终端中，可以直接运行 `/usr/local/bin/python3 main.py`，文件名无需嵌套两层引号。
