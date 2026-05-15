//
//  main.c
//  sushushengcheng
//
//  Created by 张佳伟 on 2025/11/7.
//

#include <stdio.h>

int main()
{
    int num;
    int sum = 0 ;
    
    printf("请输入一个数：");
    scanf("%d", &num);
    
    for (int i = 2; i <= num; i++) {
        int isPrime = 1; // 假设当前数是素数
        
        // 内层循环检查i是否为素数
        for (int j = 2; j < i; j++) {
            if (i % j == 0) {
                isPrime = 0; // 如果能被整除，说明不是素数
                break;
            }
        }
        if (isPrime == 1) {
            sum = sum + 1;
        }
    }
    
    printf("%d以内的素数有%d个\n",num,sum);
    return 0;
}
