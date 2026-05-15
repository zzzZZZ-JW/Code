import random

code = ""

for i in range(1, 7):
    shuzi_or_zimu = random.randrange(1, 4)
    if shuzi_or_zimu == 1:
        i = random.randrange(0, 10)
    elif shuzi_or_zimu == 2:
        i = chr(random.randrange(65, 91))
    else:
        i = chr(random.randrange(97, 123))
    code = code + str(i)

print("验证码为：", code)