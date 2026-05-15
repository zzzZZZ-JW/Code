//
//  main.c
//  find_max
//
//  Created by 张佳伟 on 2025/12/12.
//

#include <stdlib.h>
#include <stdio.h>

int find_max(int *arr , int size , int *max_index){
    int max = *arr;
    *max_index = 0;
    for (int *p = arr; p < arr + size; p++) {
        if (*p > max) {
            max = *p;
            *max_index = p - arr;
        }
    }
    return max;
}

int main(void){
    int input[10] = {1,2,3,4,5,6,7,8,9,10};
    int index;
    int temp;
    for (int i = 0; i < 10; i++) {
        find_max(input + i, 10 - i , &index);
        temp = input[i];
        input[i] = input[index + i];
        input[index + i] = temp;
    }
    for (int j = 0; j < 10; j++) {
        printf("%d,",input[j]);
    }
    printf("\n");
    return 0;
}
