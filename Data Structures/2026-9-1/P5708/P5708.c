#include <stdio.h>
#include <math.h>

int main() {
    double a , b , c;
    scanf("%lf %lf %lf", &a, &b, &c);

    double p , area;
    p = (a + b + c) / 2;
    area = sqrt(p * (p - a) * (p - b) * (p - c));
    
    printf("%.1f\n",area);
    return 0;
}