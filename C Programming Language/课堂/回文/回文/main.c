//
//  main.c
//  回文
//
//  Created by 张佳伟 on 2025/11/7.
//

#include <stdio.h>

int main()
{
    int num , d , result = 0;
    
    printf("请输入一个数：");
    scanf("%d",&num);
    
    while (num != 0) {
        d = num % 10 ;
        num = num / 10 ;
        result = result * 10 + d ;
    }
    
    printf("回文为：%d\n",result);
    
    return 0;
}
