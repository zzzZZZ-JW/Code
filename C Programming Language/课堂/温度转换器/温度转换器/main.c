//
//  main.c
//  温度转换器
//
//  Created by 张佳伟 on 2025/11/21.
//

#include <stdio.h>

float CToF(float c){
    float f;
    f = c * (9 / 5) + 32;
    return f;
}

float FToC(float f){
    float c ;
    c = (f - 32) * (5 / 9);
    return c;
}

int main(void)
{
    float temp;
    char type;
    float result;
    
    printf("");
    scanf("%f %c",&temp,&type);
    
    if (type == 'f') {
        result = FToC(temp);
    }else{
        result = CToF(temp);
    }
    
    printf("%f",result);
    
    return 0;
}
