# create by 张佳伟
num = int(input("请输入学生数量："))
print("--------------------------")
for i in range(num):
    print("第",i+1,"位学生的奖学金评定开始！")
    score1 = int(input("请输入该学生python成绩："))
    score2 = int(input("请输入该学生database成绩："))

    sum = score1 + score2

    if score1 >= 85 and score2 >= 85 and sum >= 180:
        print("评定结果>>>>【一等奖学金】")
    elif score1 >= 80 and score2 >= 80 and sum >= 170:
        print("评定结果>>>>【二等奖学金】")
    else:
        print("评定结果>>>>【没有奖学金】")

    answer = input("是否继续（continue/quit）？:")
    if answer == "continue":
        continue
    elif answer == "quit":
        break

print("-----所有学生评定完毕-----")
print("2506456052张佳伟")