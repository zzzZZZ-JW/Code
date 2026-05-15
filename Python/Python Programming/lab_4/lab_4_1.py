yuanjia = int(input("请输入商品价格："))

if yuanjia >= 500:
    print("优惠价为：", yuanjia * 0.95)
elif yuanjia >= 1000:
    print("优惠价为：", yuanjia * 0.9)
elif yuanjia >= 1500:
    print("优惠价为：", yuanjia * 0.85)
elif yuanjia >= 2000:
    print("优惠价为：", yuanjia * 0.8)