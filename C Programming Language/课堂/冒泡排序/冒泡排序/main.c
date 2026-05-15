//
//  main.c
//  冒泡排序
//
//  Created by 张佳伟 on 2025/12/3.
//

#include <stdio.h>

int max(int num[] , int len){
    int index = 0;
    int max = num[0];
    
    for (int i = 0; i < len; i++) {
        if (num[i] > max) {
            max = num[i];
            index = i;
        }
    }
    return index;
}

void sort(int num[] , int len) {
    for (int i = 0; i < len - 1; i++) {
        int index = max(num , len - i);
        if (index != len - 1 - i) {
            int temp = num[index];
            num[index] = num[len - 1 - i];
            num[len - 1 - i] = temp;
        }
    }
}

int main(void){
    int num[] = {0} , len;
    printf("请输入数字位数：");
    scanf("%d",&len);
    printf("请输入一串数字：");
    scanf("%d",&num);
    
    sort(num, len);
    
    printf("排序为：");
    for (int i = 0; i < len; i++) {
        printf("%d",num[i]);
    }
    
}
