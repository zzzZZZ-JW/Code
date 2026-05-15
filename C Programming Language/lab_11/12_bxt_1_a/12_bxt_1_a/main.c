//
//  main.c
//  12_bct_1_a
//
//  Created by 张佳伟 on 2025/12/19.
//

#include <stdio.h>

int main(void) {
    char message[100];
    int size = 0;
    printf("输入一条消息: ");
    for (int i = 0; i < 100; i++)
    {
        char ch = getchar();
        message[i] = ch;
        if (ch == '\n')
        {
            break;
        }
        size = size + 1;
    }

    for (int i = size - 1; i >= 0; i--)
    {
        printf("%c", message[i]);
    }
    printf("\n");
    return 0;
}

