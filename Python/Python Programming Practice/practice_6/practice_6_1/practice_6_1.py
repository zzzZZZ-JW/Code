import jieba
text = "工业互联网是智改数转新趋势下实现智能制造的关键"
result1 = jieba.lcut(text)
print(result1)

jieba.add_word("工业互联网")
jieba.add_word("智能制造")
result2 = jieba.lcut(text)
print(result2)

jieba.del_word("改数")
result3 = jieba.lcut(text)
print(result3)

jieba.load_userdict("userdict.txt")
result4 = jieba.lcut(text)
print(result4)