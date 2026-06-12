input_path = r"/Users/zhangjiawei/Class Code/Python/Python Programming/lab_8/lab_8_1/data936.txt"
output_path = r"/Users/zhangjiawei/Class Code/Python/Python Programming/lab_8/lab_8_1/data936_result.txt"

count_90 = 0
count_80 = 0
count_70 = 0
count_60 = 0
count_fail = 0

f = open(input_path, "r", encoding="utf-8")
lines = f.readlines()
f.close()

result_file = open(output_path, "w", encoding="utf-8")
title = "姓名，平时成绩，期中成绩，期末成绩，总评成绩\n"
result_file.write(title)
print(title)
for line in lines:
    line = line.strip()

    if line == "":
        continue

    parts = line.split(",")

    name = parts[0]
    pingshi = int(parts[1])
    qizhong = int(parts[2])
    qimo = int(parts[3])
    zongping = pingshi * 0.1 +qizhong * 0.3 + qimo * 0.6
    zongping = round(zongping, 1)

    if zongping >= 90:
        count_90 += 1
    elif zongping >= 80:
        count_80 += 1
    elif zongping >= 70:
        count_70 += 1
    elif zongping >= 60:
        count_60 += 1
    else:
        count_fail += 1

    new_line = name + "," + str(pingshi) + "," + str(qizhong) + "," + str(qimo) + "," + str(zongping) + "\n"
    result_file.write(new_line)
    print(new_line)

print("90分以上人数：", count_90)
print("80-89分人数：", count_80)
print("70-79分人数：", count_70)
print("60-69分人数：", count_60)
print("不及格人数：", count_fail)

result_file.write("90分以上人数：" + str(count_90) + "\n")
result_file.write("80-89分人数：" + str(count_80) + "\n")
result_file.write("70-79分人数：" + str(count_70) + "\n")
result_file.write("60-69分人数：" + str(count_60) + "\n")
result_file.write("不及格人数：" + str(count_fail) + "\n")
result_file.close()