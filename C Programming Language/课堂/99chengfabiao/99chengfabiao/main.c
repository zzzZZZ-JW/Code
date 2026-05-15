//
//  main.c
//  99chengfabiao
//
//  Created by 张佳伟 on 2025/10/31.
//

#include <stdio.h>

int main()
{
    int result ;
    for (int a = 1; a <= 9; a = a + 1) {
        for (int b = 1; b <= a; b = b + 1) {
            result = a * b;
            printf("%d*%d=%d ",a,b,result);
        }
        printf("\n");
    }
}
