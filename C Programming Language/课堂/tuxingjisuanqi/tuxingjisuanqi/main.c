//
//  main.c
//  tuxingjisuanqi
//
//  Created by 张佳伟 on 2025/10/17.
//

#include <stdio.h>

int main()
{
    double r;
    double l;
    double s;
    const double pi = 3.14;
    
    printf("请输入半径：");
    scanf("%lf" , &r);
           
    l = 2*pi*r;
    s = pi*r*r;
           
    printf("圆的周长是：%.2f \n",l);
    printf("面积是：%.2f \n",s);
           
    return 0;
}
