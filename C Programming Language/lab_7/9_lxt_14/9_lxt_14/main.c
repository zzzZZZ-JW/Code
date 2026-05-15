//
//  main.c
//  9_lxt_14
//
//  Created by 张佳伟 on 2025/11/28.
//

#include <stdio.h>
#include <stdbool.h>

bool has_zero(int a[], int n)
{
    int i;
    for (i = 0; i < n; i++)
        if (a[i] == 0)
            return true;
    return false;
}
