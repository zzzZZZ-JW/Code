window.REVIEW_TOPICS = [
  { id: "basics", name: "基础语法与控制结构" },
  { id: "collections", name: "列表·元组·字典·集合" },
  { id: "functions", name: "函数与模块" },
  { id: "oop", name: "类与对象" },
  { id: "files", name: "文件处理" },
  { id: "wordcloud", name: "分词与词云图" },
  { id: "tkinter", name: "图形界面开发" },
  { id: "integrated", name: "综合应用" }
];

window.REVIEW_QUESTIONS = [
  {
    id: "c-sample-sorted-lambda",
    type: "choice",
    topic: "collections",
    source: "样卷",
    prompt: "某程序需要按图书借阅次数从高到低排序，程序输出结果是？",
    code: "books = [(\"Python\", 18), (\"AI\", 25), (\"Data\", 12)]\nresult = sorted(books, key=lambda x: x[1], reverse=True)\nprint(result[0])",
    options: [
      { id: "A", text: "(\"Python\", 18)" },
      { id: "B", text: "(\"AI\", 25)" },
      { id: "C", text: "(\"Data\", 12)" },
      { id: "D", text: "25" }
    ],
    answer: "B",
    explanation: "key=lambda x: x[1] 按元组第 2 项排序，reverse=True 表示降序，最大借阅次数是 25。"
  },
  {
    id: "c-sample-list-index",
    type: "choice",
    topic: "collections",
    source: "样卷",
    prompt: "阅读代码，程序输出结果是？",
    code: "data = [\"apple\", \"banana\", \"orange\", \"pear\"]\ndata[1] = \"grape\"\nprint(data[-2])",
    options: [
      { id: "A", text: "banana" },
      { id: "B", text: "grape" },
      { id: "C", text: "orange" },
      { id: "D", text: "pear" }
    ],
    answer: "C",
    explanation: "data[1] 被改为 grape，data[-2] 是倒数第二个元素 orange。"
  },
  {
    id: "c-sample-range",
    type: "choice",
    topic: "basics",
    source: "样卷",
    prompt: "阅读 for 循环代码，程序输出结果是？",
    code: "total = 0\nfor n in range(2, 10, 3):\n    total += n\nprint(total)",
    options: [
      { id: "A", text: "9" },
      { id: "B", text: "12" },
      { id: "C", text: "15" },
      { id: "D", text: "20" }
    ],
    answer: "C",
    explanation: "range(2, 10, 3) 依次产生 2、5、8，和为 15。"
  },
  {
    id: "c-sample-dict-get",
    type: "choice",
    topic: "collections",
    source: "样卷",
    prompt: "某程序用字典保存图书库存数量，程序输出结果是？",
    code: "books = {\"Python入门\": 5, \"数据分析\": 3}\ncount = books.get(\"人工智能\", 0)\nprint(count)",
    options: [
      { id: "A", text: "0" },
      { id: "B", text: "None" },
      { id: "C", text: "人工智能" },
      { id: "D", text: "程序报错，因为字典中没有这个键" }
    ],
    answer: "A",
    explanation: "dict.get(key, default) 在键不存在时返回默认值 0。"
  },
  {
    id: "c-sample-file-append",
    type: "choice",
    topic: "files",
    source: "样卷",
    prompt: "某程序希望在不清空原内容的情况下，把一条记录写到 record.txt 文件末尾。文件打开模式应选择？",
    options: [
      { id: "A", text: "\"r\"" },
      { id: "B", text: "\"w\"" },
      { id: "C", text: "\"a\"" },
      { id: "D", text: "\"rb\"" }
    ],
    answer: "C",
    explanation: "\"a\" 是追加写入模式，\"w\" 会覆盖原文件。"
  },
  {
    id: "f-sample-input-types",
    type: "fill",
    topic: "basics",
    source: "样卷",
    prompt: "补全代码：图书单价可能带小数，购买数量应为整数。",
    code: "price = ______(input(\"请输入图书单价：\"))\ncount = ______(input(\"请输入购买数量：\"))\ntotal = price * count\nprint(f\"总价：{total:.2f}元\")",
    blanks: [
      { label: "第 1 空", answers: ["float"] },
      { label: "第 2 空", answers: ["int"] }
    ],
    explanation: "价格用 float，数量用 int。input 返回字符串，计算前必须转换类型。"
  },
  {
    id: "f-sample-counter-output",
    type: "fill",
    topic: "collections",
    source: "样卷",
    prompt: "阅读程序，写出两行运行结果。",
    code: "items = [\"茶\", \"咖啡\", \"茶\", \"牛奶\", \"茶\"]\ncounter = {}\nfor item in items:\n    counter[item] = counter.get(item, 0) + 1\nprint(counter[\"茶\"])\nprint(len(counter))",
    blanks: [
      { label: "第 1 行输出", answers: ["3"] },
      { label: "第 2 行输出", answers: ["3"] }
    ],
    explanation: "茶出现 3 次；不同键有 茶、咖啡、牛奶，共 3 个。"
  },
  {
    id: "c-if-order-discount",
    type: "choice",
    topic: "basics",
    source: "实验4 程序结构",
    prompt: "超市折扣规则为 500 元以上 95 折，1000 元以上 9 折，1500 元以上 85 折，2000 元以上 8 折。下面代码对 2500 元商品会输出什么折扣？",
    code: "yuanjia = 2500\nif yuanjia >= 500:\n    print(yuanjia * 0.95)\nelif yuanjia >= 1000:\n    print(yuanjia * 0.9)\nelif yuanjia >= 1500:\n    print(yuanjia * 0.85)\nelif yuanjia >= 2000:\n    print(yuanjia * 0.8)",
    options: [
      { id: "A", text: "2000.0" },
      { id: "B", text: "2125.0" },
      { id: "C", text: "2250.0" },
      { id: "D", text: "2375.0" }
    ],
    answer: "D",
    explanation: "if/elif 从上到下只执行第一个满足条件的分支，2500 先满足 >=500，所以按 95 折。正确写法应从高门槛往低门槛判断。"
  },
  {
    id: "c-split-sum",
    type: "choice",
    topic: "basics",
    source: "作业 lab_3",
    prompt: "阅读代码，输入 3,5,7 后输出结果是？",
    code: "user_input = input(\"请输入几个数字：\")\nnumbers = user_input.split(\",\")\ntotal = 0\nfor i in numbers:\n    total = total + int(i)\nprint(total)",
    options: [
      { id: "A", text: "357" },
      { id: "B", text: "15" },
      { id: "C", text: "3,5,7" },
      { id: "D", text: "程序报错" }
    ],
    answer: "B",
    explanation: "split(',') 得到字符串列表，再逐个 int 转换后求和。"
  },
  {
    id: "f-password-methods",
    type: "fill",
    topic: "basics",
    source: "作业 lab_3",
    prompt: "密码强度检查中，分别补全判断小写字母、大写字母、数字的方法名。",
    code: "for ch in password:\n    if ch.______():\n        has_lower = True\n    if ch.______():\n        has_upper = True\n    if ch.______():\n        has_digit = True",
    blanks: [
      { label: "小写判断", answers: ["islower"] },
      { label: "大写判断", answers: ["isupper"] },
      { label: "数字判断", answers: ["isdigit"] }
    ],
    explanation: "字符串常用判断方法包括 islower、isupper、isdigit、isalpha 等。"
  },
  {
    id: "c-set-vote",
    type: "choice",
    topic: "collections",
    source: "实验5 复合数据类型",
    prompt: "歌手编号集合 geshou1={1,2,3,4,5}，投票列表中出现过的编号集合为 all_toupiao_set。要得到第一组获得选票的歌手编号，应使用？",
    options: [
      { id: "A", text: "all_toupiao_set | geshou1" },
      { id: "B", text: "all_toupiao_set & geshou1" },
      { id: "C", text: "all_toupiao_set - geshou1" },
      { id: "D", text: "all_toupiao_set == geshou1" }
    ],
    answer: "B",
    explanation: "交集 & 表示两个集合共有的元素，即第一组中实际获得选票的编号。"
  },
  {
    id: "f-dict-merge-get",
    type: "fill",
    topic: "collections",
    source: "实践3 公司合并",
    prompt: "补全公司部门人数合并代码。",
    code: "all_depts = set(a.keys()) | set(b.keys())\nc = {}\nfor dept in all_depts:\n    c[dept] = a.______(dept, 0) + b.______(dept, 0)",
    blanks: [
      { label: "第 1 空", answers: ["get"] },
      { label: "第 2 空", answers: ["get"] }
    ],
    explanation: "公司没有某个部门时，用 get(dept, 0) 避免 KeyError。"
  },
  {
    id: "c-dict-items-sort",
    type: "choice",
    topic: "collections",
    source: "作业 lab_5",
    prompt: "单词频率字典 counts={'hello':2,'world':1}，要得到可排序的键值对列表，应使用？",
    options: [
      { id: "A", text: "list(counts.items())" },
      { id: "B", text: "counts.keys()[0]" },
      { id: "C", text: "counts.append('hello')" },
      { id: "D", text: "dict(counts.values())" }
    ],
    answer: "A",
    explanation: "items() 返回 (key, value) 形式的键值对视图，list(...) 可转为列表。"
  },
  {
    id: "f-sort-key-lambda",
    type: "fill",
    topic: "collections",
    source: "实践3 字符统计",
    prompt: "补全按出现次数降序排序的 key 函数。",
    code: "items = list(count.items())\nitems.sort(key=lambda x: x[____], reverse=True)",
    blanks: [
      { label: "索引", answers: ["1"] }
    ],
    explanation: "count.items() 中每个元素形如 (字符, 次数)，次数在索引 1。"
  },
  {
    id: "c-list-count",
    type: "choice",
    topic: "collections",
    source: "实践3 随机数统计",
    prompt: "随机数统计中，ls1 是原始成绩列表，num 是某个分数。统计 num 出现次数应写为？",
    options: [
      { id: "A", text: "ls1.count(num)" },
      { id: "B", text: "num.count(ls1)" },
      { id: "C", text: "ls1.index(num)" },
      { id: "D", text: "len(num)" }
    ],
    answer: "A",
    explanation: "列表 count(value) 返回 value 在列表中出现的次数。"
  },
  {
    id: "f-function-syntax",
    type: "fill",
    topic: "functions",
    source: "教材第7章",
    prompt: "补全函数定义和返回值语句。",
    code: "______ add(a, b):\n    total = a + b\n    ______ total",
    blanks: [
      { label: "函数关键字", answers: ["def"] },
      { label: "返回关键字", answers: ["return"] }
    ],
    explanation: "函数用 def 定义，用 return 返回结果。"
  },
  {
    id: "c-gcd-loop",
    type: "choice",
    topic: "functions",
    source: "实验6 函数",
    prompt: "欧几里得算法求 GCD 时，循环条件通常是？",
    code: "def GCD(a, b):\n    while ______:\n        r = a % b\n        a = b\n        b = r\n    return a",
    options: [
      { id: "A", text: "a == 0" },
      { id: "B", text: "b != 0" },
      { id: "C", text: "a < b" },
      { id: "D", text: "r == 0" }
    ],
    answer: "B",
    explanation: "辗转相除法不断用余数替换，直到 b 为 0，此时 a 是最大公约数。"
  },
  {
    id: "f-lcm-call-gcd",
    type: "fill",
    topic: "functions",
    source: "实验6 函数",
    prompt: "补全最小公倍数函数。",
    code: "def LCM(a, b):\n    gcd = ______(a, b)\n    return (a * b) // gcd",
    blanks: [
      { label: "函数名", answers: ["GCD", "gcd"] }
    ],
    explanation: "最小公倍数 = 两数乘积 // 最大公约数。"
  },
  {
    id: "c-recursion-monkey",
    type: "choice",
    topic: "functions",
    source: "实验6 函数",
    prompt: "猴子吃桃递归中，第 10 天吃之前桃子数量为 1。递归终止条件应写为？",
    options: [
      { id: "A", text: "if n == 1: return 10" },
      { id: "B", text: "if n == 10: return 1" },
      { id: "C", text: "if n > 10: return 0" },
      { id: "D", text: "if n == 0: return 1" }
    ],
    answer: "B",
    explanation: "递归需要明确终止条件；题目给出第 10 天吃之前为 1。"
  },
  {
    id: "f-varargs",
    type: "fill",
    topic: "functions",
    source: "实验6 函数",
    prompt: "补全可变参数函数定义。",
    code: "def min_n(a, b, ______):\n    current_min = a\n    for num in c:\n        if num < current_min:\n            current_min = num\n    return current_min",
    blanks: [
      { label: "可变参数", answers: ["*c"] }
    ],
    explanation: "*c 可以接收第 3 个及以后的任意多个实参，函数内部以元组形式使用。"
  },
  {
    id: "f-main-guard",
    type: "fill",
    topic: "functions",
    source: "实践4 自幂数",
    prompt: "补全模块主程序判断语句。",
    code: "if ______ == \"______\":\n    for i in range(1, 1000):\n        if narcissistic_number(i):\n            print(i)",
    blanks: [
      { label: "第 1 空", answers: ["__name__"] },
      { label: "第 2 空", answers: ["__main__"] }
    ],
    explanation: "if __name__ == '__main__' 用来判断当前文件是否作为主程序运行。"
  },
  {
    id: "c-tuple-return",
    type: "choice",
    topic: "functions",
    source: "实践4 序列数值处理",
    prompt: "函数 get_max_min_num(s) 返回最大值、最小值、元素个数，最合适的 return 写法是？",
    options: [
      { id: "A", text: "return max(s), min(s), len(s)" },
      { id: "B", text: "return max, min, len" },
      { id: "C", text: "print(max(s), min(s), len(s))" },
      { id: "D", text: "return s.max(), s.min(), s.len()" }
    ],
    answer: "A",
    explanation: "逗号分隔多个返回值时，Python 实际返回一个元组。"
  },
  {
    id: "c-init-self",
    type: "choice",
    topic: "oop",
    source: "教材第8章",
    prompt: "关于 __init__ 和 self，下列说法正确的是？",
    options: [
      { id: "A", text: "__init__ 需要手动调用，self 表示父类" },
      { id: "B", text: "__init__ 创建对象时自动调用，self 表示当前对象" },
      { id: "C", text: "self 只能写成 this" },
      { id: "D", text: "类中不能定义函数" }
    ],
    answer: "B",
    explanation: "__init__ 是初始化方法；实例方法第一个参数 self 表示当前对象。"
  },
  {
    id: "f-student-attrs",
    type: "fill",
    topic: "oop",
    source: "实验7 面向对象",
    prompt: "补全 Student 类的属性初始化。",
    code: "class Student:\n    def __init__(self, student_id, name, birthday):\n        self.______ = student_id\n        self.______ = name\n        self.______ = birthday",
    blanks: [
      { label: "学号属性", answers: ["student_id"] },
      { label: "姓名属性", answers: ["name"] },
      { label: "生日属性", answers: ["birthday"] }
    ],
    explanation: "实例属性通常写成 self.属性名 = 参数值。"
  },
  {
    id: "c-age-birthday",
    type: "choice",
    topic: "oop",
    source: "作业 lab_7",
    prompt: "计算年龄时，如果今年生日还没到，应该如何处理？",
    options: [
      { id: "A", text: "年龄加 1" },
      { id: "B", text: "年龄减 1" },
      { id: "C", text: "年龄乘 12" },
      { id: "D", text: "直接返回出生年份" }
    ],
    answer: "B",
    explanation: "当前年份减出生年份只是初值；今年生日未到时需要减 1。"
  },
  {
    id: "f-temp-method",
    type: "fill",
    topic: "oop",
    source: "实验7 Temperature",
    prompt: "补全摄氏转华氏方法。",
    code: "class Temperature:\n    def __init__(self, degree):\n        self.degree = degree\n\n    def ToFahrenheit(self):\n        return self.degree * ______ + ______",
    blanks: [
      { label: "乘数", answers: ["1.8", "9/5", "9 / 5"] },
      { label: "加数", answers: ["32"] }
    ],
    explanation: "华氏温度 = 摄氏温度 * 1.8 + 32。"
  },
  {
    id: "c-super-inherit",
    type: "choice",
    topic: "oop",
    source: "实践5 继承",
    prompt: "Student 继承 Person，在 Student.__init__ 中初始化姓名和年龄，推荐写法是？",
    options: [
      { id: "A", text: "super().__init__(name, age)" },
      { id: "B", text: "Person.introduce(name, age)" },
      { id: "C", text: "self.super(name, age)" },
      { id: "D", text: "return Person" }
    ],
    answer: "A",
    explanation: "super().__init__(...) 调用父类构造方法，复用公共属性初始化逻辑。"
  },
  {
    id: "f-shopping-item-total",
    type: "fill",
    topic: "oop",
    source: "实验7 购物车",
    prompt: "补全购物车中单件商品小计计算。",
    code: "for item in self.items:\n    item_total = item[\"______\"] * item[\"______\"]\n    total = total + item_total",
    blanks: [
      { label: "价格键", answers: ["price"] },
      { label: "数量键", answers: ["quantity"] }
    ],
    explanation: "每个商品用字典保存 name、price、quantity，小计 = price * quantity。"
  },
  {
    id: "c-str-method",
    type: "choice",
    topic: "oop",
    source: "实验7 购物车",
    prompt: "print(cart) 时，如果希望自动输出购物车内容，应在类中定义哪个方法？",
    options: [
      { id: "A", text: "__init__" },
      { id: "B", text: "__str__" },
      { id: "C", text: "__list__" },
      { id: "D", text: "add_item" }
    ],
    answer: "B",
    explanation: "print(对象) 会调用对象的 __str__ 方法得到字符串表示。"
  },
  {
    id: "f-file-open-read",
    type: "fill",
    topic: "files",
    source: "实验8 文件处理",
    prompt: "补全读取 UTF-8 文本文件的代码。",
    code: "f = open(input_path, \"______\", encoding=\"______\")\nlines = f.readlines()\nf.close()",
    blanks: [
      { label: "打开模式", answers: ["r"] },
      { label: "编码", answers: ["utf-8", "UTF-8"] }
    ],
    explanation: "读取文本文件用 'r'，中文或课程数据常显式指定 encoding='utf-8'。"
  },
  {
    id: "c-strip-empty",
    type: "choice",
    topic: "files",
    source: "实验8 文件处理",
    prompt: "处理文件每一行时，line = line.strip() 的主要作用是？",
    options: [
      { id: "A", text: "删除文件" },
      { id: "B", text: "去掉行首行尾空白和换行符" },
      { id: "C", text: "把字符串转成整数" },
      { id: "D", text: "把文件关闭" }
    ],
    answer: "B",
    explanation: "strip() 常用于清理每行两端的空格、制表符和换行符。"
  },
  {
    id: "f-score-weight",
    type: "fill",
    topic: "files",
    source: "实验8 成绩文件",
    prompt: "补全总评成绩公式：平时 10%，期中 30%，期末 60%。",
    code: "zongping = pingshi * ______ + qizhong * ______ + qimo * ______",
    blanks: [
      { label: "平时权重", answers: ["0.1", ".1"] },
      { label: "期中权重", answers: ["0.3", ".3"] },
      { label: "期末权重", answers: ["0.6", ".6"] }
    ],
    explanation: "总评 = 平时 * 0.1 + 期中 * 0.3 + 期末 * 0.6。"
  },
  {
    id: "c-vote-dict-count",
    type: "choice",
    topic: "files",
    source: "实验8 村长选举",
    prompt: "统计候选人票数时，最简洁的更新语句是？",
    options: [
      { id: "A", text: "votes[name] = votes.get(name, 0) + 1" },
      { id: "B", text: "votes.get(name) = votes + 1" },
      { id: "C", text: "name[votes] += 1" },
      { id: "D", text: "votes.append(name, 1)" }
    ],
    answer: "A",
    explanation: "用字典保存姓名到票数的映射，get 可处理首次出现。"
  },
  {
    id: "f-file-write",
    type: "fill",
    topic: "files",
    source: "实验8 文件处理",
    prompt: "补全写入结果文件的代码。",
    code: "out = open(output_path, \"w\", encoding=\"utf-8\")\nout.______(result + \"\\n\")\nout.______()",
    blanks: [
      { label: "写入方法", answers: ["write"] },
      { label: "关闭方法", answers: ["close"] }
    ],
    explanation: "文件对象用 write 写入字符串，用 close 关闭文件。"
  },
  {
    id: "c-with-open",
    type: "choice",
    topic: "files",
    source: "文件处理拓展",
    prompt: "下面哪种写法能在代码块结束后自动关闭文件？",
    options: [
      { id: "A", text: "with open(path, 'r', encoding='utf-8') as f:" },
      { id: "B", text: "auto open(path)" },
      { id: "C", text: "open.close(path)" },
      { id: "D", text: "while open(path)" }
    ],
    answer: "A",
    explanation: "with open(...) as f 是上下文管理器写法，能自动关闭文件。"
  },
  {
    id: "f-jieba-lcut",
    type: "fill",
    topic: "wordcloud",
    source: "实践6 分词",
    prompt: "补全 jieba 分词代码。",
    code: "import jieba\ntext = \"工业互联网是智改数转新趋势下实现智能制造的关键\"\nresult = jieba.______(text)",
    blanks: [
      { label: "分词函数", answers: ["lcut"] }
    ],
    explanation: "jieba.lcut(text) 直接返回分词后的列表。"
  },
  {
    id: "c-userdict",
    type: "choice",
    topic: "wordcloud",
    source: "实践6 词典维护",
    prompt: "要加载自定义词典 userdict.txt，应使用？",
    options: [
      { id: "A", text: "jieba.load_userdict('userdict.txt')" },
      { id: "B", text: "jieba.open('userdict.txt')" },
      { id: "C", text: "WordCloud.load_userdict('userdict.txt')" },
      { id: "D", text: "re.load('userdict.txt')" }
    ],
    answer: "A",
    explanation: "jieba.load_userdict 可以把课程词语如 工业互联网、智改数转 加入分词词典。"
  },
  {
    id: "f-regex-punc",
    type: "fill",
    topic: "wordcloud",
    source: "实践6 中文词云",
    prompt: "补全去除中文标点的正则替换。",
    code: "import re\nst1 = re.______(r'[，。、“”‘’！？]', '', str(text1))",
    blanks: [
      { label: "函数名", answers: ["sub"] }
    ],
    explanation: "re.sub(pattern, repl, text) 用替换方式清洗文本。"
  },
  {
    id: "c-word-join",
    type: "choice",
    topic: "wordcloud",
    source: "实践6 中文词云",
    prompt: "WordCloud.generate 需要用空格分隔的词串。jieba 分词后应如何拼接？",
    options: [
      { id: "A", text: "\" \".join(cut_words)" },
      { id: "B", text: "cut_words.split(' ')" },
      { id: "C", text: "cut_words + 1" },
      { id: "D", text: "dict(cut_words)" }
    ],
    answer: "A",
    explanation: "中文分词列表需要用空格连接成字符串，词云库才能按词识别。"
  },
  {
    id: "f-wordcloud-font",
    type: "fill",
    topic: "wordcloud",
    source: "实践6 中文词云",
    prompt: "补全中文词云对象中最关键的中文字体参数。",
    code: "wc = WordCloud(\n    ______=\"simhei.ttf\",\n    max_words=100,\n    background_color=\"white\"\n)",
    blanks: [
      { label: "参数名", answers: ["font_path"] }
    ],
    explanation: "中文词云必须指定支持中文的字体文件，否则可能显示方框。"
  },
  {
    id: "c-mask-array",
    type: "choice",
    topic: "wordcloud",
    source: "实践6 词云图",
    prompt: "使用图片作为词云形状时，PIL 打开图片后通常还需要？",
    options: [
      { id: "A", text: "np.array(mask_img)" },
      { id: "B", text: "int(mask_img)" },
      { id: "C", text: "jieba.lcut(mask_img)" },
      { id: "D", text: "mask_img.write()" }
    ],
    answer: "A",
    explanation: "WordCloud 的 mask 参数需要数组形式，常用 np.array(Image.open(...))。"
  },
  {
    id: "f-tfidf",
    type: "fill",
    topic: "wordcloud",
    source: "实践6 TF-IDF",
    prompt: "补全 TF-IDF 关键词提取代码，要求返回权重。",
    code: "import jieba.analyse as analyse\nkeywords = analyse.______(text, topK=20, ______=True)",
    blanks: [
      { label: "函数名", answers: ["extract_tags"] },
      { label: "权重参数", answers: ["withWeight"] }
    ],
    explanation: "analyse.extract_tags 是 jieba 的 TF-IDF 关键词提取函数，withWeight=True 返回 (词, 权重)。"
  },
  {
    id: "c-frequencies",
    type: "choice",
    topic: "wordcloud",
    source: "实践6 关键词词云",
    prompt: "已经得到 key_dict={'教育':0.8,'学生':0.6}，要按权重生成词云，应使用？",
    options: [
      { id: "A", text: "wc.generate_from_frequencies(key_dict)" },
      { id: "B", text: "wc.generate(key_dict)" },
      { id: "C", text: "jieba.lcut(key_dict)" },
      { id: "D", text: "plt.show(key_dict)" }
    ],
    answer: "A",
    explanation: "generate_from_frequencies 接收 {词: 权重或次数} 形式的字典。"
  },
  {
    id: "f-tk-import-root",
    type: "fill",
    topic: "tkinter",
    source: "教材第11章",
    prompt: "补全 Tkinter 窗口创建代码。",
    code: "import tkinter as tk\nroot = tk.______()\nroot.title(\"练习程序\")\nroot.______()",
    blanks: [
      { label: "窗口类", answers: ["Tk"] },
      { label: "事件循环", answers: ["mainloop"] }
    ],
    explanation: "tk.Tk() 创建主窗口，root.mainloop() 启动事件循环。"
  },
  {
    id: "c-layout-manager",
    type: "choice",
    topic: "tkinter",
    source: "教材第11章",
    prompt: "Tkinter 中以行和列网格形式排列控件的布局管理器是？",
    options: [
      { id: "A", text: "pack()" },
      { id: "B", text: "grid()" },
      { id: "C", text: "place()" },
      { id: "D", text: "mainloop()" }
    ],
    answer: "B",
    explanation: "grid() 以 row、column 的网格方式布局控件。"
  },
  {
    id: "c-command-bind",
    type: "choice",
    topic: "tkinter",
    source: "教材第11章",
    prompt: "按钮点击后调用 check_answer 函数，创建按钮时最常见的绑定方式是？",
    options: [
      { id: "A", text: "tk.Button(root, text='提交', command=check_answer)" },
      { id: "B", text: "tk.Button(root, text='提交', event=check_answer)" },
      { id: "C", text: "tk.Button(root, text='提交').mainloop(check_answer)" },
      { id: "D", text: "tk.Button(root, check_answer)" }
    ],
    answer: "A",
    explanation: "Button、Radiobutton、Checkbutton 等控件可用 command=函数 绑定命令。"
  },
  {
    id: "f-bind-event",
    type: "fill",
    topic: "tkinter",
    source: "综合项目实践",
    prompt: "补全回车键绑定代码。",
    code: "answer_entry.bind(\"<______>\", lambda event: check_answer())",
    blanks: [
      { label: "事件描述符", answers: ["Return"] }
    ],
    explanation: "Entry 绑定回车键常用 '<Return>'；bind 回调会收到 event 参数。"
  },
  {
    id: "c-entry-get",
    type: "choice",
    topic: "tkinter",
    source: "综合项目实践",
    prompt: "获取 Entry 输入框内容并去掉首尾空格，正确写法是？",
    options: [
      { id: "A", text: "answer_entry.get().strip()" },
      { id: "B", text: "answer_entry.text.strip()" },
      { id: "C", text: "answer_entry.input()" },
      { id: "D", text: "tk.get(answer_entry)" }
    ],
    answer: "A",
    explanation: "Entry 控件使用 get() 读取文本，字符串再用 strip() 清理空格。"
  },
  {
    id: "f-config-label",
    type: "fill",
    topic: "tkinter",
    source: "综合项目实践",
    prompt: "补全根据答案结果更新提示标签的代码。",
    code: "if user_answer == current_answer:\n    result_label.______(text=\"回答正确！\", fg=\"green\")\nelse:\n    result_label.______(text=\"回答错误\", fg=\"red\")",
    blanks: [
      { label: "第 1 空", answers: ["config", "configure"] },
      { label: "第 2 空", answers: ["config", "configure"] }
    ],
    explanation: "Label 的显示文本、颜色等属性可用 config 或 configure 更新。"
  },
  {
    id: "c-global-callback",
    type: "choice",
    topic: "tkinter",
    source: "综合项目实践",
    prompt: "在 Tkinter 回调函数中修改 total_count、right_count 这类全局统计变量，函数内部通常需要？",
    options: [
      { id: "A", text: "global total_count, right_count" },
      { id: "B", text: "return global" },
      { id: "C", text: "import total_count" },
      { id: "D", text: "self.global()" }
    ],
    answer: "A",
    explanation: "函数内给全局变量重新赋值时，需要用 global 声明。"
  },
  {
    id: "code-print-fee",
    type: "code",
    topic: "integrated",
    source: "样卷编程题",
    prompt: "编程题：根据输入页数计算校园打印费用。pages<=0 输出“页数输入错误”；1-20 页每页 0.30；21-100 页前 20 页 0.30、超出部分 0.25；100 页以上再按 0.20 计算。合法时输出“应付金额：xx.x元”。",
    criteria: [
      { label: "读取并转换页数为整数", points: 15, all: ["int\\s*\\(\\s*input\\s*\\("] },
      { label: "先判断 pages <= 0", points: 20, all: ["pages\\s*<=\\s*0", "页数输入错误"] },
      { label: "正确处理 20 页以内", points: 15, all: ["pages\\s*<=\\s*20", "0\\.30|\\.30|0\\.3|\\.3"] },
      { label: "正确处理 21-100 页", points: 20, all: ["pages\\s*<=\\s*100", "20\\s*\\*\\s*0\\.3|20\\s*\\*\\s*0\\.30", "0\\.25|\\.25"] },
      { label: "正确处理 100 页以上", points: 20, all: ["100", "0\\.20|\\.20|0\\.2|\\.2"] },
      { label: "使用 f-string 或格式化保留 1 位小数", points: 10, any: [":\\.1f", "round\\s*\\("] }
    ],
    sampleAnswer: "pages = int(input(\"请输入打印页数：\"))\nif pages <= 0:\n    print(\"页数输入错误\")\nelif pages <= 20:\n    money = pages * 0.30\n    print(f\"应付金额：{money:.1f}元\")\nelif pages <= 100:\n    money = 20 * 0.30 + (pages - 20) * 0.25\n    print(f\"应付金额：{money:.1f}元\")\nelse:\n    money = 20 * 0.30 + 80 * 0.25 + (pages - 100) * 0.20\n    print(f\"应付金额：{money:.1f}元\")",
    explanation: "这类分段计费题最容易错在判断顺序和边界：先处理非法，再按页数从小到大分段。"
  },
  {
    id: "code-task-record",
    type: "code",
    topic: "oop",
    source: "样卷编程题",
    prompt: "编程题：定义 TaskRecord 类，__init__(self, name, finished) 初始化姓名和完成任务数；add_task(self, count) 当 count>0 时增加 finished 并返回 True，否则返回 False；show(self) 按 finished 判断等级并输出。",
    criteria: [
      { label: "定义 TaskRecord 类", points: 15, all: ["class\\s+TaskRecord\\s*:"] },
      { label: "构造方法包含 name、finished 并保存到 self", points: 20, all: ["def\\s+__init__\\s*\\(\\s*self\\s*,\\s*name\\s*,\\s*finished\\s*\\)", "self\\.name", "self\\.finished"] },
      { label: "add_task 方法判断 count > 0", points: 20, all: ["def\\s+add_task\\s*\\(\\s*self\\s*,\\s*count\\s*\\)", "count\\s*>\\s*0"] },
      { label: "合法时累加 finished 并返回 True", points: 15, all: ["self\\.finished\\s*(\\+=|=\\s*self\\.finished\\s*\\+)", "return\\s+True"] },
      { label: "非法时返回 False", points: 10, all: ["return\\s+False"] },
      { label: "show 方法按 8、5 分级并输出格式", points: 20, all: ["def\\s+show\\s*\\(\\s*self\\s*\\)", "优秀", "合格", "不合格", "学生", "完成任务"] }
    ],
    sampleAnswer: "class TaskRecord:\n    def __init__(self, name, finished):\n        self.name = name\n        self.finished = finished\n\n    def add_task(self, count):\n        if count > 0:\n            self.finished += count\n            return True\n        return False\n\n    def show(self):\n        if self.finished >= 8:\n            level = \"优秀\"\n        elif self.finished >= 5:\n            level = \"合格\"\n        else:\n            level = \"不合格\"\n        print(f\"学生：{self.name}，完成任务：{self.finished}个，等级：{level}\")",
    explanation: "类题核心是属性初始化、带参数方法、返回值、if/elif/else 分级。"
  },
  {
    id: "code-vote-file",
    type: "code",
    topic: "files",
    source: "实验8 村长选举",
    prompt: "编程题：读取 data935.txt，每行一个候选人姓名，统计票数并按票数降序写入 data935_result.txt，格式如“吴娟 得票 59”。",
    criteria: [
      { label: "打开并读取 UTF-8 文件", points: 15, all: ["open\\s*\\(", "encoding\\s*=\\s*[\"']utf-8[\"']", "readlines\\s*\\("] },
      { label: "使用字典统计票数", points: 25, all: ["votes\\s*=\\s*\\{\\}", "votes\\[", "\\.get\\s*\\(|if\\s+name\\s+in\\s+votes"] },
      { label: "处理空行或 strip", points: 15, all: ["strip\\s*\\(", "continue|if\\s+name\\s*==\\s*[\"']"] },
      { label: "转换为列表并按票数降序", points: 20, any: ["sorted\\s*\\(.+reverse\\s*=\\s*True", "sort\\s*\\(.+reverse\\s*=\\s*True", "for\\s+i\\s+in\\s+range\\s*\\("] },
      { label: "写入结果文件", points: 15, all: ["open\\s*\\(.+[\"']w[\"']", "write\\s*\\("] },
      { label: "输出格式包含“得票”", points: 10, all: ["得票"] }
    ],
    sampleAnswer: "votes = {}\nwith open(\"data935.txt\", \"r\", encoding=\"utf-8\") as f:\n    for line in f.readlines():\n        name = line.strip()\n        if name == \"\":\n            continue\n        votes[name] = votes.get(name, 0) + 1\n\nvotes_list = sorted(votes.items(), key=lambda x: x[1], reverse=True)\nwith open(\"data935_result.txt\", \"w\", encoding=\"utf-8\") as f:\n    for name, count in votes_list:\n        result = f\"{name} 得票 {count}\"\n        print(result)\n        f.write(result + \"\\n\")",
    explanation: "文件处理题常考：读文件、strip 清洗、字典统计、排序、写文件。"
  },
  {
    id: "code-factorial-combination",
    type: "code",
    topic: "functions",
    source: "实践4 组合数",
    prompt: "编程题：定义 factorial(n) 函数计算 n!，输入 n、m，三次调用 factorial 计算组合数 C(n,m)=n!/(m!(n-m)!) 并输出。",
    criteria: [
      { label: "定义 factorial 函数", points: 20, all: ["def\\s+factorial\\s*\\(\\s*n\\s*\\)"] },
      { label: "函数内使用循环累乘", points: 20, all: ["for\\s+.+in\\s+range\\s*\\(", "ret|result", "\\*="] },
      { label: "返回阶乘结果", points: 15, all: ["return\\s+"] },
      { label: "输入 n 和 m", points: 10, any: ["input\\s*\\(", "eval\\s*\\(\\s*input"] },
      { label: "三次调用 factorial", points: 20, all: ["factorial\\s*\\(\\s*n\\s*\\)", "factorial\\s*\\(\\s*m\\s*\\)", "factorial\\s*\\(\\s*n\\s*-\\s*m\\s*\\)"] },
      { label: "使用整除或整数化输出组合数", points: 15, any: ["//", "int\\s*\\("] }
    ],
    sampleAnswer: "def factorial(n):\n    ret = 1\n    for i in range(1, n + 1):\n        ret *= i\n    return ret\n\nn = int(input(\"请输入n：\"))\nm = int(input(\"请输入m：\"))\nresult = factorial(n) // (factorial(m) * factorial(n - m))\nprint(result)",
    explanation: "函数题重点是把重复逻辑封装成函数，并正确使用返回值。"
  },
  {
    id: "code-chinese-wordcloud",
    type: "code",
    topic: "wordcloud",
    source: "实践6 中文词云",
    prompt: "编程题：读取 教育.txt，去除中文标点，使用 jieba 分词，指定 simhei.ttf 字体、bird.png 形状、停用词，生成并保存中文词云图。",
    criteria: [
      { label: "导入 jieba、WordCloud、Image、numpy、re", points: 20, all: ["jieba", "WordCloud", "Image", "np|numpy", "re"] },
      { label: "读取 教育.txt 且指定 UTF-8", points: 15, all: ["open\\s*\\(.+教育\\.txt", "encoding\\s*=\\s*[\"']utf-8[\"']"] },
      { label: "使用 re.sub 去除标点", points: 15, all: ["re\\.sub\\s*\\("] },
      { label: "使用 jieba.lcut 分词并用空格 join", points: 20, all: ["jieba\\.lcut\\s*\\(", "[\"']\\s[\"']\\.join\\s*\\("] },
      { label: "读取 bird.png 并转 np.array", points: 10, all: ["Image\\.open\\s*\\(.+bird\\.png", "np\\.array\\s*\\("] },
      { label: "WordCloud 指定 font_path、stopwords、mask", points: 15, all: ["font_path\\s*=\\s*[\"']simhei\\.ttf[\"']", "stopwords", "mask\\s*="] },
      { label: "生成并保存图片", points: 5, all: ["\\.generate\\s*\\(", "\\.to_file\\s*\\("] }
    ],
    sampleAnswer: "import numpy as np\nfrom PIL import Image\nimport jieba\nfrom wordcloud import WordCloud\nimport re\n\nwith open(\"教育.txt\", \"r\", encoding=\"utf-8\") as f:\n    text1 = f.readlines()\nst1 = re.sub(r'[，。、“”‘’！？]', '', str(text1))\ncut_words = jieba.lcut(st1)\nwords = \" \".join(cut_words)\nmask_array = np.array(Image.open(\"bird.png\"))\nexclude_words = ['我', '了', '在', '的', '我们', '是', '和', '一个', '这', '那么']\nwc = WordCloud(font_path=\"simhei.ttf\", max_words=100, mask=mask_array, width=800, height=600, stopwords=set(exclude_words), background_color=\"white\")\ncloud = wc.generate(words)\ncloud.to_file(\"Chinese_WordCloud.png\")",
    explanation: "中文词云题是文件读取、文本清洗、分词、停用词、字体、mask 和保存图片的组合。"
  },
  {
    id: "code-shopping-cart",
    type: "code",
    topic: "oop",
    source: "实验7 购物车",
    prompt: "编程题：实现 ShoppingCart 类，items 初始为空；add_item(name, price, quantity=1) 添加商品字典；__str__ 返回购物车内容和总价，空购物车返回“购物车是空的”。",
    criteria: [
      { label: "定义 ShoppingCart 类和 __init__", points: 20, all: ["class\\s+ShoppingCart\\s*:", "def\\s+__init__\\s*\\(\\s*self\\s*\\)", "self\\.items\\s*=\\s*\\[\\]"] },
      { label: "add_item 含默认数量参数", points: 15, all: ["def\\s+add_item\\s*\\(\\s*self\\s*,\\s*name\\s*,\\s*price\\s*,\\s*quantity\\s*=\\s*1\\s*\\)"] },
      { label: "商品以字典形式加入列表", points: 20, all: ["\\{", "name", "price", "quantity", "self\\.items\\.append\\s*\\("] },
      { label: "__str__ 处理空购物车", points: 15, all: ["def\\s+__str__\\s*\\(\\s*self\\s*\\)", "if\\s+not\\s+self\\.items", "购物车是空的"] },
      { label: "遍历 items 计算 item_total 和 total", points: 20, all: ["for\\s+item\\s+in\\s+self\\.items", "item_total", "total"] },
      { label: "金额格式保留两位小数", points: 10, all: [":\\.2f"] }
    ],
    sampleAnswer: "class ShoppingCart:\n    def __init__(self):\n        self.items = []\n\n    def add_item(self, name, price, quantity=1):\n        item = {\"name\": name, \"price\": price, \"quantity\": quantity}\n        self.items.append(item)\n\n    def __str__(self):\n        if not self.items:\n            return \"购物车是空的\"\n        result = \"购物车内容:\\n\"\n        total = 0\n        for item in self.items:\n            item_total = item[\"price\"] * item[\"quantity\"]\n            result += f\"- {item['name']} × {item['quantity']}: ￥{item_total:.2f}\\n\"\n            total += item_total\n        result += f\"总计: ￥{total:.2f}\"\n        return result",
    explanation: "购物车题同时检查类、列表、字典、字符串拼接和格式化输出。"
  },
  {
    id: "code-poem-loader",
    type: "code",
    topic: "integrated",
    source: "综合项目实践",
    prompt: "编程题：写 load_poem(poemfiles) 函数。文件每行格式为 title|author|line1,line2,...；跳过空行；把每首诗转成 Poem(title, author, lines) 对象加入列表并返回。",
    criteria: [
      { label: "定义 Poem 类并保存 title、author、lines", points: 20, all: ["class\\s+Poem\\s*:", "self\\.title", "self\\.author", "self\\.lines"] },
      { label: "定义 load_poem 函数", points: 15, all: ["def\\s+load_poem\\s*\\(\\s*poemfiles\\s*\\)"] },
      { label: "打开文件并指定 UTF-8", points: 15, all: ["open\\s*\\(\\s*poemfiles", "encoding\\s*=\\s*[\"']utf-8[\"']"] },
      { label: "逐行 strip 并跳过空行", points: 15, all: ["for\\s+line\\s+in", "line\\.strip\\s*\\(", "continue"] },
      { label: "使用 | 分割标题作者内容", points: 15, all: ["split\\s*\\(\\s*[\"']\\|[\"']\\s*\\)"] },
      { label: "使用逗号分割诗句并创建对象", points: 15, all: ["split\\s*\\(\\s*[\"'],[\"']\\s*\\)", "Poem\\s*\\("] },
      { label: "返回 poems 列表", points: 5, all: ["return\\s+poems"] }
    ],
    sampleAnswer: "class Poem:\n    def __init__(self, title, author, lines):\n        self.title = title\n        self.author = author\n        self.lines = lines\n\ndef load_poem(poemfiles):\n    poems = []\n    with open(poemfiles, \"r\", encoding=\"utf-8\") as file:\n        for line in file:\n            line = line.strip()\n            if line == \"\":\n                continue\n            parts = line.split(\"|\")\n            title = parts[0]\n            author = parts[1]\n            text = parts[2]\n            lines = text.split(\",\")\n            poems.append(Poem(title, author, lines))\n    return poems",
    explanation: "综合项目的数据层重点是文件读取、字符串拆分和对象化存储。"
  },
  {
    id: "code-tkinter-submit",
    type: "code",
    topic: "tkinter",
    source: "综合项目实践",
    prompt: "编程题：写一个 Tkinter 答案检查回调 check_answer。要求读取 Entry 内容并 strip；空答案提示红色；提交后 total_count 加 1；答对 right_count 加 1 并显示绿色；答错显示正确答案。",
    criteria: [
      { label: "定义 check_answer 回调并声明全局统计变量", points: 15, all: ["def\\s+check_answer\\s*\\(", "global\\s+.+total_count"] },
      { label: "从 Entry 获取输入并 strip", points: 15, all: ["\\.get\\s*\\(\\s*\\)", "\\.strip\\s*\\("] },
      { label: "处理空答案并设置红色提示", points: 15, all: ["user_answer\\s*==\\s*[\"']", "请输入", "fg\\s*=\\s*[\"']red[\"']"] },
      { label: "更新总题数", points: 15, all: ["total_count\\s*(\\+=|=\\s*total_count\\s*\\+)"] },
      { label: "比较 current_answer", points: 15, all: ["user_answer\\s*==\\s*current_answer"] },
      { label: "答对更新 right_count 和绿色提示", points: 15, all: ["right_count\\s*(\\+=|=\\s*right_count\\s*\\+)", "fg\\s*=\\s*[\"']green[\"']"] },
      { label: "答错显示正确答案", points: 10, all: ["正确答案|current_answer"] }
    ],
    sampleAnswer: "def check_answer():\n    global total_count, right_count\n    user_answer = answer_entry.get().strip()\n    if user_answer == \"\":\n        result_label.config(text=\"请输入答案后再提交\", fg=\"red\")\n        return\n    total_count += 1\n    if user_answer == current_answer:\n        right_count += 1\n        result_label.config(text=\"回答正确！\", fg=\"green\")\n    else:\n        result_label.config(text=\"回答错误，正确答案是：\" + current_answer, fg=\"red\")",
    explanation: "GUI 题重点是控件取值、事件回调、全局状态和界面刷新。"
  }
];
