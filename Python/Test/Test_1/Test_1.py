import random

code = ""

for i in range(1, 5):
    shuzi_or_zimu = random.randrange(1, 3)
    if shuzi_or_zimu == 1:
        i = random.randrange(0, 10)
    else:
        i = chr(random.randrange(65, 91))
    code = code + str(i)

print("验证码为：", code)
