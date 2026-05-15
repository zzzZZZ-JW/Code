//
//  main.c
//  基础数学函数
//
//  Created by 张佳伟 on 2025/11/21.
//

#include <stdio.h>

int maximum(int a, int b) {
    int max;
    if (a > b) {
        max = a;
    } else {
        max = b;
    }
    return max;
}

int minimun(int a,int b){
    int min;
    if (a > b) {
        min = b ;
    }else{
        min = a ;
    }
    return min;
}

int abs(int x){
    if (x < 0) {
        return -x;
    }else{
        return x;
    }
}
