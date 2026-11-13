# 实验四 搜索算法实现

按实验四讲义实现 A*，完成图结构与启发值展示、路径回溯、真实搜索过程图，以及修改启发函数和边权的思考题。

## 运行

本机已有 Anaconda 环境包含所需依赖：Python 3.13.9、Matplotlib 3.10.6、NetworkX 3.5。

```zsh
cd "/Users/zhangjiawei/Class Code/Introduction to AI/lab4"
/opt/anaconda3/bin/python run_experiment.py
```

默认输出到 [课程资料目录中的运行结果](/Users/zhangjiawei/Library/CloudStorage/OneDrive-个人/资料/人工智能专业导论/实验四/运行结果)，包括 `console.txt`、`tests.txt`、`results.json`、两张程序生成的 PNG，以及 `baseline.html`、`comparison.html` 结果页面。添加 `--show` 显示绘图窗口；添加 `--output "/自选目录"` 可更改输出位置。

单独运行测试：

```zsh
/opt/anaconda3/bin/python -m unittest -v test_astar_search
```

核心算法只使用标准库；绘图和独立最短代价核对需要 `requirements.txt` 中的依赖。

## 文件与算法约定

- `astar_search.py`：图、坐标、曼哈顿启发函数及 A* 核心。边权有限且非负，目标启发值为0；发现更低代价时重开节点，并跳过旧堆条目。同 f 按节点名称排序。
- `run_experiment.py`：五组对照、NetworkX Dijkstra 核对、真实过程图和测试日志。
- `test_astar_search.py`：8项行为测试，包含不可达、起终点相同、重开节点和高估反例等。
- `build_report.py`：按原模板和上述结果生成 Word 完成版。使用 Codex 文档运行时执行；依赖结果目录中的两张实际浏览器截图，不会自行生成或伪造截图。

`selected` 包含最终选取的目标，`expanded_count` 只统计实际遍历邻居的次数。堆里跳过的旧条目不计入这两项。

## 已验证结果

| 条件 | 路径 | 代价 | 选取数 | 展开数 | 相对当前图是否最优 |
| --- | --- | ---: | ---: | ---: | --- |
| 原曼哈顿 | A→B→C→D→E | 7 | 5 | 4 | 是 |
| 零启发 | A→B→C→D→E | 7 | 5 | 4 | 是 |
| 1/3曼哈顿 | A→B→C→D→E | 7 | 5 | 4 | 是 |
| 2倍曼哈顿 | A→B→D→E | 9 | 4 | 3 | 否 |
| C—D权重改为8 | A→B→D→E | 9 | 5 | 4 | 是 |

讲义原启发值 h(C)=5 大于真实剩余代价4，因此不可采纳；本次原例恰好找到最优解。1/3曼哈顿满足一致性，但本图中并未减少搜索节点数。2倍曼哈顿展示高估可能返回次优路径。原讲义首节点 f=0 改为 h(A)=6，并补齐旧堆条目过滤、节点重开和真实搜索步骤返回。

## 报告与记录

原讲义和已填个人信息的模板均保留；报告另存为 [实验四完成版](/Users/zhangjiawei/Library/CloudStorage/OneDrive-个人/资料/人工智能专业导论/实验四/2506456052-张佳伟-实验四-完成版.docx)。模板中误留的“实验三 数组和循环”已更正。报告使用实际浏览器截图和程序图像，模板元数据、节属性、页脚、编号及样式包部件保持不变。文档构建约定和内部渲染结果在资料根目录的 `.codex-lab4`。

2026-11-13：完成程序、五组对照和8项测试；截图通过本地 Chrome 无头模式渲染实际结果页面取得。只完成本地代码和报告，未提交、推送或向课程平台上传。

报告验收：完成版共4页，已完成逐页渲染检查和模板差异核对；截图完整、中文可读、页码正确，无手动分页。原模板与元数据保持不变。
