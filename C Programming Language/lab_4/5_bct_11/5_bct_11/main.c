//
//  main.c
//  5_bct_11
//
//  Created by 张佳伟 on 2025/10/31.
//

#include <stdio.h>

int main()
{
    int shi , ge , shu ;
    
    printf("请输入一个两位数：");
    scanf("%1d%1d",&shi,&ge);
    
    shu = shi * 10 + ge ;
    
    if (shu <= 9 || shu >=100) {
        printf("输入错误！请输入一个两位数");
    }else if (shu >= 11 && shu <= 19) {
        switch (shu) {
            case 11:
                printf("对应的英文单词为：Eleven\n");
                break;
            case 12:
                printf("对应的英文单词为：Twelve\n");
                break;
            case 13:
                printf("对应的英文单词为：Thirteen\n");
                break;
            case 14:
                printf("对应的英文单词为：Fourteen\n");
                break;
            case 15:
                printf("对应的英文单词为：Fifteen\n");
                break;
            case 16:
                printf("对应的英文单词为：Sixteen\n");
                break;
            case 17:
                printf("对应的英文单词为：Seventeen\n");
                break;
            case 19:
                printf("对应的英文单词为：Nineteen\n");
                break;
            default:
                break;
        }
    }else {
        switch (shi) {
            case 2:
                printf("对应的英文单词为：Twenty");
                break;
            case 3:
                printf("对应的英文单词为：Thirty");
                break;
            case 4:
                printf("对应的英文单词为：Forty");
                break;
            case 5:
                printf("对应的英文单词为：Fifty");
                break;
            case 6:
                printf("对应的英文单词为：Sixty");
                break;
            case 7:
                printf("对应的英文单词为：Seventy");
                break;
            case 8:
                printf("对应的英文单词为：Eighty");
                break;
            case 9:
                printf("对应的英文单词为：Ninety");
                break;
            default:
                break;
        }
        switch (ge) {
            case 1:
                printf("-one\n");
                break;
            case 2:
                printf("-two\n");
                break;
            case 3:
                printf("-three\n");
                break;
            case 4:
                printf("-four\n");
                break;
            case 5:
                printf("-five\n");
                break;
            case 6:
                printf("-six\n");
                break;
            case 7:
                printf("-seven\n");
                break;
            case 8:
                printf("-eight\n");
                break;
            case 9:
                printf("-nine\n");
                break;
            case 0:
                printf("\n");
                break;
            default:
                break;
        }
    }
    
    return 0;
}
