//
//  main.c
//  数组求和
//
//  Created by 张佳伟 on 2025/11/14.
//

#include <stdio.h>

int main()
{
    int score[3][4];
    int sum[3]={0};
    
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 4; j++) {
            sum[i] = sum[i] + score[i][j];
        }
    }
    
    return 0;
}
