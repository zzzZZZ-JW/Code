import random

ls = list()
while len(ls) < 40:
    num = random.randint(40,100)
    if num not in ls:
        ls.append(num)
    if len(ls) == 40:
        break
print(ls)