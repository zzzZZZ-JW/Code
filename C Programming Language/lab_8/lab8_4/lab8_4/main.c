//
//  main.c
//  lab8_4
//
//  Created by 张佳伟 on 2025/11/29.
//

#include <stdlib.h>
#include <stdio.h>

int sum(int num) {
    static int total = 0;
    total = total + num;
    return total;
}

int main(void) {
    int n , num , result;
    
    printf("请输入整数n：");
    scanf("%d", &n);
    printf("请输入%d个整数：", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &num);
        result = sum(num);
        printf("%d\n", result);
    }
    
    return 0;
}
