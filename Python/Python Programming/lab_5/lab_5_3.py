score = "65,92,78,70,94,48,73,81,93,97,95,50,46,71,98,63,85,100,61,56,73,98,68,76,71,55,91,87,53,46,49,58,62,76,98,48,63,78,70,80"
split_score = score.split(",")
list_score = []

for i in split_score:
    num = int(i)
    list_score.append(num)

count_yx = 0
count_lh = 0
count_zd = 0
count_jg = 0
count_bjg = 0

for j in list_score:
    if j >= 90:
        count_yx += 1
    elif j >= 80:
        count_lh += 1
    elif j >= 70:
        count_zd += 1
    elif j >= 60:
        count_jg += 1
    else:
        count_bjg += 1

totle = len(list_score)
print(f"优秀：{count_yx}人，占比{count_yx/totle:.2%}")
print(f"良好：{count_lh}人，占比{count_lh/totle:.2%}")
print(f"中等：{count_zd}人，占比{count_zd/totle:.2%}")
print(f"及格：{count_jg}人，占比{count_jg/totle:.2%}")
print(f"不及格：{count_bjg}人，占比{count_bjg/totle:.2%}")