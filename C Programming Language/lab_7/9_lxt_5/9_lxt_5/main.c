//
//  main.c
//  9_lxt_5
//
//  Created by 张佳伟 on 2025/11/21.
//

#include <stdio.h>

int num_digits(int n){
    int digits = 0;
    
    do {
        n = n / 10;
        digits++;
    } while (n > 0);
    
    return digits;
}
