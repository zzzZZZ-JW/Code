//
//  main.c
//  6_bct_1
//
//  Created by 张佳伟 on 2025/10/31.
//

#include <stdio.h>

int main()
{
    double num , max = 0;
    
    printf("请输入一个数：");
    scanf("%lf",&num);
    
    max = num ;
    
    while (num > 0) {
        printf("请输入一个数：");
        scanf("%lf",&num);
        
        if (num <= 0) {
            break;
        }
        
        if (num > max) {
            max = num ;
        }
    }
    printf("最大的数是：%.2f\n",max);
    
    return 0;
}
