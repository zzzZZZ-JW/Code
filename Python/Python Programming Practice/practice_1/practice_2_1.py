import math

a = int(input("请输入第一元二次方程第一个系数："))
b = int(input("请输入第一元二次方程第二个系数："))
c = int(input("请输入第一元二次方程第三个系数："))

x1 = (-b + math.sqrt(b*b - 4*a*c)) / (2*a)
x2 = (-b - math.sqrt(b*b - 4*a*c)) / (2*a)

print("x1=%d,x2=%d" % (x1, x2))