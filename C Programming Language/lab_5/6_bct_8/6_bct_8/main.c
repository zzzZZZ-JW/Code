//
//  main.c
//  6_bct_8
//
//  Created by 张佳伟 on 2025/11/7.
//

#include <stdio.h>

int main()
{
    int tianshu , qishi ;
    
    printf("请输入这个月的天数：");
    scanf("%d",&tianshu);
    
    printf("该月起始日是星期几（1=星期日，7=星期六）：");
    scanf("%d",&qishi);
    
    for (int i = 1; i <= tianshu; i = i + 1) {
        if (i == 7) {
            printf("\n");
        }else{
            printf("%d",i);
        }
    }
    return 0;
}
