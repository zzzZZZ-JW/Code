score = float(input("请输入成绩:"))
if score>=90 and score<=100:
    print("考试成绩优秀")
elif score>=80 and score<90:
    print("考试成绩良好")
elif score>=70 and score <80:
    print("考试成绩中等")
elif score>=60 and score <70:
    print("考试成绩及格 ")
else:
    print("考试成绩不及格")