//
//  main.c
//  递归_反转字符串
//
//  Created by 张佳伟 on 2025/11/28.
//

#include <stdio.h>

void reverse(char a[], int left, int right) {
    if (left >= right) {
        return;
    }else{
        char temp = a[left];
        a[left] = a[right];
        a[right] = temp;
        
        reverse(a, left + 1, right - 1);
        return;
    }
}
