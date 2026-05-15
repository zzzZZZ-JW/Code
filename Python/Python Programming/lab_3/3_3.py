islower = False
isupper = False
changdu = False
hasdigit = False

while True:
    password = input("请输入一个密码: ")

    if len(password) >= 6:
        changdu = True
    else:
        print("不少于6位")
        continue

    islower = False
    isupper = False
    hasdigit = False

    for i in password:
        if i.islower():
            islower = True
        if i.isupper():
            isupper = True
        if i.isdigit():
            hasdigit = True

    if islower == False:
        print("必须包含小写字母")
        continue

    if isupper == False:
        print("必须包含大写字母")
        continue

    if hasdigit == False:
        print("必须包含数字")
        continue

    break

queren = False
while queren == False:
    password2 = input("请再次输入密码: ")
    if password2 == password:
        queren = True
    else:
        print("两次输入的密码不一致")