class Temperature:
    def __init__(self , degree):
        self.degree = degree
    
    def ToFahrenheit(self):
        return self.degree * 1.8 + 32
    
    def ToCelsius(self):
        return (self.degree - 32) / 1.8
    
t1 = float(input("请输入摄氏温度："))
huashi = Temperature(t1)
print("华氏温度为：", huashi.ToFahrenheit())
t2 = float(input("请输入华氏温度："))
sheshi = Temperature(t2)
print("摄氏温度为：", sheshi.ToCelsius())
