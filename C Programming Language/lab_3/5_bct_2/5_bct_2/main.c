//
//  main.c
//  5_bct_2
//
//  Created by 张佳伟 on 2025/10/28.
//

#include <stdio.h>

int main()
{
    int time1 , time2 ;
    
    printf("请输入一个24小时制的时间：");
    scanf("%d:%d",&time1,&time2);
    
    if (time1 <= 12) {
        printf("12小时制时间为：%d:%d AM \n",time1,time2);
    }else {
        time1 = time1 - 12 ;
        printf("12小时制时间为：%d:%d PM \n",time1,time2);
    }
}
