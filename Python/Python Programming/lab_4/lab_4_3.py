num1=int(input("请输入第一个数："))
num2=int(input("请输入第二个数："))

for i in range(1,num2+1):
    if num1%i==0 and num2%i==0:
        result = i
print(result)