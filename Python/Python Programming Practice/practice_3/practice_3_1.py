import random

ls1 = [random.randint(60,100) for i in range(70)]
ls2 = []

for num in ls1:
    if num not in ls2:
        ls2.append(num)

ls2.sort()
for num in ls2:
    print(f"{num}出现的次数为:{ls1.count(num)}")