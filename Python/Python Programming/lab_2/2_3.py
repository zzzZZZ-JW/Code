name1 = input("请输入第1个商品名称：")
price1 = float(input("请输入单价："))
num1 = int(input("请输入数量："))

name2 = input("请输入第2个商品名称：")
price2 = float(input("请输入单价："))
num2 = int(input("请输入数量："))

name3 = input("请输入第3个商品名称：")
price3 = float(input("请输入单价："))
num3 = int(input("请输入数量："))

totle1 = price1 * num1
totle2 = price2 * num2
totle3 = price3 * num3
totle = totle1 + totle2 + totle3

print("==========购物清单==========")
print("商品名称    单价    数量    小计")
print(name1, "    ", price1, "    ", num1, "    ", totle1)
print(name2, "    ", price2, "    ", num2, "    ", totle2)
print(name3, "    ", price3, "    ", num3, "    ", totle3)
print("==========总计==========")
print("总计：", totle)
print("==========谢谢惠顾！==========")