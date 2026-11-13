"""通过返回路径与代价验证算法，不依赖堆等内部实现。"""

import math
import unittest

from astar_search import GRAPH, POSITIONS, a_star_search, manhattan_heuristic


class SearchTests(unittest.TestCase):
    def test_handout_example(self):
        result = a_star_search(GRAPH, "A", "E", manhattan_heuristic(POSITIONS, "E"))
        self.assertEqual(result.path, ["A", "B", "C", "D", "E"])
        self.assertEqual(result.cost, 7)

    def test_start_is_goal(self):
        result = a_star_search(GRAPH, "E", "E", {n: 0 for n in GRAPH})
        self.assertEqual((result.path, result.cost), (["E"], 0))
        self.assertEqual(result.expanded_count, 0)

    def test_unreachable_goal(self):
        graph = {"S": [("A", 1)], "A": [], "G": []}
        result = a_star_search(graph, "S", "G", {n: 0 for n in graph})
        self.assertIsNone(result.path)
        self.assertTrue(math.isinf(result.cost))

    def test_admissible_inconsistent_heuristic_reopens_node(self):
        # 最优 S-B-A-G=1+1+3=5；若 A 关闭后不重开，将错误返回 6。
        graph = {"S": [("A", 3), ("B", 1)], "A": [("G", 3)],
                 "B": [("A", 1)], "G": []}
        result = a_star_search(graph, "S", "G", {"S": 5, "A": 0, "B": 4, "G": 0})
        self.assertEqual(result.path, ["S", "B", "A", "G"])
        self.assertEqual(result.cost, 5)

    def test_stale_entry_does_not_repeat_expansion(self):
        # A 的旧条目在到达 G 前弹出，应跳过，不再次展开 A。
        graph = {"S": [("A", 8), ("B", 1)], "B": [("A", 1)],
                 "A": [("G", 20)], "G": []}
        result = a_star_search(graph, "S", "G", {n: 0 for n in graph})
        self.assertEqual(result.path, ["S", "B", "A", "G"])
        self.assertEqual(result.cost, 22)
        self.assertEqual(result.expanded_count, 3)

    def test_overestimate_can_return_suboptimal_path(self):
        result = a_star_search(GRAPH, "A", "E", manhattan_heuristic(POSITIONS, "E", 2))
        self.assertEqual((result.path, result.cost), (["A", "B", "D", "E"], 9))

    def test_changed_edge_weight(self):
        graph = {n: [(v, 8 if {n, v} == {"C", "D"} else w) for v, w in edges]
                 for n, edges in GRAPH.items()}
        result = a_star_search(graph, "A", "E", manhattan_heuristic(POSITIONS, "E"))
        self.assertEqual((result.path, result.cost), (["A", "B", "D", "E"], 9))

    def test_negative_edge_is_rejected(self):
        with self.assertRaises(ValueError):
            a_star_search({"S": [("G", -1)], "G": []}, "S", "G", {"S": 0, "G": 0})


if __name__ == "__main__":
    unittest.main(verbosity=2)
