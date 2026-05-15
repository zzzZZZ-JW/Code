//
//  main.c
//  n_jiecheng
//
//  Created by 张佳伟 on 2025/10/31.
//

#include <stdio.h>

int main()
{
    int n , result ;
    printf("请输入需要求阶乘的数：");
    scanf("%d",&n) ;
    for (int i = 1 ; i <= n ; i = i + 1) {
        result = result * i ;
    }
    printf("%d \n",result);
    return 0;
}
