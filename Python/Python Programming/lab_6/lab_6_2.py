def GCD(a,b):
    while b != 0:
        i = a % b
        a = b
        b = i
    return a

def LCM(a,b):
    gcd = GCD(a,b)
    lcm = (a * b) // gcd
    return lcm

num1 = int(input("请输入第一个整数: "))
num2 = int(input("请输入第二个整数: "))
print(GCD(num1,num2))
print(LCM(num1,num2))