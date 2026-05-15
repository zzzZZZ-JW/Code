//
//  main.c
//  10_lxt_5
//
//  Created by 张佳伟 on 2025/12/18.
//

#include <stdlib.h>
#include <stdio.h>

void split_time(int total_sec, int *hr, int *min, int *sec) {
    *hr = total_sec / 3600;
    *min = (total_sec % 3600) / 60;
    *sec = total_sec % 60;
}

int main(void){
    int total_sec;
    printf("请输入总秒数: ");
    scanf("%d", &total_sec);
    
    int hr, min, sec;
    split_time(total_sec, &hr, &min, &sec);
    printf("结果为: %d小时%d分钟%d秒\n", hr, min, sec);
    return 0;
}
