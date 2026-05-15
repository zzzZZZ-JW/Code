//
//  main.c
//  10_lxt_4
//
//  Created by 张佳伟 on 2025/12/18.
//

#include <stdlib.h>
#include <stdio.h>

void swap(int *p, int *q) {
    int temp = *p;
    *p = *q;
    *q = temp;
}

int main(void){
    int a, b;
    printf("请输入两个数(a,b)：");
    scanf("%d,%d",&a,&b);
    swap(&a,&b);
    printf("交换后为：%d,%d\n",a,b);
    return 0;
}
