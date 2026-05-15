word = str(input("请输入一段英文："))
count = {}
for i in word:
    count[i] = count.get(i,0) + 1
list1 = list(count.items())
list1.sort(key=lambda x:x[1] , reverse=True)

for i,count in list1:
    if i == " ":
        print(f"  {count} <这个是空格>")
    else:
        print(f"{i} {count}")
