//
//  main.c
//  xingsanjiao
//
//  Created by 张佳伟 on 2025/11/5.
//

#include <stdio.h>

int main() {
    int hang = 5;
    
    for(int i = 1; i <= hang; i++) {
        for(int j = 1; j <= hang - i; j++) {
            printf(" ");
        }
        
        for(int xing = 1; xing <= 2*i - 1; xing++) {
            printf("*");
        }
        
        printf("\n");
    }
    return 0;
}
