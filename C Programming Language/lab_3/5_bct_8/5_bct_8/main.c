//
//  main.c
//  5_bct_8
//
//  Created by 张佳伟 on 2025/10/29.
//

#include <stdio.h>

int main()
{
    int time1 , time2 , totle;
    
    printf("请输入一个24小时制时间：");
    scanf("%d:%d",&time1,&time2);
    
    totle = time1 * 60 + time2 ;
    
    int f1 = 480 ;
    int f2 = 583 ;
    int f3 = 679 ;
    int f4 = 767 ;
    int f5 = 840 ;
    int f6 = 945 ;
    int f7 = 1140 ;
    int f8 = 1305 ;
    
    int juedui1 , juedui2 , juedui3 , juedui4 , juedui5 , juedui6 , juedui7 , juedui8 ;
    
    if ((juedui1 = totle - f1) < 0) {
        juedui1 = -juedui1 ;
    }
    if ((juedui2 = totle - f2) < 0) {
        juedui2 = -juedui2 ;
    }
    if ((juedui3 = totle - f3) < 0) {
        juedui3 = -juedui3 ;
    }
    if ((juedui4 = totle - f4) < 0) {
        juedui4 = -juedui4 ;
    }
    if ((juedui5 = totle - f5) < 0) {
        juedui5 = -juedui5 ;
    }
    if ((juedui6 = totle - f6) < 0) {
        juedui6 = -juedui6 ;
    }
    if ((juedui7 = totle - f7) < 0) {
        juedui7 = -juedui7 ;
    }
    if ((juedui8 = totle - f8) < 0) {
        juedui8 = -juedui8 ;
    }
    
    int min = juedui1 ;
    int close = 1 ;
    
    if (juedui2 < juedui1) {
        min = juedui2 ;
        close = 2 ;
    }
    if (juedui3 < juedui2) {
        min = juedui3 ;
        close = 3 ;
    }
    if (juedui4 < juedui3) {
        min = juedui4 ;
        close = 4 ;
    }
    if (juedui5 < juedui4) {
        min = juedui5 ;
        close = 5 ;
    }
    if (juedui6 < juedui5) {
        min = juedui6 ;
        close = 6 ;
    }
    if (juedui7 < juedui6) {
        min = juedui7 ;
        close = 7 ;
    }
    if (juedui8 < juedui7) {
        min = juedui8 ;
        close = 8 ;
    }
    
    switch (close) {
        case 1:
            printf("最近的航班起飞时间为8:00 a.m.，抵达时间为10:16 a.m. \n");
            break;
        case 2:
            printf("最近的航班起飞时间为9:43 a.m.，抵达时间为11:52 a.m. \n");
            break;
        case 3:
            printf("最近的航班起飞时间为11:19 a.m.，抵达时间为1:31 p.m. \n");
            break;
        case 4:
            printf("最近的航班起飞时间为12:47 p.m.，抵达时间为3:00 p.m. \n");
            break;
        case 5:
            printf("最近的航班起飞时间为2:00 p.m.，抵达时间为4:08 p.m. \n");
            break;
        case 6:
            printf("最近的航班起飞时间为3:45 p.m.，抵达时间为5:55 p.m. \n");
            break;
        case 7:
            printf("最近的航班起飞时间为7:00 p.m.，抵达时间为9:20 p.m. \n");
            break;
        case 8:
            printf("最近的航班起飞时间为9:45 p.m.，抵达时间为11:58 p.m. \n");
            break;
    }
    return 0;
}
