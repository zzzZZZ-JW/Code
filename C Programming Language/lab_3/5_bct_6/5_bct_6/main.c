//
//  main.c
//  5_bct_6
//
//  Created by 张佳伟 on 2025/10/29.
//

#include <stdio.h>

int main()
{
    int i1 , i2 , i3 , i4 , i5 , i6 , i7 , i8 , i9 , i10 , i11 , i12 , test ;
    
    printf("请输入12位数字：");
    scanf("%1d%1d%1d%1d%1d%1d%1d%1d%1d%1d%1d%1d",&i1 , &i2 , &i3 , &i4 , &i5 , &i6 , &i7 , &i8 , &i9 , &i10 , &i11 , &i12) ;
    
    test = 9 - (((( i1 + i3 + i5 + i7 + i9 + i11 ) * 3 + ( i2 + i4 + i6 + i8 + i10 )) - 1 ) % 10 ) ;
    
    if (test == i12) {
        printf("VALID \n") ;
    }else {
        printf("NOT VALID \n") ;
    }
    
    return 0;
}
