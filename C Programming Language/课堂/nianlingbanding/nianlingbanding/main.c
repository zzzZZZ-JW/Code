//
//  main.c
//  nianlingbanding
//
//  Created by 张佳伟 on 2025/10/22.
//

#include <stdio.h>

int main()
{
    int year ;
    
    printf("请输入年龄：");
    scanf("%d",&year);
    
    if (year < 0) {
        printf("请输入正确的年龄！\n");
    }else if(year <3){
        printf("年龄阶段为：婴幼儿\n");
    }else if (year < 6){
        printf("年龄阶段为：学龄前\n");
    }else if (year < 18) {
        printf("年龄阶段为：青少年\n");
    }else if (year < 35){
        printf("年龄阶段为：青年\n");
    }else if (year < 60){
        printf("年龄阶段为：中年\n");
    }else {
        printf("年龄阶段为：老年\n");
    }
    
    return 0;
}
