def factorial(n):
    ret = 1
    for i in range(1 , n + 1):
        ret = ret * i
    return ret

n = int(input("请输入n："))
m = int(input("请输入m："))

result1 = factorial(n)
result2 = factorial(m)
result3 = factorial(n - m)

result = result1 // (result2 * result3)

print("结果为：", result)