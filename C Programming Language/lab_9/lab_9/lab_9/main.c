//
//  main.c
//  lab_9
//
//  Created by 张佳伟 on 2025/12/6.
//

#include <stdio.h>
#include <string.h>

#define MAX_STUDENTS 100
#define MAX_NAME_LEN 20
#define SUBJECT_COUNT 3

// 函数声明（保持不变）
int initialize_system(char names[][MAX_NAME_LEN], int ids[],
                      float scores[][SUBJECT_COUNT],
                      float totals[], float averages[], char grades[]);

int input_student_info(char names[][MAX_NAME_LEN], int ids[],
                       float scores[][SUBJECT_COUNT], int current_count);

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

// 辅助函数：计算等级
char calculate_grade(float average) {
    if (average >= 90.0) return 'A';
    else if (average >= 80.0) return 'B';
    else if (average >= 70.0) return 'C';
    else if (average >= 60.0) return 'D';
    else return 'F';
}

// 辅助函数：计算单个学生的总分和平均分
void calculate_student_total_average(float scores[][SUBJECT_COUNT], 
                                     float totals[], float averages[], 
                                     int index) {
    totals[index] = 0.0;
    for (int k = 0; k < SUBJECT_COUNT; k++) {
        totals[index] += scores[index][k];
    }
    averages[index] = totals[index] / SUBJECT_COUNT;
}

// 1. 初始化系统，预置5个学生数据
int initialize_system(char names[][MAX_NAME_LEN], int ids[],
                      float scores[][SUBJECT_COUNT],
                      float totals[], float averages[], char grades[]) {
    // 预置5个学生的姓名
    strcpy(names[0], "Zhang San");
    strcpy(names[1], "Li Si");
    strcpy(names[2], "Wang Wu");
    strcpy(names[3], "Zhao Liu");
    strcpy(names[4], "Qian Qi");
    
    // 学号 1001-1005
    ids[0] = 1001;
    ids[1] = 1002;
    ids[2] = 1003;
    ids[3] = 1004;
    ids[4] = 1005;
    
    // 三门成绩
    // 学生1: 85, 90, 88
    scores[0][0] = 85.0;
    scores[0][1] = 90.0;
    scores[0][2] = 88.0;
    
    // 学生2: 78, 82, 80
    scores[1][0] = 78.0;
    scores[1][1] = 82.0;
    scores[1][2] = 80.0;
    
    // 学生3: 92, 95, 88
    scores[2][0] = 92.0;
    scores[2][1] = 95.0;
    scores[2][2] = 88.0;
    
    // 学生4: 65, 70, 68
    scores[3][0] = 65.0;
    scores[3][1] = 70.0;
    scores[3][2] = 68.0;
    
    // 学生5: 55, 60, 58
    scores[4][0] = 55.0;
    scores[4][1] = 60.0;
    scores[4][2] = 58.0;
    
    // 计算每个学生的总分、平均分和等级
    for (int i = 0; i < 5; i++) {
        calculate_student_total_average(scores, totals, averages, i);
        grades[i] = calculate_grade(averages[i]);
    }
    
    return 5; // 返回初始学生数量
}

// 2. 输入新学生信息
int input_student_info(char names[][MAX_NAME_LEN], int ids[],
                       float scores[][SUBJECT_COUNT], int current_count) {
    if (current_count >= MAX_STUDENTS) {
        printf("学生数量已达上限，无法添加新学生！\n");
        return current_count;
    }
    
    printf("\n=== 添加新学生 ===\n");
    
    // 输入姓名
    printf("请输入学生姓名（最多%d个字符）：", MAX_NAME_LEN - 1);
    scanf("%s", names[current_count]);
    
    // 输入学号
    printf("请输入学生学号：");
    scanf("%d", &ids[current_count]);
    
    // 输入三门成绩
    printf("请输入三门课程成绩（用空格分隔）：");
    for (int i = 0; i < SUBJECT_COUNT; i++) {
        scanf("%f", &scores[current_count][i]);
    }
    
    printf("学生信息添加成功！\n");
    return current_count + 1; // 返回新的学生数量
}

