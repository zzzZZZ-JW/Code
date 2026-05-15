user_input = input("请输入: ")

zimu = 0
shuzi = 0
qita = 0

for i in user_input:
    if i.isalpha() == True:
        zimu += 1
    elif i.isdigit() == True:
        shuzi += 1
    else:
        qita += 1

print("字母有%d个" %zimu)
print("数字有%d个" %shuzi)
print("其他有%d个" %qita)