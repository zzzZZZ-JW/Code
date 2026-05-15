user_input = input("请输入一段英文文本：")
word_list = user_input.split()
counts = {}
for word in word_list:
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1

counts_list = list(counts.items())
def get_count(element):
    return element[1]
result = sorted(counts_list, key=get_count, reverse=True)
print(result)
