//
//  main.c
//  10_lxt_8
//
//  Created by 张佳伟 on 2025/12/18.
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
    int arr[] = {1,2,3,4,5,6,7,8,9};
    int size = 9;
    int max_index;
    int max = find_max(arr, size, &max_index);
    printf("最大值为: %d\n", max);
    return 0;
}
