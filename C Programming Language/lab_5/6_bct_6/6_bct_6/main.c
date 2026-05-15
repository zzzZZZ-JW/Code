//
//  main.c
//  6_bct_6
//
//  Created by 张佳伟 on 2025/11/7.
//

#include <stdio.h>

int main()
{
    int n , result ;
    
    printf("请输入一个数：");
    scanf("%d",&n);
    
    for (int i = 2; i * i <= n; i = i + 2) {
        result = i * i ;
        printf("%d\n",result);
    }
    return 0;
}
