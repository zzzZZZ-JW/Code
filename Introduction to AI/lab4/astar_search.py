"""实验四：A* 搜索。核心算法仅依赖 Python 标准库。"""

from dataclasses import dataclass, field
import heapq
import math


GRAPH = {
    "A": [("B", 1), ("C", 4)],
    "B": [("A", 1), ("C", 2), ("D", 5)],
    "C": [("A", 4), ("B", 2), ("D", 1)],
    "D": [("B", 5), ("C", 1), ("E", 3)],
    "E": [("D", 3)],
}
POSITIONS = {"A": (0, 2), "B": (2, 3), "C": (2, 1),
             "D": (4, 2), "E": (6, 2)}


def manhattan_heuristic(positions, goal, scale=1):
    """绘图距离本身不保证可采纳；缩放尺度需与边权核对。"""
    gx, gy = positions[goal]
    return {node: scale * (abs(x - gx) + abs(y - gy))
            for node, (x, y) in positions.items()}


@dataclass
class SearchResult:
    path: list | None = None
    cost: float = math.inf
    selected: list = field(default_factory=list)
    steps: list = field(default_factory=list)
    expanded_count: int = 0
    skipped_entries: int = 0


def a_star_search(graph, start, goal, heuristic):
    """边权非负；h 可采纳且目标 h=0 时，重开节点可保证最优性。

    堆按 (f, 节点名, 入堆时的 g) 排序，同 f 时按节点名排序。
    selected 包括目标；expanded_count 仅统计实际遍历邻居的次数。
    """
    if start not in graph or goal not in graph:
        raise ValueError("起点和终点必须在图中")
    for node, neighbors in graph.items():
        if node not in heuristic or not math.isfinite(heuristic[node]) or heuristic[node] < 0:
            raise ValueError("每个节点都需要有限且非负的启发值")
        for neighbor, weight in neighbors:
            if neighbor not in graph or not math.isfinite(weight) or weight < 0:
                raise ValueError("邻居必须存在，且边权必须有限、非负")
    if heuristic[goal] != 0:
        raise ValueError("目标节点的启发值必须为 0")

    open_heap = [(heuristic[start], start, 0)]
    g = {node: math.inf for node in graph}
    g[start] = 0
    parent, closed = {}, set()
    result = SearchResult()
    while open_heap:
        current_f, current, queued_g = heapq.heappop(open_heap)
        if queued_g != g[current] or current in closed:
            result.skipped_entries += 1
            continue  # 跳过旧代价对应的过期堆条目
        result.selected.append(current)
        updates = []
        if current == goal:
            path = [goal]
            while path[-1] != start:
                path.append(parent[path[-1]])
            result.path, result.cost = path[::-1], g[goal]
        else:
            closed.add(current)
            result.expanded_count += 1
            for neighbor, weight in graph[current]:
                new_g = g[current] + weight
                if new_g < g[neighbor]:
                    g[neighbor], parent[neighbor] = new_g, current
                    reopened = neighbor in closed
                    closed.discard(neighbor)  # 更优路线允许重新打开节点
                    heapq.heappush(open_heap,
                                   (new_g + heuristic[neighbor], neighbor, new_g))
                    updates.append({"node": neighbor, "g": new_g,
                                    "h": heuristic[neighbor],
                                    "f": new_g + heuristic[neighbor],
                                    "reopened": reopened})
        # 用有效堆条目记录真正的 OPEN，过滤过期条目后按 f 排序。
        frontier = sorted((f, n, cost) for f, n, cost in open_heap
                          if cost == g[n] and n not in closed)
        result.steps.append({"step": len(result.selected), "current": current,
                             "g": g[current], "h": heuristic[current],
                             "f": current_f, "open": [n for _, n, _ in frontier],
                             "closed": sorted(closed), "updates": updates,
                             "goal": current == goal})
        if current == goal:
            return result
    return result
