//
//  main.c
//  10_lxt_7
//
//  Created by 张佳伟 on 2025/12/18.
//

#include <stdlib.h>
#include <stdio.h>

void split_date(int day_of_year, int year, int *month, int *day) {
    int days_in_month[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    

