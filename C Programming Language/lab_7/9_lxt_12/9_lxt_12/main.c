//
//  main.c
//  9_lxt_12
//
//  Created by 张佳伟 on 2025/11/27.
//

#include <stdio.h>

double inner_product(double a[] , double b[] , int n){
    int sum = 0 ;
    for (int i = 0; i < n; i++) {
        sum = sum + a[i] * b[i] ;
    }
    return sum;
}
