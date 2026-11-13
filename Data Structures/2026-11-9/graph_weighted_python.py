edge_list = [(1,2),(2,3),(3,4),(4,14),(14,5),(1,9),(9,8),
             (8,7),(7,5),(9,2),(2,12),(12,13),(2,10),(1,12),
             (12,11),(8,3),(5,10),(10,11),(5,6),(11,13),(6,7),
             (7,14),(3,10)]
weight_list = [39.5, 19.5, 19.5, 29.5, 29.5, 62, 34.5, 24.5,
               37.5, 56.5, 62.5, 92, 46.5, 38.5, 34.5, 56.5,
               88.5, 26.5, 57.5, 71, 43.5, 31.5, 52]
n_vertex, n_edge = 14, 23

# -1 表示两个城市之间没有直达铁路；第 0 行和第 0 列不使用。
G = [[-1] * (n_vertex + 1) for _ in range(n_vertex + 1)]
for i in range(1, n_vertex + 1):
    G[i][i] = 0.0

# 第 k 条边对应第 k 个权值；无向网络需要对称赋值。
for k in range(n_edge):
    i, j = edge_list[k]
    G[i][j] = G[j][i] = weight_list[k]

# 输出带权邻接矩阵，行和列均依次对应城市 1～14。
for i in range(1, n_vertex + 1):
    for j in range(1, n_vertex + 1):
        if G[i][j] == -1:
            print(f"{-1:6d}", end="")
        else:
            print(f"{G[i][j]:6.1f}", end="")
        print("\n" if j == n_vertex else " ", end="")
