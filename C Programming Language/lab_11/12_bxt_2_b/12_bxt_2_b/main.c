//
//  main.c
//  12_bxt_2_b
//
//  Created by 张佳伟 on 2025/12/25.
//

#include <stdio.h>

int main(void) {
    char message[100];
    char *p = message;

    printf("输入一条消息: ");
    for ( p ; p < message + 100; p++) {
        char ch = getchar();
        if (ch == '\n')
        {
            break;
        }
        *p = ch;
    }

    for ( p = p - 1 ; p >= message; p--) {
        putchar(*p);
    }
    printf("\n");
    return 0;
}
