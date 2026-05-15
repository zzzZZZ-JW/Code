//
//  main.c
//  bct_4
//
//  Created by 张佳伟 on 2025/10/17.
//

#include <stdio.h>

int main()
{
    double doller ,result;
    printf("请输入一个美元金额：");
    scanf("%lf",&doller);
    
    result = doller * 1.05;
    
    printf("增加5%税率后的相应金额为：%.2f\n",result);
    
    return 0;
    
    
    
}
