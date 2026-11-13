"""运行讲义示例、五组对照和测试，保存真实日志、图像及结果页面。"""

import argparse
from contextlib import redirect_stdout
from dataclasses import asdict
import html
from io import StringIO
import json
from pathlib import Path
import platform
import subprocess
import sys

from astar_search import GRAPH, POSITIONS, a_star_search, manhattan_heuristic


DEFAULT_OUTPUT = (Path.home() / "Library/CloudStorage/OneDrive-个人/资料/"
                  "人工智能专业导论/实验四/运行结果")


def networkx_graph(graph):
    import networkx as nx
    network = nx.Graph()
    network.add_nodes_from(graph)
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors:
            network.add_edge(node, neighbor, weight=weight)
    return network


def heuristic_check(graph, heuristic, goal):
    import networkx as nx
    distances = nx.single_source_dijkstra_path_length(networkx_graph(graph), goal)
    return {
        "distances": distances,
        "admissible": all(heuristic[n] <= distances[n] + 1e-10 for n in graph),
        "consistent": all(heuristic[n] <= w + heuristic[v] + 1e-10
                          for n, edges in graph.items() for v, w in edges),
    }


def draw_graph(ax, graph, title, heuristic=None, path=None, step=None):
    import networkx as nx
    network = networkx_graph(graph)
    colors = []
    for node in network:
        color = "#dcebf3"
        if step:
            if node in step["closed"]:
                color = "#d3d3d3"
            if node in step["open"]:
                color = "#ffe5a1"
            if node == step["current"]:
                color = "#f7a69e"
        elif path and node in path:
            color = "#f7c8c1"
        colors.append(color)
    nx.draw_networkx_edges(network, POSITIONS, ax=ax, edge_color="#888888", width=1.5)
    if path:
        nx.draw_networkx_edges(network, POSITIONS, ax=ax,
                               edgelist=list(zip(path, path[1:])),
                               edge_color="#b83a2c", width=3)
    nx.draw_networkx_nodes(network, POSITIONS, ax=ax, node_color=colors,
                           node_size=850, edgecolors="#555555", linewidths=0.8)
    nx.draw_networkx_labels(network, POSITIONS, ax=ax, font_size=13)
    nx.draw_networkx_edge_labels(network, POSITIONS, ax=ax,
                                 edge_labels=nx.get_edge_attributes(network, "weight"),
                                 font_size=11)
    if heuristic is not None:
        positions = {n: (x, y - 0.38) for n, (x, y) in POSITIONS.items()}
        nx.draw_networkx_labels(network, positions, ax=ax,
                                 labels={n: f"h={heuristic[n]:g}" for n in graph},
                                 font_size=11, font_color="#7b2d26")
    ax.set_title(title, fontsize=13, pad=12)
    ax.set_xlim(-0.65, 6.65)
    ax.set_ylim(0.3, 3.65)
    ax.axis("off")


def save_figures(output, cases, show):
    import matplotlib
    if not show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    available = {font.name for font in font_manager.fontManager.ttflist}
    chinese = next((font for font in ["Arial Unicode MS", "PingFang SC", "Heiti TC", "SimHei"]
                    if font in available), "DejaVu Sans")
    plt.rcParams["font.sans-serif"] = [chinese]
    plt.rcParams["axes.unicode_minus"] = False
    base = cases[0]
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 3.4))
    draw_graph(axes[0], GRAPH, "图结构与讲义曼哈顿启发值", heuristic=base["heuristic"])
    draw_graph(axes[1], GRAPH, "A* 返回路径　总代价 7", path=base["result"]["path"])
    fig.tight_layout()
    fig.savefig(output / "graph_and_path.png", dpi=200)
    fig2, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    for ax, index in zip(axes, [0, 2, 3]):
        step = base["result"]["steps"][index]
        draw_graph(ax, GRAPH, f"步骤 {step['step']}　当前 {step['current']}", step=step)
        ax.text(0.5, -0.02, "OPEN: " + ",".join(step["open"]) +
                "\nCLOSED: " + ",".join(step["closed"]),
                transform=ax.transAxes, ha="center", fontsize=10)
    fig2.tight_layout()
    fig2.savefig(output / "search_process.png", dpi=200)
    if show:
        plt.show()
    plt.close("all")


