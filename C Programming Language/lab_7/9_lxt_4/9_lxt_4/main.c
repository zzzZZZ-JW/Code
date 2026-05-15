//
//  main.c
//  9_lxt_4
//
//  Created by 张佳伟 on 2025/11/21.
//

#include <stdio.h>

int day_of_year(int month , int day , int year){
    int result = 0;
    
    int yuetianshu[] = {0,31,28,31,30,31,30,31,31,30,31,30,31};
    
    for (int i = 0; i < month; i++) {
        result = result + yuetianshu[i];
    }
    result = result + day;
    
    return result;
}
