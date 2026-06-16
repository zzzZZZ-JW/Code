input_path = "data.txt"

salary = {}

f = open(input_path, "r", encoding="utf-8")
lines = f.readlines()
f.close()

for line in lines:
    line = line.strip()
    if line == "":
        continue
    data = eval(line)
    sid = data["sid"]
    salary_7 = data["7月"]
    salary_8 = data["8月"]
    salary_9 = data["9月"]
    average = (salary_7 + salary_8 + salary_9) // 3
    salary[sid] = [salary_8, salary_7, salary_9, average]

keys = list(salary.keys())
keys.sort()

for key in keys:
    print(key, salary[key])