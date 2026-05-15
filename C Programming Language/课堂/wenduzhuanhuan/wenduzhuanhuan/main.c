//
//  main.c
//  wenduzhuanhuan
//
//  Created by 张佳伟 on 2025/10/17.
//

#include <stdio.h>

int main()
{
    //声明变量
    double c;
    double f;
    //用户输入
    printf("请输入摄氏温度:");
    scanf("%lf",&c);
    //公式
    f = c*9/5+32;
    //输出
    printf("对应的华氏温度为：%.2f \n",f);
    
    
    
    return 0;
}
