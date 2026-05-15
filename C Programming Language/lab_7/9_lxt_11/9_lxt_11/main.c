//
//  main.c
//  9_lxt_11
//
//  Created by 张佳伟 on 2025/11/27.
//

#include <stdio.h>
#define A 4
#define B 3
#define C 2
#define D 1
#define E 0

float computer_GPA(char grades[] , int n){
    int sum = 0;
    double average ;
    for (int i = 0; i < n; i++) {
        sum = sum + grades[i];
    }
    average = sum / n ;
    return average;
}
