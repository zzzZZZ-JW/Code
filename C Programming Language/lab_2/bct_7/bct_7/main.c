//
//  main.c
//  bct_7
//
//  Created by 张佳伟 on 2025/10/19.
//

#include <stdio.h>

int main()
{
    int jine , ershi , shi , wu , yi;
    
    printf("输入美元金额：");
    scanf("%d",&jine);
    
    ershi = jine / 20 ;
    jine = jine - ershi * 20 ;
    
    shi = jine / 10 ;
    jine = jine - shi * 10 ;
    
    wu = jine / 5 ;
    jine = jine - wu * 5 ;
    
    yi = jine ;
    
    printf("最少需要%d张20美元\n%d张10美元\n%d张5美元\n%d张1美元\n",ershi,shi,wu,yi);
    
    return 0;
}
