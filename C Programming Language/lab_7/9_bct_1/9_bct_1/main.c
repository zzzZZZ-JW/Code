//
//  main.c
//  9_bct_1
//
//  Created by 张佳伟 on 2025/11/21.
//

#include <stdio.h>

void selection_sort(int num[], int n) {
    if (n <= 1) {
        return;
    }
    
    int max = n - 1;
    for (int i = 0; i < n; i++) {
        if (num[i] > num[max]) {
            max = i;
        }
    }
    
    int temp = num[max];
    num[max] = num[n - 1];
    num[n - 1] = temp;
    
    selection_sort(num, n - 1);
}

int main(void){
    int n;
    
    printf("请输入元素数量：");
    scanf("%d",&n);
    
    int num[n];
    
    printf("请输入%d个整数：", n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &num[i]);
    }
    
    selection_sort(num,n);
    
    printf("排序后的数为：");
    for (int i = 0; i < n; i++) {
        printf("%d",num[i]);
    }
    printf("\n");
    
    return 0;
}
