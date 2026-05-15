def get_weishu(num):
    return len(str(num))

def result(num):
    result = 0
    for i in str(num):
        result = result + int(i) ** get_weishu(num)
    return result

def narcissistic_number(num):
    if num == result(num):
        return True
    else:
        return False
    
if __name__ == "__main__":
    for i in range(1, 10000000000): #循环1~10位数
        if narcissistic_number(i):       #如果i是自幂数，打印输出
            print(i)
