//
//  main.c
//  6_bct_12
//
//  Created by 张佳伟 on 2025/11/12.
//

#include <stdio.h>

int main()
{
    int n;
    printf("Enter the value of n: ");
    scanf("%d", &n);

    double sum = 1.0;
    double term = 1.0;
    double x;

    printf("Enter the value of x: ");
    scanf("%lf", &x);

    int i = 1;
    while (i <= n) {
        term = term / i;
        
        if (term >= x) {
            sum = sum + term;
            i = i + 1;
        } else {
            break;
        }
    }

    printf("The approximate value of e is: %lf\n", sum);
    return 0;
}
