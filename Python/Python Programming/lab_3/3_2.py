user_input = input("请输入几个数字（用逗号分隔）: ")
numbers = user_input.split(",")
totle = 0
for i in numbers:
    totle = totle + int(i)
print("输入的数字的和是: %i" %totle)