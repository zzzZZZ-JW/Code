//
//  main.c
//  5_bct_3
//
//  Created by 张佳伟 on 2025/10/28.
//

#include <stdio.h>

int main()
{
    float gushu , meigujia , commission , value , commission2 ;
    
    printf("请输入股票数量：");
    scanf("%f", &gushu);
    printf("请输入每股的价格：");
    scanf("%f",&meigujia);
    
    value = gushu * meigujia ;
    
    if (value < 2500.00f)
        commission = 30.00f + .017f * value;
    else if (value < 6250.00f)
        commission = 56.00f + .0066f * value;
    else if (value < 20000.00f)
        commission = 76.00f + .0034f * value;
    else if (value < 50000.00f)
        commission = 100.00f + .0022f * value;
    else if (value < 500000.00f)
        commission = 155.00f + .0011f * value;
    else
        commission = 255.00f + .0009f * value;
    
    if (commission < 39.00f)
        commission = 39.00f;
    
    if (value < 2000.00f)
        commission2 = 33.00f * value + 0.03f;
    else
        commission2 = 33.00f * value + 0.02f;
    
    printf("经纪人的佣金为: $%.2f\n", commission);
    printf("经纪人竞争对手的佣金为: $%.2f\n", commission2);
    
    return 0;
}
