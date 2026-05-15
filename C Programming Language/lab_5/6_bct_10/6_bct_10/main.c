//
//  main.c
//  6_bct_10
//
//  Created by 张佳伟 on 2025/11/7.
//

#include <stdio.h>

int main()
{
    int dangqianyue, dangqianri, dangqiannian;
    int yue, ri, nian;
    
    printf("请输入日期（月/日/年），输入0/0/0结束：\n");
    
    printf("请输入日期（月/日/年）：");
    scanf("%d/%d/%d", &yue, &ri, &nian);
    if (yue == 0 && ri == 0 && nian == 0) {
        printf("没有输入日期。\n");
        return 0;
    }
    dangqianyue = yue;
    dangqianri = ri;
    dangqiannian = nian;
    
    while (1) {
        printf("请输入日期（月/日/年）：");
        scanf("%d/%d/%d", &yue, &ri, &nian);
        if (yue == 0 && ri == 0 && nian == 0) {
            break;
        }
        
        if (nian > dangqiannian) {
            dangqianyue = yue;
            dangqianri = ri;
            dangqiannian = nian;
        } else if (nian == dangqiannian) {
            if (yue > dangqianyue) {
                dangqianyue = yue;
                dangqianri = ri;
                dangqiannian = nian;
            } else if (yue == dangqianyue) {
                if (ri > dangqianri) {
                    dangqianyue = yue;
                    dangqianri = ri;
                    dangqiannian = nian;
                }
            }
        }
    }
    
    printf("最晚的日期是：%d/%d/%d\n", dangqianyue, dangqianri, dangqiannian);
    
    return 0;
}
