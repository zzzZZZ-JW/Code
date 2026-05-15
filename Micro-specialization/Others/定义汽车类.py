def overload(self,num_passengers):
    print(f"该车的核载人数为：{self.seats}人。")
    if num_passengers > self.seats:
        result = '您已超载，请减少乘客人数！'
    else:
        result = '乘客人数符合规定，可以出发！'
    print(f'当前载客数量为：{num_passengers}人，{result}')