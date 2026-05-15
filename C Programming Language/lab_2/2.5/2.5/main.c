//
//  main.c
//  2.5
//
//  Created by 张佳伟 on 2025/10/17.
//

/* Computes the dimensional weight of a
box from input provided by the user */
#include <stdio.h>

int main(void)
{
    int height, length, width, volume, weight;
    printf("Enter height of box: ");
    scanf("%d", &height);
    
    printf("Enter length of box: ");
    scanf("%d", &length);
    
    printf("Enter width of box: ");
    scanf("%d", &width);
    
    volume = height * length * width;
    weight = (volume + 165) / 166;
    
    printf("Volume (cubic inches): %d\n", volume);
    printf("Dimensional weight (pounds): %d\n", weight);

    return 0;
}
