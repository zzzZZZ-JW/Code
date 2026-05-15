//
//  main.c
//  9_lxt_3
//
//  Created by 张佳伟 on 2025/11/21.
//

#include <stdio.h>

int gcd(int a , int b , int r){
    
    do {
        r = a % b ;
        a = b ;
        b = r ;
    } while (r != 0);
    
    return a;
}
