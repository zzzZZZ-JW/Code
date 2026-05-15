//
//  main.c
//  lab_12_1
//
//  Created by 张佳伟 on 2025/12/26.
//

#include <stdio.h>

struct Employee
{
    char name[100];
    int id;
    char department[100];
    int salary;
    int years_of_service;
};

double calculate_average_salary(struct Employee e[] , int size){
      int sum = 0;
      double average;
      for (int i = 0; i < size; i++)
      {
        sum = sum + e[i].salary;
      }
    return average = sum / size;
}

struct Employee employee_Service_Year(struct Employee e[] , int size){
    int max = e[0].years_of_service;
    int index = 0;
    for (int i = 0; i < size; i++) {                                                                                                                                                                                                                                                                            if (e[i].years_of_service > max) {
            max = e[i].years_of_service;
            index = i;
        }
    }
    return e[index];
}

int department_employee_count(struct Employee e[] , int size , char department_name[]){
    int count = 0;
    for(int i = 0; i < size; i++){
        if (e[i].department == department_name) {
            count++;
        } 
    }
    return count;
}

int main(void){
    struct Employee employee[3] = {
        {"A" , 1 , "test1" , 5000 , 1},
        {"B" , 2 , "test2" , 6000 , 2},
        {"C" , 3 , "test1" , 7000 , 3}
    };
    int xuanze;
    printf("1.计算所有员工的平均薪资\n2.找出工龄最长的员工及其信息\n3.统计各部门的员工人数\n4.显示薪资高于平均值的员工列表\n请选择功能：");
    scanf("%d" , &xuanze);

    switch (xuanze){
    case 1:
        {
        printf("平均薪资为：%.2f\n" , calculate_average_salary(employee , 3));
        break;
        }
    case 2:
        {
            struct Employee zuichang = employee_Service_Year(employee , 3);
            printf("工龄最长的员工信息：\n姓名：%s\n工号：%d\n部门：%s\n薪资：%d\n工龄：%d\n" , zuichang.name , zuichang.id , zuichang.department , zuichang.salary , zuichang.years_of_service);
        }
        break;
    case 3:
        {
            char department_name[100];
            printf("请输入要统计的部门名称：");
            scanf("%s" , department_name);
            int count = department_employee_count(employee , 3 , department_name);
            printf("部门%s的员工人数为：%d\n" , department_name , count);
        }
        break;
    case 4:
        {
            double average = calculate_average_salary(employee , 3);
            struct Employee salary_above_average[3];
            printf("薪资高于平均薪资的员工信息：\n");
            for (int i = 0; i < 3; i++)
            {
                if (employee[i].salary > average) {
                    printf("姓名：%s\n工号：%d\n部门：%s\n薪资：%d\n工龄：%d\n" , employee[i].name , employee[i].id , employee[i].department , employee[i].salary , employee[i].years_of_service);
                }
            }
        }
        break;
    }
    return 0;
}