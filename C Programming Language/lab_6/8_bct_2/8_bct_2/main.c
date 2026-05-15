//
//  main.c
//  8_bct_2
//
//  Created by 张佳伟 on 2025/11/14.
//

#include <stdbool.h>
#include <stdio.h>

int main(void)
{
    int count[10] = {0};
    int shu[10] = {0,1,2,3,4,5,6,7,8,9};
    int digit;
    long n;
    
    printf("请输入一串数字: ");
    scanf("%ld", &n);
    
    while (n > 0) {
        digit = n % 10;
        count[digit] = count[digit] + 1;
        n /= 10;
    }

    for (int i = 0; i < 10; i++) {
        printf("%d ",shu[i]);
    }
    
    printf("\n");

    for (int i = 0; i < 10; i ++) {
        printf("%d ",count[i]);
    }
    
    printf("\n");
    
    return 0;
}
