//
//  main.c
//  6_bct_11
//
//  Created by 张佳伟 on 2025/11/11.
//

#include <stdio.h>

int main()
{
    int n;
    printf("Enter the value of n: ");
    scanf("%d", &n);

    double sum = 1.0;
    double term = 1.0;

    for (int i = 1; i <= n; i++) {

        term = term / i;
        
        sum = sum + term;
    }

    printf("The approximate value of e is: %lf\n", sum);
    return 0;
}