// 3. 显示单个学生信息
void display_student_info(int index, char names[][MAX_NAME_LEN], int ids[],
                          float scores[][SUBJECT_COUNT],
                          float totals[], float averages[], char grades[]) {
    printf("\n=== 学生详细信息 ===\n");
    printf("索引：%d\n", index);
    printf("姓名：%s\n", names[index]);
    printf("学号：%d\n", ids[index]);
    printf("成绩1：%.1f\n", scores[index][0]);
    printf("成绩2：%.1f\n", scores[index][1]);
    printf("成绩3：%.1f\n", scores[index][2]);
    printf("总分：%.1f\n", totals[index]);
    printf("平均分：%.1f\n", averages[index]);
    printf("等级：%c\n", grades[index]);
}

// 4. 显示所有学生摘要
void display_all_students_summary(char names[][MAX_NAME_LEN], int ids[],
                                  float scores[][SUBJECT_COUNT],
                                  float totals[], float averages[],
                                  char grades[], int count) {
    printf("\n=== 所有学生信息摘要 ===\n");
    printf("┌────┬────────────┬────────┬──────┬──────┬──────┬──────┬──────┬──────┐\n");
    printf("│序号│   姓名     │  学号  │成绩1 │成绩2 │成绩3 │ 总分 │ 均分 │ 等级 │\n");
    printf("├────┼────────────┼────────┼──────┼──────┼──────┼──────┼──────┼──────┤\n");
    
    for (int i = 0; i < count; i++) {
        printf("│%4d│%12s│%8d│%6.1f│%6.1f│%6.1f│%6.1f│%6.1f│  %c   │\n",
               i + 1, names[i], ids[i], 
               scores[i][0], scores[i][1], scores[i][2],
               totals[i], averages[i], grades[i]);
    }
    printf("└────┴────────────┴────────┴──────┴──────┴──────┴──────┴──────┴──────┘\n");
}

// 5. 计算班级统计信息
void calculate_class_statistics(char names[][MAX_NAME_LEN],
                                float totals[], float averages[], int count) {
    if (count == 0) {
        printf("没有学生数据！\n");
        return;
    }
    
    float class_total_sum = 0.0;
    float class_average_sum = 0.0;
    float max_total = totals[0];
    float min_total = totals[0];
    int max_index = 0;
    int min_index = 0;
    
    for (int i = 0; i < count; i++) {
        class_total_sum += totals[i];
        class_average_sum += averages[i];
        
        if (totals[i] > max_total) {
            max_total = totals[i];
            max_index = i;
        }
        if (totals[i] < min_total) {
            min_total = totals[i];
            min_index = i;
        }
    }
    
    printf("\n=== 班级统计信息 ===\n");
    printf("学生总数：%d\n", count);
    printf("班级总分和：%.1f\n", class_total_sum);
    printf("班级平均总分：%.1f\n", class_total_sum / count);
    printf("班级平均分：%.1f\n", class_average_sum / count);
    printf("最高分学生：%s (学号：%d，总分：%.1f)\n", 
           names[max_index], max_index + 1001, max_total);
    printf("最低分学生：%s (学号：%d，总分：%.1f)\n", 
           names[min_index], min_index + 1001, min_total);
}

// 6. 交换两个学生信息
void swap_students(int i, int j, char names[][MAX_NAME_LEN], int ids[],
                   float scores[][SUBJECT_COUNT],
                   float totals[], float averages[], char grades[]) {
    // 交换姓名
    char temp_name[MAX_NAME_LEN];
    strcpy(temp_name, names[i]);
    strcpy(names[i], names[j]);
    strcpy(names[j], temp_name);
    
    // 交换学号
    int temp_id = ids[i];
    ids[i] = ids[j];
    ids[j] = temp_id;
    
    // 交换成绩
    for (int k = 0; k < SUBJECT_COUNT; k++) {
        float temp_score = scores[i][k];
        scores[i][k] = scores[j][k];
        scores[j][k] = temp_score;
    }
    
    // 交换总分、平均分、等级
    float temp_total = totals[i];
    totals[i] = totals[j];
    totals[j] = temp_total;
    
    float temp_average = averages[i];
    averages[i] = averages[j];
    averages[j] = temp_average;
    
    char temp_grade = grades[i];
    grades[i] = grades[j];
    grades[j] = temp_grade;
}

