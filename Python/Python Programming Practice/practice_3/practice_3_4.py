gongsi_a = eval(input("请输入A公司的数据:"))
gongsi_b = eval(input("请输入B公司的数据:"))

all = set(gongsi_a.keys()) | set(gongsi_b.keys())
gongsi_c = {}

for i in all:
    count = gongsi_a.get(i,0) + gongsi_b.get(i,0)
    gongsi_c[i] = count

print(gongsi_c)
