person_count = int(input("请输入人数："))

if person_count <= 5:
    totle = person_count * 160
elif person_count > 5:
    totle = person_count * 140

print("总价为：", totle)