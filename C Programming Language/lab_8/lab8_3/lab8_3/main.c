//
//  main.c
//  lab8_3
//
//  Created by 张佳伟 on 2025/11/29.
//

#include <stdio.h>

int gn3(int num){
    int count = 0;
    do {
        num = num / 10;
        count++;
    } while (num != 0);
    return count;
}

void shuzu(int numbers[], int num){
    int n = gn3(num);
    int temp = num;
    
    for (int i = n - 1; i >= 0; i--) {
        numbers[i] = temp % 10;
        temp = temp / 10;
    }
}

void gn1(int numbers[], int n){
    int temp;
    for (int i = 0; i < n; i++) {
        temp = numbers[i];
        numbers[i] = numbers[n-1-i];
        numbers[n-1-i] = temp;
    }
    
    for (int i = 0; i < 6; i++) {
        printf("反转数字为%d ", numbers[i]);
    }
}

void gn2(int numbers[], int n){
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum = sum + numbers[i];
    }
    printf("各位数字之和为%d",sum);
}

void gn4(int num ){
    int d , result = 0 , temp = num;
    while (temp != 0) {
            d = temp % 10 ;
            temp = temp / 10 ;
            result = result * 10 + d ;
        }
    if (result == num) {
        printf("是回文数");
    }else{
        printf("不是回文数");
    }
}

int main(void){
    int xuanze , numbers[] = {0};
    
    printf("请选择功能：");
    scanf("%d",&xuanze);
    
    
    switch (xuanze) {
        case 1:{
            int n , num;
            printf("请输入数字");
            scanf("%d",&num);
            n = gn3(num);
            shuzu(numbers , n);
            gn1(numbers, n);
            break;
        }
        case 2:{
            int n , num;
            printf("请输入数字");
            scanf("%d",&num);
            n = gn3(num);
            shuzu(numbers , n);
            gn2(numbers, n);
            break;
        }
        case 3:{
            int n , num;
            printf("请输入数字");
            scanf("%d",&num);
            n = gn3(num);
            printf("数字位数为：%d",n);
            break;
        }
        case 4:{
            int num;
            printf("请输入数字");
            scanf("%d",&num);
            gn4(num);
            break;
        }
    }
    return 0;
}
