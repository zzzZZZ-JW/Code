//
//  main.c
//  5_bct_10
//
//  Created by 张佳伟 on 2025/10/31.
//

#include <stdio.h>

int main()
{
    int chengji , dengji ;
    
    printf("请输入成绩：");
    scanf("%d",&chengji);
    
    if (chengji >= 90 && chengji <= 100) {
        dengji = 1;
    }else if (chengji >= 80 && chengji < 90) {
        dengji = 2;
    }else if (chengji >= 70 && chengji < 80) {
        dengji = 3;
    }else if (chengji >= 60 && chengji < 70) {
        dengji = 4;
    }else if (chengji >= 0 && chengji < 60) {
        dengji = 5;
    }
    
    switch (dengji) {
        case 1:
            printf("等级为A \n");
            break;
        case 2:
            printf("等级为B \n");
            break;
        case 3:
            printf("等级为C \n");
            break;
        case 4:
            printf("等级为D \n");
            break;
        case 5:
            printf("等级为E \n");
            break;
        default:
            break;
    }
    
    return 0;
}