// 7. 简单冒泡排序（按总分降序）
void simple_bubble_sort(char names[][MAX_NAME_LEN], int ids[],
                        float scores[][SUBJECT_COUNT],
                        float totals[], float averages[],
                        char grades[], int count) {
    for (int i = 0; i < count - 1; i++) {
        for (int j = 0; j < count - i - 1; j++) {
            if (totals[j] < totals[j + 1]) {
                swap_students(j, j + 1, names, ids, scores, totals, averages, grades);
            }
        }
    }
    printf("排序完成！\n");
}

// 8. 按姓名搜索
int search_by_name(char names[][MAX_NAME_LEN], char* target_name, int count) {
    for (int i = 0; i < count; i++) {
        if (strcmp(names[i], target_name) == 0) {
            return i; // 找到，返回索引
        }
    }
    return -1; // 未找到
}

// 9. 按学号搜索
int search_by_student_id(char names[][MAX_NAME_LEN], int ids[],
                         int target_id, int count) {
    for (int i = 0; i < count; i++) {
        if (ids[i] == target_id) {
            return i; // 找到，返回索引
        }
    }
    return -1; // 未找到
}

// 10. 按分数区间搜索
void search_by_score_range(char names[][MAX_NAME_LEN], int ids[],
                           float totals[], float averages[], char grades[],
                           int count, float min_score, float max_score) {
    printf("\n=== 在总分区间 [%.1f, %.1f] 内的学生 ===\n", min_score, max_score);
    int found = 0;
    
    for (int i = 0; i < count; i++) {
        if (totals[i] >= min_score && totals[i] <= max_score) {
            printf("%d. 姓名：%s，学号：%d，总分：%.1f，平均分：%.1f，等级：%c\n",
                   found + 1, names[i], ids[i], totals[i], averages[i], grades[i]);
            found++;
        }
    }
    
    if (found == 0) {
        printf("未找到符合条件的学生！\n");
    } else {
        printf("共找到 %d 名学生\n", found);
    }
}

// 11. 递归计算总分和
float recursive_sum_total_scores(char names[][MAX_NAME_LEN],
                                 float totals[], int count, int index) {
    // 递归终止条件
    if (index >= count) {
        return 0.0;
    }
    // 递归关系：当前学生的总分 + 剩余学生的总分和
    return totals[index] + recursive_sum_total_scores(names, totals, count, index + 1);
}

// 12. 递归统计某等级人数
int recursive_count_grade(char names[][MAX_NAME_LEN], char grades[],
                          int count, char target_grade, int index) {
    // 递归终止条件
    if (index >= count) {
        return 0;
    }
    // 递归关系：如果当前学生等级匹配则+1，否则+0
    int current = (grades[index] == target_grade) ? 1 : 0;
    return current + recursive_count_grade(names, grades, count, target_grade, index + 1);
}

// 13. 调试版冒泡排序（打印每趟过程）
void debug_bubble_sort(char names[][MAX_NAME_LEN], int ids[],
                       float scores[][SUBJECT_COUNT],
                       float totals[], float averages[],
                       char grades[], int count) {
    printf("\n=== 调试版冒泡排序过程 ===\n");
    
    for (int i = 0; i < count - 1; i++) {
        printf("\n第 %d 趟排序：\n", i + 1);
        
        for (int j = 0; j < count - i - 1; j++) {
            printf("  比较 %s (%.1f) 和 %s (%.1f)", 
                   names[j], totals[j], names[j+1], totals[j+1]);
            
            if (totals[j] < totals[j + 1]) {
                printf(" -> 交换\n");
                swap_students(j, j + 1, names, ids, scores, totals, averages, grades);
            } else {
                printf(" -> 不交换\n");
            }
        }
        
        // 打印当前数组状态
        printf("当前顺序：");
        for (int k = 0; k < count; k++) {
            printf("%s(%.1f) ", names[k], totals[k]);
        }
        printf("\n");
    }
    printf("排序完成！\n");
}

