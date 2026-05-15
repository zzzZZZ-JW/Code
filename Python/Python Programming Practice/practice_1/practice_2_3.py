user_input = int(input("请输入一个三位正整数:"))
a = user_input // 100
b = (user_input % 100) // 10
c = user_input % 10
output = a + b + c
print(output)