name1 =input("请输入同学的姓名：")
num1 = input("请输入同学的课程1成绩：")
num2 = input("请输入同学的课程2成绩：")
num3 = input("请输入同学的课程3成绩：")
num4 = input("请输入同学的课程4成绩：")

sum1 = int(num1) + int(num2) + int(num3) + int(num4)
average = sum1 / 4

print("**** 2022 年期末成绩单****")
print("姓名     科目1      科目2      科目3      科目4            总成绩          平均分")
print(name1,"  ",num1,"      ",num2,"      ",num3,"      ",num4,"              ",sum1,"          ",average)