//
//  main.c
//  bct_3
//
//  Created by 张佳伟 on 2025/10/17.
//

#include <stdio.h>

int main()
{
    double r ;
    const double pi = 3.14 ;
    printf("请输入球体半径：");
    scanf("%lf", &r );
    
    double v = ( 3.0f / 4.0f ) * pi * r * r ;
    
    printf("球的体积为：%.2f\n",v);
    return 0;
}
