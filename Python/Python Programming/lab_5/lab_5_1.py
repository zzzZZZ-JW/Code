print("请输入5名选手的得分：")
for i in range(1,6):
    user_input = input()
    score = user_input.split(",")
    score_list = []
    for j in score:
        score_list.append(float(j))
    max_score = max(score_list)
    min_score = min(score_list)
    sum_score = sum(score_list)
    average_score = (sum_score - max_score - min_score) / 6
    print(f"{average_score:.2f}")
