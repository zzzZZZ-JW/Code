//
//  main.c
//  9_lxt_10
//
//  Created by 张佳伟 on 2025/11/27.
//

#include <stdio.h>

int hanshhu_a(int a[], int n) {
    int max = a[0];
    for (int i = 1; i < n; i++) {
        if (a[i] > max) {
            max = a[i];
        }
    }
    return max;
}

double hanshu_b(int a[], int n) {
    int sum = 0;
    double average;
    for (int i = 0; i < n; i++) {
        sum = sum + a[i];
    }
    average = sum / n;
    return average ;
}

int hanshu_c(int a[], int n) {
    int count = 0;
    for (int i = 0; i < n; i++) {
        if (a[i] > 0) {
            count++;
        }
    }
    return count;
}
