//
//  main.c
//  lab_9_new
//
//  Created by 张佳伟 on 2025/12/9.
//

/*
 
宏定义（Constants）
• MAX_STUDENTS：最大学生数（100）
• MAX_NAME_LEN：姓名的最大长度（20个字符）
• SUBJECT_COUNT：科目数量（3科）

全局数组变量（Global Array Variables）
• names[][]：存储学生姓名的二维字符数组
• ids[]：存储学生学号的整数数组
• scores[][]：存储学生各科成绩的二维浮点数数组
• totals[]：存储学生总分的一维浮点数数组
• averages[]：存储学生平均分的一维浮点数数组
• grades[]：存储学生等级（A/B/C/D/F）的字符数组

函数（Functions）
1. initialize_system：初始化系统，返回初始学生数量
2. input_student_info：输入学生信息，返回更新后的学生数量
3. display_student_info：显示单个学生的详细信息
4. display_all_students_summary：显示所有学生的汇总信息
5. calculate_class_statistics：计算并显示班级统计数据
6. swap_students：交换两个学生的所有数据（用于排序）
7. simple_bubble_sort：使用冒泡排序按总分对学生进行排序
8. search_by_name：按姓名搜索学生，返回索引或-1
9. search_by_student_id：按学号搜索学生，返回索引或-1
10. search_by_score_range：按分数范围搜索学生
11. recursive_sum_total_scores：递归计算总分总和
12. recursive_count_grade：递归统计指定等级的学生数量
13. debug_bubble_sort：调试版本的冒泡排序（可能包含打印语句）
14. simple_system_test：系统简单测试函数
15. main：主函数，程序的入口点

函数参数说明
• current_count：当前学生数量
• target_name：要搜索的目标姓名
• target_id：要搜索的目标学号
• target_grade：要统计的目标等级
• min_score/max_score：分数范围的最小值和最大值
• index：数组索引
 
*/

#include <stdlib.h>
#include <stdio.h>

#define MAX_STUDENTS 100
#define MAX_NAME_LEN 20
#define SUBJECT_COUNT 3

char jisuan_dengji(float average){
    if (average >= 90) {
        return 'A';
    }else if (average >= 80){
        return 'B';
    }else if (average >= 70){
        return 'C';
    }else if (average >= 60){
        return 'D';
    }else{
        return 'F';
    }
}

void jisuan_xuesheng_zongfen(float scores[][SUBJECT_COUNT],
                             float totals[] , float averages[] , int index){
    totals[index] = 0;
    for (int i = 0; i < SUBJECT_COUNT; i++) {
        totals[index] = totals[index] + scores[index][i];
    }
    averages[index] = totals[index] / SUBJECT_COUNT;
}

void initialize_system(char names[][MAX_NAME_LEN], int ids[],
                      float scores[][SUBJECT_COUNT],
                      float totals[], float averages[], char grades[]){
    char name[][MAX_NAME_LEN] = {
        {'z','h','a','n','g','s','a','n'}
    };
}

int input_student_info(char names[][MAX_NAME_LEN], int ids[],
                       float scores[][SUBJECT_COUNT], int current_count){
    printf("请输入学生姓名：");
    scanf("%c",&names[current_count][MAX_NAME_LEN]);
    return current_count + 1;
}

void display_student_info(int index, char names[][MAX_NAME_LEN], int ids[],
                          float scores[][SUBJECT_COUNT],
                          float totals[], float averages[], char grades[]);

void display_all_students_summary(char names[][MAX_NAME_LEN], int ids[],
                                  float scores[][SUBJECT_COUNT],
                                  float totals[], float averages[],
                                  char grades[], int count);

void calculate_class_statistics(char names[][MAX_NAME_LEN],
                                float totals[], float averages[], int count);

void swap_students(int i, int j, char names[][MAX_NAME_LEN], int ids[],
                   float scores[][SUBJECT_COUNT],
                   float totals[], float averages[], char grades[]);

void simple_bubble_sort(char names[][MAX_NAME_LEN], int ids[],
                        float scores[][SUBJECT_COUNT],
                        float totals[], float averages[],
                        char grades[], int count);

int search_by_name(char names[][MAX_NAME_LEN], char* target_name, int count);
int search_by_student_id(char names[][MAX_NAME_LEN], int ids[],
                         int target_id, int count);
void search_by_score_range(char names[][MAX_NAME_LEN], int ids[],
                           float totals[], float averages[], char grades[],
                           int count, float min_score, float max_score);

float recursive_sum_total_scores(char names[][MAX_NAME_LEN],
                                 float totals[], int count, int index);
int recursive_count_grade(char names[][MAX_NAME_LEN], char grades[],
                          int count, char target_grade, int index);

void debug_bubble_sort(char names[][MAX_NAME_LEN], int ids[],
                       float scores[][SUBJECT_COUNT],
                       float totals[], float averages[],
                       char grades[], int count);

void simple_system_test(char names[][MAX_NAME_LEN], int ids[],
                        float scores[][SUBJECT_COUNT],
                        float totals[], int count);

int main(void) {
    char names[MAX_STUDENTS][MAX_NAME_LEN];
    int ids[MAX_STUDENTS];
    float scores[MAX_STUDENTS][SUBJECT_COUNT];
    float totals[MAX_STUDENTS];
    float averages[MAX_STUDENTS];
    char grades[MAX_STUDENTS];
    //int count = initialize_system(names, ids, scores, totals, averages, grades);
    
    int xuanze;
    printf("1、系统自检\n2、输入学生信息\n3、显示单个学生成绩\n4、显示所有学生成绩\n5、显示统计数据\n6、交换学生信息\n7、排序\n8、搜索姓名\n9、搜索学号\n10、按分数范围搜索\n11、计算总分总和\n12、计算指定等级学生数量\n13、调试冒泡排序\n14、调试\n");
    printf("请选择功能：");
    scanf("%d",&xuanze);
    
    switch (xuanze) {
        case 1:
            initialize_system;
            break;
        case 2:
            input_student_info;
            break;
            case 3:
            display_student_info;
            break;
        case 4:
            display_all_students_summary;
            break;
        case 5:
            calculate_class_statistics;
            break;
        case 6:
            swap_students;
            break;
        case 7:
            simple_bubble_sort;
            break;
        case 8:
            search_by_name;
            break;
        case 9:
            search_by_student_id;
            break;
        case 10:    
            search_by_score_range;
            break;
        case 11:
            recursive_sum_total_scores;
            break;
        case 12:
            recursive_count_grade;
            break;
        case 13:
            debug_bubble_sort;
            break;
        case 14:
            simple_system_test;
            break;
        default:
            printf("输入有误，请重新选择！");
            break;            

    }
    // TODO: 菜单循环，调用上面各功能函数
    return 0;
}
