//
//  main.c
//  6_bct_3
//
//  Created by 张佳伟 on 2025/11/7.
//

#include <stdio.h>

int main()
{
    int fenzi , fenmu , a , b , r , fengzi2 , fenmu2;
    
    printf("请输入一个分数：");
    scanf("%d/%d",&fenzi,&fenmu);
    
    a = fenzi;
    b = fenmu;
    
    do {
        r = a % b ;
        a = b ;
        b = r ;
    } while (r != 0);
    
    fengzi2 = fenzi / a ;
    fenmu2 = fenmu / a ;
    
    printf("最简式为：%d/%d\n",fengzi2,fenmu2);
    return 0;
}
