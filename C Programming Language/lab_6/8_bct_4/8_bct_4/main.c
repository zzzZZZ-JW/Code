//
//  main.c
//  8_bct_4
//
//  Created by 张佳伟 on 2025/11/17.
//

#include <stdio.h>
#define N 10

int main()
{
    int a[N], i;
    
    printf("Enter %d numbers: ", (int)(sizeof(a)/sizeof(a[0])));
    
    for (i = 0; i < (int)(sizeof(a)/sizeof(a[0])); i++)
    scanf("%d", &a[i]);
    printf("In reverse order:");
    
    for (i = (int)(sizeof(a)/sizeof(a[0])) - 1; i >= 0; i--)
    printf(" %d", a[i]);
    printf("\n");
    
    return 0;
}
