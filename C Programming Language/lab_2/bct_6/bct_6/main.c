//
//  main.c
//  bct_6
//
//  Created by 张佳伟 on 2025/10/19.
//

#include <stdio.h>

int main()
{
    int x,result;
    printf("请输入x的值：");
    scanf("%d",&x);
    
    result = (((( 3 * x + 2) * x - 5) * x - 1 ) * x + 7) * x -6 ;
    
    printf("结果为：%d \n" , result) ;
    return 0;
}
