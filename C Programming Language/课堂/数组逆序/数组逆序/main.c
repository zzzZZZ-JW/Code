//
//  main.c
//  数组逆序
//
//  Created by 张佳伟 on 2025/11/14.
//

#include <stdio.h>

int main()
{
    int numbers[6] = {1, 2, 3, 4, 5, 6};
    int temp;
    
    for (int i = 0; i < 6/2; i++) {
        temp = numbers[i];
        numbers[i] = numbers[6-1-i];
        numbers[6-1-i] = temp;
    }
    
    for (int i = 0; i < 6; i++) {
        printf("%d ", numbers[i]);
    }
    
    return 0;
}
