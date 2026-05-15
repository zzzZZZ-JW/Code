//
//  main.c
//  9_lxt_6
//
//  Created by 张佳伟 on 2025/11/21.
//

#include <stdio.h>

int dight(int n , int k){
    int digit = 0;
    
    for (int i = 0; i < k; i++) {
        digit = n % 10;
        n = n / 10 ;
    }
    
    return digit;
}
