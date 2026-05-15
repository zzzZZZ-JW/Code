//
//  main.c
//  4_bct_1
//
//  Created by 张佳伟 on 2025/10/26.
//

#include <stdio.h>

int main()
{
    int num , shi ,ge ;
    
    printf("请输入一个两位数：");
    scanf("%d",&num);
    
    shi = num / 10 ;
    ge = num % 10 ;
    
    printf("逆序为：%d%d\n",ge,shi);
    
    return 0;
}
