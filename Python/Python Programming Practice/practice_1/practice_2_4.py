user_onput = int(input("请输入1个人出生后的天数："))
year = user_onput // 360
month = (user_onput % 360) // 30
print("这个人出生了%d年%d月" % (year, month,))