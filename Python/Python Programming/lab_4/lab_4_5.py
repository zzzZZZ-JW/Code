for x in range(0, 101):
    for y in range(0, 101):
        z = 100 - x - y
        if z >= 0 and 5*x +3*y + z/3 == 100:
            print("鸡翁：", x, "鸡母：", y, "鸡雏：", z)