//
//  main.c
//  5_bct_4
//
//  Created by 张佳伟 on 2025/10/29.
//

#include <stdio.h>

int main()
{
    int v ;
    
    printf("请输入风速（海里/小时）:");
    scanf("%d",&v);
    
    if (v < 1) {
        printf("对应的蒲福风级为：Calm（无风）\n");
    }else if (v <= 3) {
        printf("对应的蒲福风级为：Light air（轻风）\n");
    }else if (v <= 27) {
        printf("对应的蒲福风级为：Breeze（微风）\n");
    }else if (v <= 47) {
        printf("对应的蒲福风级为：Gale（大风）\n");
    }else if (v <= 63) {
        printf("对应的蒲福风级为：Storm（暴风）\n");
    }else {
        perror("对应的蒲福风级为：Hurricane（飓风）\n");
    }
    return 0;
}
