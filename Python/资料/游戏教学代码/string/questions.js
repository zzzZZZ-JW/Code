const questions = [
  {
    background: "小明刚学会 print，兴冲冲地写了第一行代码，但运行后报错了……",
    description: "以下哪段代码能正确输出 <code>Hello Python</code>？",
    tissue: {
      label: '纸巾',
      code: 'print("Hello Python")'
    },
    carrot: {
      label: '萝卜',
      code: 'print "Hello Python"'
    },
    answer: "tissue",
    explanation: "print 是一个函数，必须用括号 () 把内容包起来。Python 3 中 <code>print \"...\"</code> 会报语法错误。记住：函数调用 = 函数名 + 小括号！"
  },
  {
    background: "老师要求用 print 在一行内输出三个水果名，用逗号隔开。小红写了两种方案……",
    description: "哪段代码的输出是 <code>apple,banana,cherry</code>（逗号之间没有空格）？",
    tissue: {
      label: '纸巾',
      code: 'print("apple", "banana", "cherry")'
    },
    carrot: {
      label: '萝卜',
      code: 'print("apple", "banana", "cherry", sep=",")'
    },
    answer: "carrot",
    explanation: "print 默认用空格分隔多个参数。要改变分隔符，需要用 <code>sep</code> 参数。<code>sep=\",\"</code> 就是告诉 print：请用逗号来分隔，不要用空格。"
  },
  {
    background: "小李想让两个 print 的内容显示在同一行，他试了两种写法……",
    description: "哪段代码能让 <code>Hello</code> 和 <code>World</code> 显示在同一行？",
    tissue: {
      label: '纸巾',
      code: 'print("Hello", end=" ")\nprint("World")'
    },
    carrot: {
      label: '萝卜',
      code: 'print("Hello")\nprint("World")'
    },
    answer: "tissue",
    explanation: "print 默认在末尾加换行符 <code>\\n</code>。使用 <code>end=\" \"</code> 可以把换行符替换成空格，这样下一个 print 就会接在同一行。"
  },
  {
    background: "小王要创建一个字符串变量保存自己的名字，他写了两种方式……",
    description: "哪种写法能正确创建一个值为 <code>Hello Python</code> 的字符串？",
    tissue: {
      label: '纸巾',
      code: 'a = Hello Python'
    },
    carrot: {
      label: '萝卜',
      code: 'a = "Hello Python"'
    },
    answer: "carrot",
    explanation: "字符串必须用引号包裹（双引号 <code>\"\"</code> 或单引号 <code>''</code>）。不加引号的话，Python 会把它当成变量名去查找，找不到就报 NameError。"
  },
  {
    background: "小张想用一个变量来存字符串，他给变量取名叫 str。代码能正常运行，但后面出了问题……",
    description: "执行 <code>str = \"Hello\"</code> 之后，再执行 <code>str(123)</code> 会怎样？",
    tissue: {
      label: '纸巾',
      code: '# 正常返回字符串 "123"\nstr(123)'
    },
    carrot: {
      label: '萝卜',
      code: '# 报错！str 已经不是函数了\nstr(123)'
    },
    answer: "carrot",
    explanation: "虽然 <code>str = \"Hello\"</code> 不会立刻报错，但它把 Python 内置的 <code>str()</code> 函数覆盖了！之后再调用 <code>str(123)</code> 就会出错。永远不要用 <code>str</code>、<code>list</code>、<code>int</code> 等内置名称作为变量名。"
  },
  {
    background: "小陈想把字符串变成小写，她记得有个 lower 函数……",
    description: "哪种写法能正确地把字符串转为小写？",
    tissue: {
      label: '纸巾',
      code: 'a = "HELLO"\nprint(lower(a))'
    },
    carrot: {
      label: '萝卜',
      code: 'a = "HELLO"\nprint(a.lower())'
    },
    answer: "carrot",
    explanation: "<code>lower()</code> 是字符串对象的方法，不是独立的函数。在面向对象编程中，要用 <code>对象.方法()</code> 的格式调用。所以是 <code>a.lower()</code> 而不是 <code>lower(a)</code>。"
  },
  {
    background: "小周想获取字符串的长度，他不确定该怎么写……",
    description: "哪种写法能正确获取字符串 <code>a</code> 的长度？",
    tissue: {
      label: '纸巾',
      code: 'a = "Python"\nprint(len(a))'
    },
    carrot: {
      label: '萝卜',
      code: 'a = "Python"\nprint(a.len())'
    },
    answer: "tissue",
    explanation: "<code>len()</code> 是 Python 的内置函数，不是字符串的方法。要用 <code>len(a)</code> 而不是 <code>a.len()</code>。注意区分：<code>len()</code>、<code>abs()</code> 是内置函数；<code>.lower()</code>、<code>.upper()</code>、<code>.replace()</code> 是字符串方法。"
  },
  {
    background: "小吴想把名字的首字母大写，她试了两种方式……",
    description: "执行以下代码后，<code>print(a)</code> 的输出是什么？<br><code>a = \"hello\"</code><br><code>a.capitalize()</code><br><code>print(a)</code>",
    tissue: {
      label: '纸巾',
      code: '# 输出 Hello\n# capitalize 会修改原字符串'
    },
    carrot: {
      label: '萝卜',
      code: '# 输出 hello\n# 原字符串没有被修改'
    },
    answer: "carrot",
    explanation: "字符串是不可变的（immutable）！<code>a.capitalize()</code> 会返回一个新字符串，但不会修改原来的 <code>a</code>。必须用 <code>a = a.capitalize()</code> 把结果赋值回去。"
  },
  {
    background: "考试题问：<code>\"hello\"[1]</code> 的结果是什么？小赵和小钱给出了不同答案……",
    description: "<code>\"hello\"[1]</code> 的结果是什么？",
    tissue: {
      label: '纸巾',
      code: '# 结果是 "h"'
    },
    carrot: {
      label: '萝卜',
      code: '# 结果是 "e"'
    },
    answer: "carrot",
    explanation: "Python 的索引从 0 开始！<code>\"hello\"[0]</code> 是 <code>'h'</code>，<code>\"hello\"[1]</code> 是 <code>'e'</code>。这是几乎所有编程语言的通用规则。"
  },
  {
    background: "小孙想用 f-string 来格式化输出，但不确定语法……",
    description: "已知 <code>name = \"小明\"</code>，<code>age = 20</code>，哪种写法能输出 <code>我叫小明，今年20岁</code>？",
    tissue: {
      label: '纸巾',
      code: 'print(f"我叫{name}，今年{age}岁")'
    },
    carrot: {
      label: '萝卜',
      code: 'print("我叫{name}，今年{age}岁")'
    },
    answer: "tissue",
    explanation: "f-string 需要在引号前加 <code>f</code> 前缀！没有 <code>f</code> 的话，花括号 <code>{}</code> 就只是普通字符，不会被替换成变量的值。"
  },
  {
    background: "小刘想把字符串 \"123\" 和数字 456 拼接在一起……",
    description: "哪种写法能正确输出 <code>123456</code>？",
    tissue: {
      label: '纸巾',
      code: 'print("123" + 456)'
    },
    carrot: {
      label: '萝卜',
      code: 'print("123" + str(456))'
    },
    answer: "carrot",
    explanation: "Python 不允许字符串和数字直接用 <code>+</code> 拼接。需要先用 <code>str()</code> 把数字转成字符串，或者用 f-string：<code>f\"123{456}\"</code>。"
  },
  {
    background: "小黄想判断用户输入的字符串是不是纯数字……",
    description: "哪种写法能正确判断字符串 <code>s</code> 是否全是数字？",
    tissue: {
      label: '纸巾',
      code: 's = "12345"\nprint(isdigit(s))'
    },
    carrot: {
      label: '萝卜',
      code: 's = "12345"\nprint(s.isdigit())'
    },
    answer: "carrot",
    explanation: "<code>isdigit()</code> 是字符串的方法，不是内置函数。要用 <code>s.isdigit()</code> 的格式。类似的还有 <code>s.isalpha()</code>（判断是否全是字母）、<code>s.isalnum()</code>（判断是否全是字母或数字）。"
  }
];
