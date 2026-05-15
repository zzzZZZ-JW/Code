//
//  main.c
//  6_bct_4
//
//  Created by 张佳伟 on 2025/11/2.
//

#include <stdio.h>

int main()
{
    // 定义两个变量：佣金和交易金额
    float commission, value;
    
    // 提示用户输入交易金额
    printf("Enter value of trade: ");
    // 读取用户输入的交易金额
    scanf("%f", &value);
    
    // 当输入的交易金额不为0时，循环计算佣金
    while (value != 0) {
        // 根据不同的交易金额范围计算佣金
        if (value < 2500.00f)
            commission = 30.00f + .017f * value;        // 小于2500美元：30美元 + 1.7%的交易金额
        else if (value < 6250.00f)
            commission = 56.00f + .0066f * value;       // 2500-6250美元：56美元 + 0.66%的交易金额
        else if (value < 20000.00f)
            commission = 76.00f + .0034f * value;       // 6250-20000美元：76美元 + 0.34%的交易金额
        else if (value < 50000.00f)
            commission = 100.00f + .0022f * value;      // 20000-50000美元：100美元 + 0.22%的交易金额
        else if (value < 500000.00f)
            commission = 155.00f + .0011f * value;      // 50000-500000美元：155美元 + 0.11%的交易金额
        else
            commission = 255.00f + .0009f * value;      // 大于等于500000美元：255美元 + 0.09%的交易金额
        
        // 如果计算出的佣金低于39美元，则按39美元收取（最低佣金）
        if (commission < 39.00f)
            commission = 39.00f;
        
        // 输出计算出的佣金，保留两位小数
        printf("Commission: $%.2f\n", commission);
        
        // 再次提示用户输入交易金额，为下一次循环做准备
        printf("Enter value of trade: ");
        scanf("%f", &value);
        
    }
    return 0;
}
