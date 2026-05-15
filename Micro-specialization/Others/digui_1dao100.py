# create by 张佳伟
def factorial(num):
    if num == 1:
        return 1
    else:
        return num + factorial(num - 1)
result = factorial(100)
print(result)