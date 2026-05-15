def get_max_min_num(s):
    result_max = max(s)
    result_min = min(s)
    result_count = len(s)
    return result_max, result_min, result_count

list1 = [9 , 7 , 8 , 3 , 2 , 1 , 55 , 6]
print("list1 =", list1)
print(f"最大值={get_max_min_num(list1)[0]}，最小值={get_max_min_num(list1)[1]}，元素个数={get_max_min_num(list1)[2]}")
list2 = ["apple" , "pear" , "melon" , "kiwi"]
print("list2 =", list2)
print(f"最大值={get_max_min_num(list2)[0]}，最小值={get_max_min_num(list2)[1]}，元素个数={get_max_min_num(list2)[2]}")
list3 = "TheQuickBrownFox"
print("list3 =", list3)
print(f"最大值={get_max_min_num(list3)[0]}，最小值={get_max_min_num(list3)[1]}，元素个数={get_max_min_num(list3)[2]}")