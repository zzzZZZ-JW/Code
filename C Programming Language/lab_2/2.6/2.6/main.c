//
//  main.c
//  2.6
//
//  Created by 张佳伟 on 2025/10/17.
//

/* Converts a Fahrenheit temperature to Celsius */

#include <stdio.h>
#define FREEZING_PT 32.0f
#define SCALE_FACTOR (5.0f / 9.0f)

int main(void)
{
    float fahrenheit, celsius;
    
    printf("Enter Fahrenheit temperature: ");
    scanf("%f", &fahrenheit);
    
    celsius = (fahrenheit - FREEZING_PT) * SCALE_FACTOR;
    
    printf("Celsius equivalent: %.1f\n", celsius);
    
    return 0;
}
