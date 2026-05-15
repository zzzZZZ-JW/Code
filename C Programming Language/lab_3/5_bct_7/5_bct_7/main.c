//
//  main.c
//  5_bct_7
//
//  Created by 张佳伟 on 2025/10/29.
//

#include <stdio.h>

int main()
{
    int n1 , n2 , n3 , n4 , max , min ;
    
    printf("请输入4个整数：");
    scanf("%d %d %d %d",&n1,&n2,&n3,&n4);
    
    if (n1 > n2) {
        max = n1 ;
        min = n2 ;
    }else {
        max = n2 ;
        min = n1 ;
    }
    
    if (n3 > max) {
        max = n3 ;
    }else if (n3 < min) {
        min = n3 ;
    }
    if (n4 > max) {
        max = n4 ;
    }else if (n4 < min) {
        min = n4 ;
    }
    printf("最大值为：%d \n",max);
    printf("最小值为：%d \n",min);
    
    return 0;
}
