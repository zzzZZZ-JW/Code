//
//  main.c
//  10_lxt_6
//
//  Created by 张佳伟 on 2025/12/18.
//

#include <stdlib.h>
#include <stdio.h>

void find_two_largest(int a[], int n, int *largest, int *second_largest) {
    *largest = a[0];
    *second_largest = a[1];
    
    for (int i = 2; i < n; i++) {
        if (a[i] > *largest) {
            *second_largest = *largest;
            *largest = a[i];
        } else if (a[i] > *second_largest & a[i] < *largest) {
            *second_largest = a[i];
        }
    }
}

int main(void){
    int a[] = {1,2,3,4,5,6,7,8,9};
    int n = 9;
    int largest, second_largest;
    
    find_two_largest(a, n, &largest, &second_largest);
    
    printf("最大值为: %d\n", largest);
    printf("第二大值为: %d\n", second_largest);
    
    return 0;
}