// 14. 简单系统自检
void simple_system_test(char names[][MAX_NAME_LEN], int ids[],
                        float scores[][SUBJECT_COUNT],
                        float totals[], int count) {
    printf("\n=== 系统自检 ===\n");
    
    // 测试1：检查数组边界
    if (count >= 0 && count <= MAX_STUDENTS) {
        printf("✓ 学生数量检查通过\n");
    } else {
        printf("✗ 学生数量异常\n");
    }
    
    // 测试2：检查分数范围
    int score_valid = 1;
    for (int i = 0; i < count && score_valid; i++) {
        for (int j = 0; j < SUBJECT_COUNT; j++) {
            if (scores[i][j] < 0 || scores[i][j] > 100) {
                score_valid = 0;
                break;
            }
        }
    }
    if (score_valid) {
        printf("✓ 分数范围检查通过\n");
    } else {
        printf("✗ 存在异常分数\n");
    }
    
    // 测试3：检查总分计算
    int total_valid = 1;
    for (int i = 0; i < count; i++) {
        float sum = 0.0;
        for (int j = 0; j < SUBJECT_COUNT; j++) {
            sum += scores[i][j];
        }
        if (sum != totals[i]) {
            total_valid = 0;
            break;
        }
    }
    if (total_valid) {
        printf("✓ 总分计算检查通过\n");
    } else {
        printf("✗ 总分计算有误\n");
    }
    
    printf("系统自检完成！\n");
}

// 15. 辅助函数：重新计算所有学生的总分、平均分和等级
void recalculate_all(char names[][MAX_NAME_LEN],
                     float scores[][SUBJECT_COUNT],
                     float totals[], float averages[], 
                     char grades[], int count) {
    for (int i = 0; i < count; i++) {
        calculate_student_total_average(scores, totals, averages, i);
        grades[i] = calculate_grade(averages[i]);
    }
}

