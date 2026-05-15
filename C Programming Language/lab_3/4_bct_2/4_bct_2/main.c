//
//  main.c
//  4_bct_2
//
//  Created by 张佳伟 on 2025/10/26.
//

#include <stdio.h>

int main()
{
    int num , bai , shi , ge ;
    
    printf("请输入一个三位数：");
    scanf("%d",&num);
    
    bai = num / 100;
    
    num = num - bai*100 ;
    
    shi = num / 10 ;
    ge = num % 10 ;
    
    printf("逆序为：%d%d%d\n",ge,shi,bai);

    return 0;
}
