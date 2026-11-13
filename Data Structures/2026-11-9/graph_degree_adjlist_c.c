#include <stdio.h>
#include <stdlib.h>

#define MaxVNum 100

/* 邻接表的边结点：邻接城市编号、铁路权值、下一条边。 */
typedef struct EdgeNode {
    int adjvex;
    float weight;
    struct EdgeNode *next;
} EdgeNode;

float G[MaxVNum][MaxVNum];
int n = 14, e = 23;
float W[23] = {39.5, 19.5, 19.5, 29.5, 29.5, 62, 34.5, 24.5,
               37.5, 56.5, 62.5, 92, 46.5, 38.5, 34.5, 56.5,
               88.5, 26.5, 57.5, 71, 43.5, 31.5, 52};
int E[][2] = {{1,2},{2,3},{3,4},{4,14},{14,5},{1,9},{9,8},
              {8,7},{7,5},{9,2},{2,12},{12,13},{2,10},{1,12},
              {12,11},{8,3},{5,10},{10,11},{5,6},{11,13},{6,7},
              {7,14},{3,10}};

/* 释放各城市对应的链表。 */
void freeAdjList(EdgeNode *adjList[]) {
    int i;
    for (i = 1; i <= n; i++) {
        EdgeNode *p = adjList[i];
        while (p != NULL) {
            EdgeNode *next = p->next;
            free(p);
            p = next;
        }
        adjList[i] = NULL;
    }
}

int main(void) {
    int i, j, k;
    EdgeNode *adjList[MaxVNum] = {NULL};
    int inDegree[MaxVNum] = {0};
    int outDegree[MaxVNum] = {0};

    /* -1 表示没有直达铁路；第 0 行和第 0 列不使用。 */
    for (i = 1; i <= n; i++) {
        for (j = 1; j <= n; j++) {
            G[i][j] = (i == j) ? 0.0f : -1.0f;
        }
    }

    /* 第 k 条边对应第 k 个权值；无向网络需要对称赋值。 */
    for (k = 0; k < e; k++) {
        i = E[k][0];
        j = E[k][1];
        G[i][j] = G[j][i] = W[k];
    }

    /* 输出带权邻接矩阵，行和列均依次对应城市 1～14。 */
    for (i = 1; i <= n; i++) {
        for (j = 1; j <= n; j++) {
            if (G[i][j] == -1.0f) {
                printf("%6d", -1);
            } else {
                printf("%6.1f", G[i][j]);
            }
            printf("%s", j == n ? "\n" : " ");
        }
    }

    /* 从矩阵构造邻接表，尾插法使邻接城市按编号升序排列。 */
    for (i = 1; i <= n; i++) {
        EdgeNode *tail = NULL;
        for (j = 1; j <= n; j++) {
            if (i != j && G[i][j] != -1.0f) {
                EdgeNode *node = malloc(sizeof(EdgeNode));
                if (node == NULL) {
                    fprintf(stderr, "邻接表内存分配失败。\n");
                    freeAdjList(adjList);
                    return EXIT_FAILURE;
                }
                node->adjvex = j;
                node->weight = G[i][j];
                node->next = NULL;
                if (tail == NULL) {
                    adjList[i] = node;
                } else {
                    tail->next = node;
                }
                tail = node;

                /* 无向边按两个方向记录，入度数列、出度数行。 */
                outDegree[i]++;
                inDegree[j]++;
            }
        }
    }

    printf("\n顶点度数（无向图按双向边表示，入度 = 出度 = 度数）：\n");
    printf("城市  入度  出度  度数\n");
    for (i = 1; i <= n; i++) {
        int degree = 0;
        EdgeNode *p;
        for (p = adjList[i]; p != NULL; p = p->next) {
            degree++;
        }
        printf("%4d  %4d  %4d  %4d\n", i, inDegree[i], outDegree[i], degree);
    }

    printf("\n带权邻接表（邻接城市, 权值）：\n");
    for (i = 1; i <= n; i++) {
        EdgeNode *p;
        printf("%2d", i);
        for (p = adjList[i]; p != NULL; p = p->next) {
            printf(" -> (%d, %.1f)", p->adjvex, p->weight);
        }
        printf(" -> NULL\n");
    }

    freeAdjList(adjList);
    return 0;
}
