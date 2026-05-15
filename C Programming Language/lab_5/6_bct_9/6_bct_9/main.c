//
//  main.c
//  6_bct_9
//
//  Created by 张佳伟 on 2025/11/7.
//

#include <stdio.h>

int main()
{
    double huankuanjine, lilv, yuefukuan;
    int cishu;
    
    printf("请输入还款金额：");
    scanf("%lf", &huankuanjine);
    
    printf("请输入月利率：");
    scanf("%lf", &lilv);
    
    printf("请输入月还款金额：");
    scanf("%lf", &yuefukuan);
    
    printf("请输入还贷次数：");
    scanf("%d", &cishu);
    
    double balance = huankuanjine;
    double monthly_rate = (lilv * 0.01) / 12;
    
    for (int i = 1; i <= cishu; i++) {
        balance = balance + balance * monthly_rate;
        
        balance = balance - yuefukuan;
        
        printf("第%d个月还款后剩余的贷款余额为%.2f\n", i, balance);
    }
    
    return 0;
}
