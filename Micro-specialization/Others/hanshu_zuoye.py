# create by 张佳伟

def if_tax(base_salary , bonus):
    gongzi = base_salary + bonus

    if (gongzi > 5000) and (gongzi < 15000):
        shui = (gongzi - 5000)*0.05
        print("需缴税", shui,"元")
    elif (gongzi > 15000):
        shui = (gongzi - 10000)*0.05 + 250
        print("需缴税", shui,"元")
    else:
        print("无需缴税")

answer = "yes"
while answer == "yes":
    base_salary = int(input("请输入base_salary:"))
    bonus = int(input("请输入bonus:"))

    if_tax(base_salary, bonus)

    answer = input("是否继续(yes/no):")
    if answer == "no":
        break

print("张佳伟2506456052")

