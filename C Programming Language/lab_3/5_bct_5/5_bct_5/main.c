//
//  main.c
//  5_bct_5
//
//  Created by 张佳伟 on 2025/10/29.
//

#include <stdio.h>

int main()
{
    double suode , shui ;
    
    printf("请输入应纳税所得额：");
    scanf("%lf",&suode);
    
    if (suode <= 750) {
        shui = suode * 0.01 ;
        printf("税金为：%.2f\n",shui);
    }else if (suode <= 2250) {
        shui = 7.50 + (suode - 750) * 0.02 ;
        printf("税金为：%.2f\n",shui);
    }else if (suode <= 3750) {
        shui = 37.50 + (suode - 2250) * 0.03 ;
        printf("税金为：%.2f\n",shui) ;
    }else if (suode <= 5250) {
        shui = 82.50 + (suode - 3750) * 0.04 ;
        printf("税金为：%.2f\n",shui) ;
    }else if (suode <= 7000) {
        shui = 142.50 + (suode - 5250) * 0.05 ;
        printf("税金为：%.2f\n",shui) ;
    }else {
        shui = 230.00 + (suode - 7000) * 0.06 ;
        printf("s税金为：%.2f\n",shui) ;
    }
    return 0;
}