def write_result_pages(output, base_log, cases, tests):
    style = """<style>body{margin:24px;font:18px/1.5 -apple-system,'PingFang SC',sans-serif;color:#111}
    h1{font-size:24px;margin:0 0 14px}pre{font:17px/1.45 Menlo,'PingFang SC',monospace;
    margin:12px 0;white-space:pre-wrap}img{display:block;width:100%;max-width:1080px}
    table{border-collapse:collapse;width:100%;font-size:17px}th,td{padding:9px 12px;
    border:1px solid #bcbcbc;text-align:left}th{background:#f0f0f0}p{margin:12px 0}</style>"""
    start = '<!doctype html><html lang="zh-CN"><meta charset="utf-8">' + style
    baseline = (start + "<title>实验四 A* 实际运行结果</title><h1>实验四 A* 搜索运行结果</h1>"
                + "<pre>" + html.escape(base_log) + "</pre><img src='graph_and_path.png' "
                "alt='实际运行生成的图结构与路径'></html>")
    (output / "baseline.html").write_text(baseline, encoding="utf-8")
    rows = []
    for case in cases:
        r = case["result"]
        rows.append("<tr>" + "".join("<td>" + html.escape(str(value)) + "</td>" for value in
                    [case["name"], "→".join(r["path"]), r["cost"],
                     len(r["selected"]), r["expanded_count"],
                     "是" if case["optimal"] else "否"]) + "</tr>")
    test_summary = "\n".join(line for line in tests.splitlines()
                             if line.startswith("Ran ") or line == "OK")
    comparison = (start + "<title>实验四 对照实验实际结果</title><h1>思考题 对照实验结果</h1>"
                  "<table><thead><tr><th>实验条件</th><th>返回路径</th><th>代价</th>"
                  "<th>选取数</th><th>展开数</th><th>最优</th></tr></thead><tbody>"
                  + "".join(rows) + "</tbody></table>"
                  "<p>选取数包含目标；展开数只统计遍历邻居的次数。"
                  "最优性由 NetworkX Dijkstra 计算的最短代价核对。</p>"
                  "<pre>" + html.escape(test_summary) + "</pre></html>")
    (output / "comparison.html").write_text(comparison, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--show", action="store_true", help="保存图片后显示绘图窗口")
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    modified = {n: [(v, 8 if {n, v} == {"C", "D"} else w) for v, w in edges]
                for n, edges in GRAPH.items()}
    definitions = [("讲义曼哈顿", GRAPH, 1), ("零启发", GRAPH, 0),
                   ("1/3 曼哈顿", GRAPH, 1 / 3), ("2 倍曼哈顿", GRAPH, 2),
                   ("C-D 权重改为 8", modified, 1)]
    cases = []
    for name, graph, scale in definitions:
        heuristic = manhattan_heuristic(POSITIONS, "E", scale)
        result = a_star_search(graph, "A", "E", heuristic)
        check = heuristic_check(graph, heuristic, "E")
        cases.append({"name": name, "graph": graph, "heuristic": heuristic,
                      "result": asdict(result), "check": check,
                      "optimal": result.cost == check["distances"]["A"]})
    base = cases[0]
    stream = StringIO()
    with redirect_stdout(stream):
        print(f"Python {platform.python_version()} | {platform.system()} {platform.machine()}")
        print("起点 A，目标 E；同 f 按节点名称排序")
        print("h =", base["heuristic"])
        for step in base["result"]["steps"]:
            print(f"步骤 {step['step']}: {step['current']}  g={step['g']:g}  "
                  f"h={step['h']:g}  f={step['f']:g}  "
                  f"OPEN={','.join(step['open']) or '-'}  CLOSED={','.join(step['closed']) or '-'}")
        print("返回路径:", " -> ".join(base["result"]["path"]))
        print(f"总代价: {base['result']['cost']}；选取节点: {len(base['result']['selected'])}；"
              f"实际展开: {base['result']['expanded_count']}")
        print("启发值检查: h(C)=5 > 最短剩余代价 4，本例仍返回最优路径")
    base_log = stream.getvalue()
    tests = subprocess.run([sys.executable, "-m", "unittest", "-v", "test_astar_search"],
                           cwd=Path(__file__).resolve().parent, capture_output=True, text=True)
    test_log = tests.stdout + tests.stderr
    (output / "tests.txt").write_text(test_log, encoding="utf-8")
    if tests.returncode:
        print(test_log)
        raise SystemExit(tests.returncode)
    save_figures(output, cases, args.show)
    write_result_pages(output, base_log, cases, test_log)
    report = {"environment": {"python": platform.python_version(),
                               "system": platform.system(), "machine": platform.machine()},
              "cases": cases, "test_exit_code": tests.returncode}
    (output / "results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [base_log, "\n对照实验："]
    for case in cases:
        r = case["result"]
        lines.append(f"{case['name']}: {' -> '.join(r['path'])}; 代价={r['cost']}; "
                     f"选取={len(r['selected'])}; 展开={r['expanded_count']}; 最优={case['optimal']}")
    log = "\n".join(lines) + "\n\n" + test_log
    (output / "console.txt").write_text(log, encoding="utf-8")
    print(log)
    print("结果目录:", output)


if __name__ == "__main__":
    main()
