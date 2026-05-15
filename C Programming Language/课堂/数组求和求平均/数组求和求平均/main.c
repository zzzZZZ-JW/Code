//
//  main.c
//  数组求和求平均
//
//  Created by 张佳伟 on 2025/11/14.
//

#include <stdio.h>

int main()
{
    int score[3][4];
    int sum;
    int average;
    int sum;
    
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 3; j++) {
            sum = sum + score[i][j];
            average = sum / 3 ;
        }
    }
    average = sum / 12;
    return 0;
}
