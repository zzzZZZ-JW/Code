//
//  main.c
//  chengjiguanli
//
//  Created by 张佳伟 on 2025/10/29.
//

#include <stdio.h>

int main()
{
    int student_id ;
    char student_name[50] ;
    double chinese , math , english ;
    double totle , average ;
    char overall_grade ;
    int menu_choice ;
    
    printf("=== 学生信息管理系统 ===\n");
    printf("1.输入学生信息\n");
    printf("2.计算总分和平均分\n");
    printf("3.判断等级\n");
    printf("4.生成成绩报告\n");
    printf("请选择功能（1-4）：");
    scanf("%d",&menu_choice);
    
    switch (menu_choice) {
        case 1:
            printf("请输入学生学号：");
            scanf("%d",&student_id);
            
            printf("请输入学生姓名：");
            scanf("%s",student_name);
            
            break;
        case 2:
            printf("请输入学生语文成绩：");
            scanf("%lf",&chinese);
            
            printf("请输入学生数学成绩：");
            scanf("%lf",&math);
            
            printf("请输入学生英语成绩：");
            scanf("%lf",&english);
            
            break;
        case 3:
            totle = chinese + math + english ;
            average = totle / 3 ;
            
        case 4:
            
        default:
            printf("无此功能！");
            break;
    }
    return 0;
}
