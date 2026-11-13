(() => {
  const extraQuestions = [
    {
      id: "f-r2-notebook-discount",
      type: "fill",
      topic: "basics",
      source: "复习题(2)",
      prompt: "挖空题：文具店笔记本单价 18 元，购买数量不少于 5 本按 9 折计算。补全类型转换和折扣。",
      code: "price = 18\ncount = input(\"请输入购买数量：\")\ncount = __________(count)\n\nif count >= 5:\n    total = price * count * __________\nelse:\n    total = price * count\n\nprint(f\"应付金额：{total:.2f}元\")",
      blanks: [
        { label: "数量转换", answers: ["int"] },
        { label: "折扣", answers: ["0.9", ".9"] }
      ],
      explanation: "input 得到字符串，数量要转 int；9 折就是乘 0.9。"
    },
    {
      id: "c-r2-loop-read",
      type: "choice",
      topic: "basics",
      source: "复习题(2)",
      prompt: "程序阅读：下面程序最终输出什么？",
      code: "total = 0\nfor i in range(2, 8):\n    if i % 3 == 0:\n        total += i\nprint(total)",
      options: [
        { id: "A", text: "3" },
        { id: "B", text: "6" },
        { id: "C", text: "9" },
        { id: "D", text: "12" }
      ],
      answer: "C",
      explanation: "range(2, 8) 包含 2,3,4,5,6,7；能被 3 整除的是 3 和 6，和为 9。"
    },
    {
      id: "d-r2-count-plus",
      type: "debug",
      topic: "basics",
      source: "复习题(2)",
      prompt: "Debug 纠错：程序用于统计及格人数，但有一处错误。写出错误代码和正确代码。",
      code: "scores = [58, 60, 72, 45, 90]\ncount = 0\n\nfor score in scores:\n    if score >= 60:\n        count =+ 1\n\nprint(count)",
      debug: {
        wrongAnswers: ["count =+ 1"],
        fixedAnswers: ["count += 1", "count = count + 1"]
      },
      explanation: "count =+ 1 是把 +1 赋给 count，不是累加；累加应写 count += 1。"
    },
    {
      id: "code-r2-list-filter-sort",
      type: "code",
      topic: "collections",
      source: "复习题(2)",
      prompt: "补全编程：将 scores 中不低于 60 分的成绩保存到 passed，并按从高到低输出。",
      code: "scores = [49, 85, 62, 91, 58, 73]\npassed = []\n\n# 请补全代码\n\nprint(passed)",
      criteria: [
        { label: "遍历 scores", points: 20, all: ["for\\s+score\\s+in\\s+scores"] },
        { label: "判断 score >= 60", points: 20, all: ["score\\s*>=\\s*60"] },
        { label: "使用 append 加入 passed", points: 25, all: ["passed\\.append\\s*\\(\\s*score\\s*\\)"] },
        { label: "按降序排序", points: 25, any: ["passed\\.sort\\s*\\([^\\)]*reverse\\s*=\\s*True", "sorted\\s*\\(\\s*passed\\s*,[^\\)]*reverse\\s*=\\s*True"] },
        { label: "输出 passed", points: 10, all: ["print\\s*\\(\\s*passed\\s*\\)"] }
      ],
      sampleAnswer: "for score in scores:\n    if score >= 60:\n        passed.append(score)\n\npassed.sort(reverse=True)\nprint(passed)",
      explanation: "列表筛选题的核心是遍历、条件判断、append 和 sort(reverse=True)。"
    },
    {
      id: "code-r2-book-category-count",
      type: "code",
      topic: "collections",
      source: "复习题(2)",
      prompt: "补全编程：统计图书类别出现次数，结果保存到 book_count 字典中并输出。",
      code: "books = [\"文学\", \"计算机\", \"文学\", \"历史\", \"计算机\", \"文学\", \"艺术\"]\nbook_count = {}\n\n# 请补全代码",
      criteria: [
        { label: "遍历 books", points: 20, all: ["for\\s+book\\s+in\\s+books"] },
        { label: "使用字典 book_count", points: 20, all: ["book_count\\s*=\\s*\\{\\}|book_count\\["] },
        { label: "使用 get 默认 0 统计", points: 35, all: ["book_count\\.get\\s*\\(\\s*book\\s*,\\s*0\\s*\\)\\s*\\+\\s*1"] },
        { label: "回写到 book_count[book]", points: 15, all: ["book_count\\s*\\[\\s*book\\s*\\]\\s*="] },
        { label: "输出统计结果", points: 10, all: ["print\\s*\\(\\s*book_count\\s*\\)"] }
      ],
      sampleAnswer: "for book in books:\n    book_count[book] = book_count.get(book, 0) + 1\n\nprint(book_count)",
      explanation: "字典统计题最稳的模板是 d[key] = d.get(key, 0) + 1。"
    },
    {
      id: "f-r2-set-unique",
      type: "fill",
      topic: "collections",
      source: "复习题(2)",
      prompt: "挖空题：活动签到名单有重复，去重并输出实际签到人数。",
      code: "names = [\"张三\", \"李四\", \"王五\", \"张三\", \"赵六\", \"李四\", \"钱七\"]\nunique_names = ______(names)\nprint(unique_names)\nprint(______(unique_names))",
      blanks: [
        { label: "去重函数", answers: ["set"] },
        { label: "计数函数", answers: ["len"] }
      ],
      explanation: "set 可去除重复元素，len 统计集合中的不同姓名数。"
    },
    {
      id: "f-r2-student-lambda",
      type: "fill",
      topic: "collections",
      source: "复习题(2)",
      prompt: "挖空题：按学生成绩从高到低排序。",
      code: "students = [(\"张三\", 86), (\"李四\", 92), (\"王五\", 78), (\"赵六\", 95)]\nresult = sorted(students, key=lambda x: x[__________], reverse=__________)\nprint(result)",
      blanks: [
        { label: "成绩索引", answers: ["1"] },
        { label: "降序参数", answers: ["True", "true"] }
      ],
      explanation: "成绩是元组第 2 项，索引为 1；reverse=True 表示降序。"
    },
    {
      id: "f-r2-csv-reader",
      type: "fill",
      topic: "files",
      source: "复习题(2)",
      prompt: "挖空题：读取 scores.csv，第一行为表头，后续每行依次为学号、姓名、成绩。补全跳过表头与索引。",
      code: "import csv\n\nwith open(\"scores.csv\", \"r\", encoding=\"utf-8\") as f:\n    reader = csv.__________(f)\n    __________(reader)\n    for row in reader:\n        name = row[__________]\n        score = row[__________]\n        print(name, score)",
      blanks: [
        { label: "CSV 读取器", answers: ["reader"] },
        { label: "跳过表头", answers: ["next"] },
        { label: "姓名索引", answers: ["1"] },
        { label: "成绩索引", answers: ["2"] }
      ],
      explanation: "csv.reader(f) 逐行返回列表；next(reader) 跳过表头；姓名和成绩分别在索引 1、2。"
    },
    {
      id: "d-r2-dict-get-default",
      type: "debug",
      topic: "collections",
      source: "复习题(2)",
      prompt: "Debug 纠错：下面统计类别次数的代码第一次遇到某类别会报错。写出错误代码和正确代码。",
      code: "book_count = {}\nfor book in books:\n    book_count[book] = book_count.get(book) + 1",
      debug: {
        wrongAnswers: ["book_count[book] = book_count.get(book) + 1"],
        fixedAnswers: ["book_count[book] = book_count.get(book, 0) + 1"]
      },
      explanation: "get(book) 找不到键时返回 None，None + 1 会报错；应提供默认值 0。"
    },
    {
      id: "d-r2-tk-command-call",
      type: "debug",
      topic: "tkinter",
      source: "复习题(2)",
      prompt: "Debug 纠错：按钮创建时写成 command=show_text() 会提前执行函数。写出错误代码和正确代码。",
      code: "button = tk.Button(root, text=\"显示\", command=show_text())",
      debug: {
        wrongAnswers: ["command=show_text()", "button = tk.Button(root, text=\"显示\", command=show_text())"],
        fixedAnswers: ["command=show_text", "button = tk.Button(root, text=\"显示\", command=show_text)"]
      },
      explanation: "command 需要传函数对象，不要加括号；加括号会在创建按钮时立即调用。"
    },
    {
      id: "d-r2-list-append-extend",
      type: "debug",
      topic: "collections",
      source: "复习题(2)",
      prompt: "Debug 纠错：向列表 passed 加入一个成绩时，下面写法不合适。写出错误代码和正确代码。",
      code: "passed.extend(score)",
      debug: {
        wrongAnswers: ["passed.extend(score)"],
        fixedAnswers: ["passed.append(score)"]
      },
      explanation: "append 添加一个元素；extend 用于把可迭代对象逐项展开加入列表。score 是单个整数，应用 append。"
    },
    {
      id: "code-r2-print-kind-fee",
      type: "code",
      topic: "integrated",
      source: "复习题(2)",
      prompt: "综合编程：输入打印页数和打印类型。黑白每页 0.3 元，彩色每页 1 元；pages<=0 输出“页数错误”；类型不是“黑白”或“彩色”输出“类型错误”；否则输出金额并保留两位小数。",
      criteria: [
        { label: "使用 input 读取页数和类型", points: 15, all: ["input\\s*\\(", "print_type|ptype|kind|type"] },
        { label: "使用 int 转换页数", points: 15, all: ["int\\s*\\(\\s*input|pages\\s*=\\s*int\\s*\\("] },
        { label: "判断 pages <= 0 并输出页数错误", points: 20, all: ["pages\\s*<=\\s*0", "页数错误"] },
        { label: "处理黑白打印 0.3 元", points: 20, all: ["黑白", "0\\.3|\\.3"] },
        { label: "处理彩色打印 1 元", points: 15, all: ["彩色", "pages\\s*\\*\\s*1|money\\s*=\\s*pages"] },
        { label: "处理类型错误", points: 10, all: ["类型错误"] },
        { label: "金额保留两位小数", points: 5, all: [":\\.2f"] }
      ],
      sampleAnswer: "pages = int(input(\"请输入打印页数：\"))\nprint_type = input(\"请输入打印类型（黑白/彩色）：\")\n\nif pages <= 0:\n    print(\"页数错误\")\nelif print_type == \"黑白\":\n    money = pages * 0.3\n    print(f\"应付金额：{money:.2f}元\")\nelif print_type == \"彩色\":\n    money = pages * 1\n    print(f\"应付金额：{money:.2f}元\")\nelse:\n    print(\"类型错误\")",
      explanation: "这题同时考输入、类型转换、分支顺序和格式化输出。"
    },
    {
      id: "code-r2-grade-levels",
      type: "code",
      topic: "collections",
      source: "复习题(2)",
      prompt: "综合编程：给定 scores，使用字典统计优秀、良好、及格、不及格人数，并输出平均分。",
      criteria: [
        { label: "使用列表保存 scores", points: 10, all: ["scores\\s*=\\s*\\["] },
        { label: "使用字典保存等级人数", points: 20, all: ["levels\\s*=\\s*\\{", "优秀", "良好", "及格", "不及格"] },
        { label: "遍历成绩", points: 15, all: ["for\\s+score\\s+in\\s+scores"] },
        { label: "按 90/80/60 分支统计", points: 25, all: ["score\\s*>=\\s*90", "score\\s*>=\\s*80", "score\\s*>=\\s*60"] },
        { label: "用 sum 和 len 计算平均分", points: 20, all: ["sum\\s*\\(\\s*scores\\s*\\)", "len\\s*\\(\\s*scores\\s*\\)"] },
        { label: "平均分保留两位小数", points: 10, all: [":\\.2f"] }
      ],
      sampleAnswer: "scores = [95, 86, 72, 59, 88, 61, 100]\nlevels = {\"优秀\": 0, \"良好\": 0, \"及格\": 0, \"不及格\": 0}\n\nfor score in scores:\n    if score >= 90:\n        levels[\"优秀\"] += 1\n    elif score >= 80:\n        levels[\"良好\"] += 1\n    elif score >= 60:\n        levels[\"及格\"] += 1\n    else:\n        levels[\"不及格\"] += 1\n\naverage = sum(scores) / len(scores)\nprint(levels)\nprint(f\"平均分：{average:.2f}\")",
      explanation: "这类题很像期末综合题：列表、字典、循环、分支、内置函数一起考。"
    },
    {
      id: "code-r2-club-dedupe",
      type: "code",
      topic: "collections",
      source: "复习题(2)",
      prompt: "综合编程：社团报名记录中有重复的完全相同报名信息。先去重，再统计每个社团报名人数，并输出实际报名学生人数。",
      criteria: [
        { label: "使用 set 对 records 去重", points: 20, all: ["set\\s*\\(\\s*records\\s*\\)"] },
        { label: "使用字典统计社团人数", points: 20, all: ["club_count\\s*=\\s*\\{", "club_count\\.get\\s*\\("] },
        { label: "使用集合保存学生姓名", points: 20, all: ["students\\s*=\\s*set\\s*\\(", "students\\.add\\s*\\("] },
        { label: "解包遍历 name, club", points: 15, all: ["for\\s+name\\s*,\\s*club\\s+in"] },
        { label: "输出每个社团人数", points: 15, all: ["for\\s+club\\s*,\\s*count\\s+in\\s+club_count\\.items\\s*\\("] },
        { label: "输出实际报名学生人数", points: 10, all: ["len\\s*\\(\\s*students\\s*\\)", "实际报名学生人数"] }
      ],
      sampleAnswer: "unique_records = set(records)\nclub_count = {}\nstudents = set()\n\nfor name, club in unique_records:\n    club_count[club] = club_count.get(club, 0) + 1\n    students.add(name)\n\nfor club, count in club_count.items():\n    print(club, count)\nprint(\"实际报名学生人数：\", len(students))",
      explanation: "完全相同记录去重用 set(records)；实际人数要按姓名集合统计。"
    },
    {
      id: "code-r2-calc-fee",
      type: "code",
      topic: "functions",
      source: "复习题(2)",
      prompt: "综合编程：定义 calc_fee(weight)，重量小于等于 0 返回“重量错误”；小于等于 1 千克收费 8 元；超过 1 千克后超出部分每千克加收 3 元。",
      criteria: [
        { label: "定义 calc_fee(weight)", points: 20, all: ["def\\s+calc_fee\\s*\\(\\s*weight\\s*\\)"] },
        { label: "非法重量返回字符串", points: 20, all: ["weight\\s*<=\\s*0", "return\\s+[\"']重量错误[\"']"] },
        { label: "1 千克以内返回 8", points: 15, all: ["weight\\s*<=\\s*1", "return\\s+8"] },
        { label: "超过部分按每千克 3 元", points: 20, all: ["8\\s*\\+\\s*\\(\\s*weight\\s*-\\s*1\\s*\\)\\s*\\*\\s*3"] },
        { label: "使用 return 返回结果", points: 10, all: ["return"] },
        { label: "测试代码调用函数并格式化输出", points: 15, all: ["calc_fee\\s*\\(", ":\\.2f"] }
      ],
      sampleAnswer: "def calc_fee(weight):\n    if weight <= 0:\n        return \"重量错误\"\n    elif weight <= 1:\n        return 8\n    else:\n        return 8 + (weight - 1) * 3\n\nweight = float(input(\"请输入重量（千克）：\"))\nfee = calc_fee(weight)\n\nif isinstance(fee, str):\n    print(fee)\nelse:\n    print(f\"快递费用：{fee:.2f}元\")",
      explanation: "函数封装题重点是参数、分支、return，以及调用后的输出处理。"
    },
    {
      id: "code-r2-book-order",
      type: "code",
      topic: "oop",
      source: "复习题(2)",
      prompt: "综合编程：定义 BookOrder 类，包含书名、单价、数量、是否会员；total() 返回订单金额，会员 9 折；show() 输出订单信息。",
      criteria: [
        { label: "定义 BookOrder 类", points: 15, all: ["class\\s+BookOrder\\s*:"] },
        { label: "__init__ 含 book、price、count、is_member", points: 20, all: ["def\\s+__init__\\s*\\(\\s*self\\s*,\\s*book\\s*,\\s*price\\s*,\\s*count\\s*,\\s*is_member\\s*\\)", "self\\.book", "self\\.price", "self\\.count", "self\\.is_member"] },
        { label: "total 方法计算 price * count", points: 15, all: ["def\\s+total\\s*\\(\\s*self\\s*\\)", "self\\.price\\s*\\*\\s*self\\.count"] },
        { label: "会员 9 折", points: 15, all: ["if\\s+self\\.is_member", "0\\.9|\\.9"] },
        { label: "show 方法输出订单信息", points: 20, all: ["def\\s+show\\s*\\(\\s*self\\s*\\)", "书名", "订单金额", "self\\.total\\s*\\("] },
        { label: "创建对象并调用 show", points: 15, all: ["BookOrder\\s*\\(", "\\.show\\s*\\("] }
      ],
      sampleAnswer: "class BookOrder:\n    def __init__(self, book, price, count, is_member):\n        self.book = book\n        self.price = price\n        self.count = count\n        self.is_member = is_member\n\n    def total(self):\n        money = self.price * self.count\n        if self.is_member:\n            money *= 0.9\n        return money\n\n    def show(self):\n        print(f\"书名：{self.book}\")\n        print(f\"单价：{self.price:.2f}元\")\n        print(f\"数量：{self.count}\")\n        print(f\"是否会员：{self.is_member}\")\n        print(f\"订单金额：{self.total():.2f}元\")\n\norder = BookOrder(\"Python程序设计\", 58, 2, True)\norder.show()",
      explanation: "类题常考 __init__、实例属性、方法调用、self.total() 组合使用。"
    },
    {
      id: "code-r2-csv-score-process",
      type: "code",
      topic: "files",
      source: "复习题(2)",
      prompt: "综合编程：读取 students.csv，跳过表头，输出成绩不低于 80 分的学生姓名和成绩，并计算全班平均分。",
      criteria: [
        { label: "导入 csv 模块", points: 10, all: ["import\\s+csv"] },
        { label: "with open 读取 UTF-8 文件", points: 15, all: ["with\\s+open\\s*\\(", "encoding\\s*=\\s*[\"']utf-8[\"']"] },
        { label: "使用 csv.reader", points: 15, all: ["csv\\.reader\\s*\\("] },
        { label: "使用 next(reader) 跳过表头", points: 15, all: ["next\\s*\\(\\s*reader\\s*\\)"] },
        { label: "成绩转 int", points: 15, all: ["int\\s*\\(\\s*row\\s*\\[\\s*2\\s*\\]\\s*\\)"] },
        { label: "判断 score >= 80 并输出姓名成绩", points: 15, all: ["score\\s*>=\\s*80", "print\\s*\\("] },
        { label: "累计 total/count 并输出平均分", points: 15, all: ["total\\s*(\\+=|=\\s*total\\s*\\+)", "count\\s*(\\+=|=\\s*count\\s*\\+)", "average"] }
      ],
      sampleAnswer: "import csv\n\ntotal = 0\ncount = 0\n\nwith open(\"students.csv\", \"r\", encoding=\"utf-8\") as f:\n    reader = csv.reader(f)\n    next(reader)\n    for row in reader:\n        name = row[1]\n        score = int(row[2])\n        total += score\n        count += 1\n        if score >= 80:\n            print(name, score)\n\nif count > 0:\n    average = total / count\n    print(f\"平均分：{average:.2f}\")\nelse:\n    print(\"没有成绩数据\")",
      explanation: "CSV 文件题会把文件、列表索引、类型转换、条件筛选和平均值揉在一起。"
    },
    {
      id: "code-r2-jieba-counter",
      type: "code",
      topic: "wordcloud",
      source: "复习题(2)",
      prompt: "综合编程：读取 course_comments.txt，去除常见标点，使用 jieba.lcut 分词，过滤长度小于 2 的词和停用词，用 Counter 统计词频并输出。",
      criteria: [
        { label: "导入 jieba 和 Counter", points: 20, all: ["import\\s+jieba", "from\\s+collections\\s+import\\s+Counter"] },
        { label: "读取文本文件全部内容", points: 15, all: ["open\\s*\\(.+course_comments\\.txt", "\\.read\\s*\\("] },
        { label: "去除或替换常见标点", points: 15, any: ["replace\\s*\\(", "re\\.sub\\s*\\("] },
        { label: "使用 jieba.lcut", points: 15, all: ["jieba\\.lcut\\s*\\("] },
        { label: "过滤短词和停用词", points: 20, all: ["len\\s*\\(\\s*w\\s*\\)\\s*>=\\s*2|len\\s*\\(.+\\)\\s*>=\\s*2", "stop_words"] },
        { label: "使用 Counter 和 most_common 输出", points: 15, all: ["Counter\\s*\\(", "\\.most_common\\s*\\("] }
      ],
      sampleAnswer: "import jieba\nfrom collections import Counter\n\nwith open(\"course_comments.txt\", \"r\", encoding=\"utf-8\") as f:\n    text = f.read()\n\npunctuations = \"，。！？；：“”‘’、,.!?;:\\\"'()（）\\n\\t\"\nfor p in punctuations:\n    text = text.replace(p, \" \")\n\nstop_words = {\"的\", \"了\", \"是\", \"我\", \"也\", \"很\", \"和\", \"在\", \"有\", \"就\"}\nwords = jieba.lcut(text)\nfiltered = [w for w in words if len(w) >= 2 and w not in stop_words]\nword_count = Counter(filtered)\n\nfor word, count in word_count.most_common():\n    print(word, count)",
      explanation: "这题比词云更偏文本处理：清洗、分词、过滤、Counter 统计。"
    },
    {
      id: "code-r2-tkinter-entry-label",
      type: "code",
      topic: "tkinter",
      source: "复习题(2)",
      prompt: "综合编程：使用 tkinter 写一个简单窗口，包含输入框、按钮和标签。点击按钮后，将输入框内容显示到标签中。",
      criteria: [
        { label: "导入 tkinter 并创建 root", points: 15, all: ["import\\s+tkinter\\s+as\\s+tk", "root\\s*=\\s*tk\\.Tk\\s*\\("] },
        { label: "定义 show_text 回调函数", points: 15, all: ["def\\s+show_text\\s*\\("] },
        { label: "使用 entry.get 获取输入", points: 15, all: ["entry\\.get\\s*\\("] },
        { label: "使用 label.config 修改标签", points: 15, all: ["label\\.config\\s*\\("] },
        { label: "创建 Entry、Button、Label", points: 25, all: ["tk\\.Entry\\s*\\(", "tk\\.Button\\s*\\(", "tk\\.Label\\s*\\("] },
        { label: "Button 使用 command 绑定函数对象", points: 10, all: ["command\\s*=\\s*show_text"] },
        { label: "启动 mainloop", points: 5, all: ["root\\.mainloop\\s*\\("] }
      ],
      sampleAnswer: "import tkinter as tk\n\ndef show_text():\n    text = entry.get()\n    label.config(text=text)\n\nroot = tk.Tk()\nroot.title(\"输入显示\")\n\nentry = tk.Entry(root)\nentry.pack(padx=20, pady=10)\n\nbutton = tk.Button(root, text=\"显示\", command=show_text)\nbutton.pack(pady=5)\n\nlabel = tk.Label(root, text=\"\")\nlabel.pack(padx=20, pady=10)\n\nroot.mainloop()",
      explanation: "Tkinter 小题常考：控件创建、pack 布局、command 绑定、get/config。"
    }
  ];

  window.REVIEW_QUESTIONS.push(...extraQuestions);
})();
