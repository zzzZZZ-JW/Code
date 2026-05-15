//
//  main.c
//  bct_5
//
//  Created by 张佳伟 on 2025/10/19.
//

#include <stdio.h>

int main()
{
    int x;
    int result;
    
    printf("请输入一个x的值：");
    scanf("%d",&x);
    
    result = ( 3 * x * x * x * x * x ) + ( 2 * x * x * x * x ) - ( 5 * x * x * x ) - ( x * x ) + ( 7 * x) - 6;
    
    printf("多项式的值为：%d\n",result);
    
    return 0;
}
