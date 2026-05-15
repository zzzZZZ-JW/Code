//
//  main.c
//  4_bct_3
//
//  Created by 张佳伟 on 2025/10/26.
//

#include <stdio.h>

int main()
{
    int i1 , i2 , i3 ;
    
    printf("请输入一个三位数：");
    scanf("%1d%1d%1d",&i1,&i2,&i3);
    
    printf("逆序为：%d%d%d\n",i3,i2,i1);
    
    return 0;
}
