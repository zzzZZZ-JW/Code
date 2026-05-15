//
//  main.c
//  8_bct_3
//
//  Created by 张佳伟 on 2025/11/17.
//

#include <stdbool.h>
#include <stdio.h>

int main(void)
{
    bool digit_seen[10] = {false};
    int digit;
    long n , yuanshi;
    
    printf("Enter a number: ");
    scanf("%ld", &yuanshi);
    
    while (yuanshi > 0) {
        n = yuanshi;
        while (n > 0) {
            digit = n % 10;
            if (digit_seen[digit])
                break;
            digit_seen[digit] = true;
            n /= 10;
        }
        
        if (n > 0)
            printf("Repeated digit\n");
        else
            printf("No repeated digit\n");

        printf("Enter a number: ");
        scanf("%ld", &yuanshi);
    }
    
    return 0;
}
