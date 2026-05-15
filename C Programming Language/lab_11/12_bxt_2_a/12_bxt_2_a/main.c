//
//  main.c
//  12_bxt_2_a
//
//  Created by 张佳伟 on 2025/12/25.
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
    char new_message[100];

    for (int i = size - 1; i >= 0; i--)
    {
        new_message[size - 1 - i] = message[i];
    }
    
    for (int i = 0; i < size; i++)
    {
        if (new_message[i] != message[i])
        {
            printf("不是回文\n");
            return 0;
        }
        if (new_message[i] == message[i])
        {
            continue;
        }
    }
    printf("是回文\n");
    return 0;
}