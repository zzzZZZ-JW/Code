//
//  main.c
//  9_lxt_2
//
//  Created by 张佳伟 on 2025/11/21.
//

#include <stdio.h>

int check(int x , int y , int n){
    if (x > 0 && x < n-1 && y > 0 && y < n-1) {
        return 1;
    }else{
        return 0;
    }
}
