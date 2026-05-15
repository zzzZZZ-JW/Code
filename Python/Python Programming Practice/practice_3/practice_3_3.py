yue_tian = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

user_input_nian = int(input("请输入年份："))
user_input_yue = int(input("请输入月份："))

days = yue_tian[user_input_yue]

if user_input_yue == 2:
    if (user_input_nian % 4 == 0 and user_input_nian % 100 != 0) or (user_input_nian % 400 == 0):
        days = days + 1

print(f"{user_input_nian}年{user_input_yue}月有{days}天")