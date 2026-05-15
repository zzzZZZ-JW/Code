//
//  main.c
//  while
//
//  Created by 张佳伟 on 2025/10/31.
//

#include <stdio.h>

int main()
{
    int num ;
    
    printf("请输入一个正整数");
    scanf("%d",&num) ;
    
    do {
        printf("输入错误，请重新输入正整数");
        scanf("%d",&num) ;
    } while (num > 0);
    
    return 0;
}
