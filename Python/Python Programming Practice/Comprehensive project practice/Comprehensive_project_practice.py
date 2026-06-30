import random
import tkinter as tk

class Poem:
    def __init__(self, title, author, lines):
        self.title = title
        self.author = author
        self.lines = lines
    
def load_poem(poemfiles):
    poems = []

    file = open(poemfiles, 'r', encoding='utf-8')

    for line in file:
        line = line.strip()

        if line == "":
            continue
        
        parts = line.split('|')

        title = parts[0]
        author = parts[1]
        text = parts[2]

        lines = text.split(',')

        poem = Poem(title, author, lines)

        poems.append(poem)
    
    file.close()
    return poems

def make_question(poems):
    poem = random.choice(poems)
    answer_index = random.randint(0, len(poem.lines) - 1)
    answer = poem.lines[answer_index]
    show_lines = []
    for i in range(len(poem.lines)):
        if i == answer_index:

            show_lines.append("__________")
        else:

            show_lines.append(poem.lines[i])
    return poem, show_lines, answer

poems = load_poem("poemfiles.txt")

current_poem = None
current_show_lines = []
current_answer = ""
total_count = 0
right_count = 0
is_answered = False

def start_practice():
    global current_poem
    global current_show_lines
    global current_answer
    global is_answered

    title_label.pack_forget()
    start_button.pack_forget()

    current_poem, current_show_lines, current_answer = make_question(poems)
    is_answered = False

    poem_title_label.config(text=current_poem.title + "  " + current_poem.author)

    show_text = ""

    for line in current_show_lines:
        show_text = show_text + line + "\n"

    poem_content_label.config(text=show_text)

    answer_entry.delete(0, tk.END)

    poem_title_label.pack(pady=20)
    poem_content_label.pack(pady=20)
    answer_entry.pack(pady=10)
    submit_button.pack(pady=10)
    next_button.pack(pady=5)
    end_button.pack(pady=5)
    result_label.pack(pady=10)
    result_label.config(text="")

def check_answer():
    global total_count
    global right_count
    global is_answered

    if is_answered == True:
        result_label.config(text="本题已经提交过，请点击下一题", fg="red")
        return

    user_answer = answer_entry.get()
    user_answer = user_answer.strip()

    if user_answer == "":
        result_label.config(text="请输入答案后再提交", fg="red")
        return

    total_count = total_count + 1
    is_answered = True

    if user_answer == current_answer:
        right_count = right_count + 1
        result_label.config(text="回答正确！", fg="green")
    else:
        result_label.config(text="回答错误，正确答案是：" + current_answer, fg="red")

def end_practice():
    if total_count == 0:
        result_label.config(text="你还没有提交任何题目", fg="red")
        return

    rate = right_count / total_count * 100

    poem_title_label.config(text="练习结束")
    poem_content_label.config(
        text="本次练习总题数：" + str(total_count) + "\n"
             + "答对题数：" + str(right_count) + "\n"
             + "正确率：" + str(round(rate, 2)) + "%"
    )

    answer_entry.pack_forget()
    submit_button.pack_forget()
    next_button.pack_forget()
    end_button.pack_forget()

    result_label.config(text="感谢使用古诗词练习程序！", fg="blue")

root = tk.Tk()

root.title("古诗词练习程序")
root.geometry("500x520")
root.resizable(False, False)

title_label = tk.Label(root, text="欢迎使用古诗词练习程序", font=("宋体", 20))
title_label.pack(pady=60)

start_button = tk.Button(root, text="开始答题", font=("宋体", 16), command=start_practice)
start_button.pack()

poem_title_label = tk.Label(root, text="", font=("宋体", 16))
poem_content_label = tk.Label(root, text="", font=("宋体", 18), justify="center")

answer_entry = tk.Entry(root, font=("宋体", 16))
answer_entry.bind("<Return>", lambda event: check_answer())

submit_button = tk.Button(root, text="提交答案", font=("宋体", 14), command=check_answer)
next_button = tk.Button(root, text="下一题", font=("宋体", 14), command=start_practice)
end_button = tk.Button(root, text="结束答题", font=("宋体", 14), command=end_practice)
result_label = tk.Label(root, text="", font=("宋体", 14))

root.mainloop()




