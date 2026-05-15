yuanyin = "aeiou"
for i in range(10):
    user_input = input("请输入%i个单词: " % (i + 1))
    if user_input[0] in yuanyin:
        print("输入的单词是以元音字母开头的")
    else:
        print("输入的单词不是以元音字母开头的")