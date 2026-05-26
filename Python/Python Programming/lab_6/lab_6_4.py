def min_n(a, b, *c):
    current_min = a
    if b < current_min:
        current_min = b
    for num in c:
        if num < current_min:
            current_min = num
    return current_min

result1 = min_n(8, 2)
print("最小值为", result1)

result2 = min_n(16, 1, 7, 4, 15)
print("最小值为", result2)