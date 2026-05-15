for i in range(2, 101):
    is_zhishu = True

    for j in range(2, i):
        if i % j == 0:
            is_zhishu = False
            break
    if is_zhishu:
        print(i)