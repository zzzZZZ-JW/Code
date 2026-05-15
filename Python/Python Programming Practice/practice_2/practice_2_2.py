weight, height = eval(input("请输入体重[单位:kg]，身高[单位：cm]，两个数据之间用英文逗号分隔"))
height /= 100 
BMI = weight/height**2
if BMI<18.5:
    print("偏瘦：低（但其他疾病危险性增加）")
elif 18.5<=BMI<24.0:
    print("正常：平均水平")
elif 24<=BMI<27.0:
    print("偏胖：增加")
elif 27<=BMI<30.0:
    print("肥胖：中度增加")
else:
    print("重度肥胖：严重增加")