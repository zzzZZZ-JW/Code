//
//  main.c
//  4_bct_6
//
//  Created by 张佳伟 on 2025/10/28.
//

#include <stdio.h>

int main()
{
    int i1 , i2 , i3 , i4 , i5 , i6 , i7 , i8 , i9 , i10 , i11 , i12 , test ;
    
    printf("请输入12位数字：");
    scanf("%1d%1d%1d%1d%1d%1d%1d%1d%1d%1d%1d%1d",&i1 , &i2 , &i3 , &i4 , &i5 , &i6 , &i7 , &i8 , &i9 , &i10 , &i11 , &i12) ;
    
    test = 9 - (((( i2 + i4 + i6 + i8 + i10 + i12 ) * 3 + ( i1 + i3 + i5 + i7 + i9 + i11 )) - 1 ) % 10 ) ;
    
    printf("校验位为：%d\n",test);
    
    return 0;
}
