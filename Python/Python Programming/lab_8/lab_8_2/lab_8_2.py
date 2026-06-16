input_path = "/Users/zhangjiawei/Class Code/Python/Python Programming/lab_8/lab_8_2/data935.txt"
output_path = "/Users/zhangjiawei/Class Code/Python/Python Programming/lab_8/lab_8_2/data935_output.txt"

votes = {}
f = open(input_path, "r", encoding="utf-8")
lines = f.readlines()
f.close()

for line in lines:
    name = line.strip()
    if name == "":
        continue
    if name in votes:
        votes[name] += 1
    else:
        votes[name] = 1

votes_list = []

for name in votes:
    one_person = (name, votes[name])
    votes_list.append(one_person)

for i in range(len(votes_list)):
    for j in range(0, len(votes_list) - 1 - i):
        if votes_list[i][1] < votes_list[j+1][1]:
            temp = votes_list[i]
            votes_list[i] = votes_list[j+1]
            votes_list[j+1] = temp

f = open(output_path, "w", encoding="utf-8")

for item in votes_list:
    name = item[0]
    count = item[1]
    result = name + " 得票 " + str(count)
    print(result)
    f.write(result + "\n")

f.close()