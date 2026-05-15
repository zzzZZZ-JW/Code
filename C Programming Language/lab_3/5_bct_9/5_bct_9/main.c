//
//  main.c
//  5_bct_9
//
//  Created by 张佳伟 on 2025/10/30.
//

#include <stdio.h>

int main()
{
    int m1 , d1 , y1 , m2 , d2 , y2 ;
    
    printf("请输入第一个日期（月/日/年）：");
    scanf("%d/%d/%d",&m1,&d1,&y1);
    
    printf("请输入第二个日期（月/日/年）：");
    scanf("%d/%d/%d",&m2,&d2,&y2);
    
    if (y1 < y2) {
        printf("%d/%d/%d比%d/%d/%d更早 \n",m1,d1,y1,m2,d2,y2);
    }else if (y1 == y2) {
        if (m1 < m2) {
            printf("%d/%d/%d比%d/%d/%d更早 \n",m1,d1,y1,m2,d2,y2);
        }else if (m1 == m2) {
            if (d1 < d2) {
                printf("%d/%d/%d比%d/%d/%d更早 \n",m1,d1,y1,m2,d2,y2);
            }else {
                printf("%d/%d/%d比%d/%d/%d更早 \n",m2,d2,y2,m1,d1,y1);
            }
        }else if (m1 > m2) {
            printf("%d/%d/%d比%d/%d/%d更早 \n",m2,d2,y2,m1,d1,y1);
        }
    }else if (y1 > y2) {
        printf("%d/%d/%d比%d/%d/%d更早 \n",m2,d2,y2,m1,d1,y1);
    }
    return 0;
}
