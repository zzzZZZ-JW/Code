//
//  main.c
//  lab8_2
//
//  Created by 张佳伟 on 2025/11/28.
//

#include <stdio.h>

void bidaxiao(int a , int b){
    int max = a;
    int min = b;
    
    if (b > a) {
        max = b;
        min = a;
    }
    printf("最大值为：%d\n",max);
    printf("最小值为：%d\n",min);
}

void jueduizhi(int n){
    int answer;
    if (n >= 0) {
        answer = n;
    }else{
        answer = -n;
    }
    printf("绝对值为：%d\n",answer);
}

void panduanzhishu(int num){
    if (num < 2) {
        printf("%d不是素数\n", num);
    }

    int i;
    
    for(i = 2; i < num; i++){
        if(num % i == 0){
            printf("%d不是素数\n", num);
            break;
        }
    }
    if (i == num) {
        printf("%d是素数\n", num);
    }
}

void GCD(int a , int b){
    int r;
    do {
        r = a % b ;
        a = b ;
        b = r ;
    } while (r != 0);
    
    printf("最大公约数为%d\n",a);
    
}

int main(void){
    int xuanze;
    
    printf("请输入功能代码：");
    scanf("%d",&xuanze);
    
    switch (xuanze) {
        case 1:
        {
            int a , b;
            
            printf("请输入两个数：");
            scanf("%d %d",&a,&b);
            
            bidaxiao(a, b);
            break;
        }
        case 2:
        {
            int n;
            
            printf("请输入一个数：");
            scanf("%d",&n);
            
            jueduizhi(n);
            break;
        }
        case 3:
        {
            int num;
            
            printf("请输入一个自然数:");
            scanf("%d",&num);
            
            panduanzhishu(num);
            break;
        }
        case 4:
        {
            int a , b;
            
            printf("请输入两个数：");
            scanf("%d,%d",&a,&b);
            
            GCD(a, b);
            break;
        }
    }
    return 0;
}
