//
//  main.c
//  zuidagongyueshu
//
//  Created by 张佳伟 on 2025/11/7.
//

#include <stdio.h>

int main()
{
    int a , b , r ;
    
    printf("请输入两个数：");
    scanf("%d,%d",&a,&b);
    
    do {
        r = a % b ;
        a = b ;
        b = r ;
    } while (r != 0);
    
    printf("最大公约数为%d\n",a);
    
    return 0;
}
