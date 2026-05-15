//
//  main.c
//  bct_8
//
//  Created by 张佳伟 on 2025/10/19.
//

#include <stdio.h>

int main()
{
    double huankuanjine , lilv , yuefukuan , yi , er , san , yisheng , ersheng ;
    printf("请输入还款金额：");
    scanf("%lf",&huankuanjine);
    
    printf("请输入月利率：");
    scanf("%lf",&lilv);
    
    printf("请输入月还款金额：");
    scanf("%lf",&yuefukuan);
    
    huankuanjine = huankuanjine + huankuanjine * ( ( lilv * 0.01 ) / 12 ) ;
    
    yi = huankuanjine - yuefukuan ;
    yisheng = yi + yi * ( ( lilv * 0.01 ) / 12 ) ;
    
    er = yisheng - yuefukuan ;
    ersheng = er + er * ( ( lilv * 0.01 ) / 12 ) ;
    
    san = ersheng - yuefukuan;

    printf("第一个月还款后剩余的贷款余额为%.2f\n第二个月还款后剩余的贷款余额为%.2f\n第三个月还款后剩余的贷款余额为%.2f\n",yi , er , san );
    
    return 0;
    
}
