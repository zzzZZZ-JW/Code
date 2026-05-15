//
//  main.c
//  数组查询
//
//  Created by 张佳伟 on 2025/11/14.
//

#include <stdio.h>

int main()
{
    int chaxun ;
    int shuzu[8] = {1,2,3,4,5,6,7,8};
    int count = 0;
    
    printf("请输入需要查询的数：");
    scanf("%d",&chaxun);
    
    for (int i = 0; i < 8; i++) {
        if (chaxun == shuzu[i]) {
            count++;
        }
    }
    printf("有%d个",count);
    
    return 0;
}
