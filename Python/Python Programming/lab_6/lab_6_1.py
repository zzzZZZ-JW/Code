def is_prime(n):
    if n <= 1:
        return False
    for i in range(2 , n):
        if n % i == 0:
            return False
    return True

for num in range(100 , 1000):
    result = is_prime(num)
    if result == True:
        print(num)