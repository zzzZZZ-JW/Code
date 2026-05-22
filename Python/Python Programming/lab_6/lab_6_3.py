def monkey_peach(n):
    if n == 10:
        return 1
    dangqian_peach = 2 * (monkey_peach(n + 1) + 1)
    return dangqian_peach

first_day_total = monkey_peach(1)
print(first_day_total)