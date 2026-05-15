//
//  main.c
//  递归_阶乘
//
//  Created by 张佳伟 on 2025/11/28.
//

#include <stdio.h>

int Fact(int n){
    if (n == 0 || n == 1) {
        return n ;
    }
    return n*Fact(n-1);
}
