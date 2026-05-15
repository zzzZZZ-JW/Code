//
//  main.c
//  素数判断
//
//  Created by 张佳伟 on 2025/11/7.
//

#include<stdio.h>

int main()
{
    int num;
    printf("请输入一个自然数:");
    scanf("%d",&num);

    if (num < 2) {
        printf("%d不是素数\n", num);
        return 0;
    }

    int i;
    
    for(i = 2; i < num; i++){
        if(num % i == 0){
            printf("%d不是素数\n", num);
            break;
        }
    }

    if (i == num) {
        printf("%d是素数\n", num);
    }

    return 0;
}
