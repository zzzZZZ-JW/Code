score1 = int(input("请输入第一门课成绩："))
score2 = int(input("请输入第二门课成绩："))

sum = score1 + score2

if score1 >= 85 and score2 >= 85 and sum >= 180:
    print("获得一等奖学金")
elif score1 >= 80 and score2 >= 80 and sum >= 170:
    print("获得二等奖学金")
else:
    print("没有奖学金")
