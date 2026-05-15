//
//  main.c
//  4_bct_4
//
//  Created by 张佳伟 on 2025/10/28.
//

#include <stdio.h>

int main()
{
    int shuru , i1 ,i2 , i3 , i4 , i5 ;
    
    printf("请输入一个介于0到32767的数：");
    scanf("%d",&shuru);
    
    i5 = shuru % 8 ;
    i4 = shuru / 8 % 8 ;
    i3 = shuru / 8 / 8 % 8 ;
    i2 = shuru / 8 / 8 / 8 % 8 ;
    i1 = shuru / 8 / 8 / 8 / 8 % 8 ;
    
    printf("八进制为%d%d%d%d%d\n", i1 , i2 , i3 , i4 , i5 );
    
    return 0;
}
