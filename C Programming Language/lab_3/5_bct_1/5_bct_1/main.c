//
//  main.c
//  5_bct_1
//
//  Created by 张佳伟 on 2025/10/28.
//

#include <stdio.h>

int main()
{
    int num ;
    
    printf("请输入一个数：");
    scanf("%d",&num);
    
    if ( num >= 0 && num <= 9 ) {
        printf("位数为1\n");
    }else if( num <= 99 ) {
        printf("位数为2\n");
    }else if( num <= 999 ) {
        printf("位数为3\n");
    }else if( num <= 9999 ) {
        printf("位数为4\n");
    }
    
    return 0;
}