// 主函数：菜单循环
int main(void) {
    char names[MAX_STUDENTS][MAX_NAME_LEN];
    int ids[MAX_STUDENTS];
    float scores[MAX_STUDENTS][SUBJECT_COUNT];
    float totals[MAX_STUDENTS];
    float averages[MAX_STUDENTS];
    char grades[MAX_STUDENTS];
    
    // 初始化系统
    int count = initialize_system(names, ids, scores, totals, averages, grades);
    
    int choice;
    char search_name[MAX_NAME_LEN];
    int search_id;
    float min_score, max_score;
    char target_grade;
    
    do {
        printf("\n========================================\n");
        printf("      学生成绩管理系统（并行数组版）     \n");
        printf("========================================\n");
        printf("1. 添加新学生\n");
        printf("2. 查看单个学生信息\n");
        printf("3. 查看所有学生信息\n");
        printf("4. 计算班级统计信息\n");
        printf("5. 按总分降序排序（简单版）\n");
        printf("6. 按总分降序排序（调试版）\n");
        printf("7. 按姓名搜索\n");
        printf("8. 按学号搜索\n");
        printf("9. 按总分区间搜索\n");
        printf("10. 递归计算总分和\n");
        printf("11. 递归统计某等级人数\n");
        printf("12. 运行系统自检\n");
        printf("13. 重新计算所有学生信息\n");
        printf("0. 退出系统\n");
        printf("========================================\n");
        printf("当前学生数量：%d\n", count);
        printf("请选择操作（0-13）：");
        scanf("%d", &choice);
        
        switch (choice) {
            case 1: // 添加新学生
                count = input_student_info(names, ids, scores, count);
                // 添加后重新计算新学生的总分、平均分和等级
                if (count > 0) {
                    int new_index = count - 1;
                    calculate_student_total_average(scores, totals, averages, new_index);
                    grades[new_index] = calculate_grade(averages[new_index]);
                }
                break;
                
            case 2: // 查看单个学生信息
                if (count == 0) {
                    printf("没有学生数据！\n");
                    break;
                }
                int index;
                printf("请输入学生索引（0-%d）：", count - 1);
                scanf("%d", &index);
                if (index >= 0 && index < count) {
                    display_student_info(index, names, ids, scores, totals, averages, grades);
                } else {
                    printf("索引无效！\n");
                }
                break;
                
            case 3: // 查看所有学生信息
                if (count == 0) {
                    printf("没有学生数据！\n");
                } else {
                    display_all_students_summary(names, ids, scores, totals, averages, grades, count);
                }
                break;
                
            case 4: // 计算班级统计信息
                calculate_class_statistics(names, totals, averages, count);
                break;
                
            case 5: // 简单版排序
                if (count == 0) {
                    printf("没有学生数据！\n");
                } else {
                    simple_bubble_sort(names, ids, scores, totals, averages, grades, count);
                }
                break;
                
            case 6: // 调试版排序
                if (count == 0) {
                    printf("没有学生数据！\n");
                } else {
                    debug_bubble_sort(names, ids, scores, totals, averages, grades, count);
                }
                break;
                
            case 7: // 按姓名搜索
                if (count == 0) {
                    printf("没有学生数据！\n");
                    break;
                }
                printf("请输入要搜索的姓名：");
                scanf("%s", search_name);
                index = search_by_name(names, search_name, count);
                if (index != -1) {
                    printf("找到学生：%s\n", search_name);
                    display_student_info(index, names, ids, scores, totals, averages, grades);
                } else {
                    printf("未找到姓名为 %s 的学生\n", search_name);
                }
                break;
                
            case 8: // 按学号搜索
                if (count == 0) {
                    printf("没有学生数据！\n");
                    break;
                }
                printf("请输入要搜索的学号：");
                scanf("%d", &search_id);
                index = search_by_student_id(names, ids, search_id, count);
                if (index != -1) {
                    printf("找到学号为 %d 的学生\n", search_id);
                    display_student_info(index, names, ids, scores, totals, averages, grades);
                } else {
                    printf("未找到学号为 %d 的学生\n", search_id);
                }
                break;
                
            case 9: // 按总分区间搜索
                if (count == 0) {
                    printf("没有学生数据！\n");
                    break;
                }
                printf("请输入总分下限：");
                scanf("%f", &min_score);
                printf("请输入总分上限：");
                scanf("%f", &max_score);
                if (min_score <= max_score) {
                    search_by_score_range(names, ids, totals, averages, grades, count, min_score, max_score);
                } else {
                    printf("区间下限不能大于上限！\n");
                }
                break;
                
            case 10: // 递归计算总分和
                if (count == 0) {
                    printf("没有学生数据！\n");
                } else {
                    float total_sum = recursive_sum_total_scores(names, totals, count, 0);
                    printf("所有学生的总分和为：%.1f\n", total_sum);
                }
                break;
                
            case 11: // 递归统计等级人数
                if (count == 0) {
                    printf("没有学生数据！\n");
                    break;
                }
                printf("请输入要统计的等级（A/B/C/D/F）：");
                scanf(" %c", &target_grade);
                int grade_count = recursive_count_grade(names, grades, count, target_grade, 0);
                printf("等级为 %c 的学生有 %d 人\n", target_grade, grade_count);
                break;
                
            case 12: // 系统自检
                simple_system_test(names, ids, scores, totals, count);
                break;
                
            case 13: // 重新计算所有学生信息
                if (count == 0) {
                    printf("没有学生数据！\n");
                } else {
                    recalculate_all(names, scores, totals, averages, grades, count);
                    printf("已重新计算所有学生的总分、平均分和等级！\n");
                }
                break;
                
            case 0: // 退出
                printf("感谢使用学生成绩管理系统，再见！\n");
                break;
                
            default:
                printf("无效的选择，请重新输入！\n");
                break;
        }
        
    } while (choice != 0);
    
    return 0;
}
