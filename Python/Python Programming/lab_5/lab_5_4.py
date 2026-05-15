geshou1 = {1, 2, 3, 4, 5}
geshou2 = {6, 7, 8, 9, 10}
toupiao = [4, 7, 9, 1, 2, 2, 6, 2, 2, 1, 6, 9, 7, 4, 5, 5, 7, 9, 5, 5, 4]

all_toupiao_set = set(toupiao)
toupiao_in_geshou1 = all_toupiao_set & geshou1
toupiao_in_geshou2 = all_toupiao_set & geshou2

list_all = sorted(all_toupiao_set)
list_geshou1 = sorted(toupiao_in_geshou1)
list_geshou2 = sorted(toupiao_in_geshou2)

print(list_all)
print(list_geshou1)
print(list_geshou2)
