class Person:
    def __init__(self , name , age):
        self.name = name
        self.age = age
    def introduce(self):
        return f"大家好，我叫{self.name}，今年{self.age}岁了。"
    
class Student(Person):
    def __init__(self , name , age , student_id , zhuanye):
        super().__init__(name , age)
        self.student_id = student_id
        self.zhuanye = zhuanye
    def introduce(self):
        return f"大家好，我是学生{self.name}，学号{self.student_id}，专业是{self.zhuanye}。"
    def study(self, subject):
        return f"{self.name}正在学习{subject}。"
    
class Teacher(Person):
    def __init__(self, name , age , id , bumen):
        super().__init__(name , age)
        self.id = id
        self.bumen = bumen
        self.course = []
    def introduce(self):
        return f"大家好，我是教师{self.name}，部门是{self.bumen}，工号{self.id}，。"
    def add_course(self, course):
        self.course.append(course)
        return f"{self.name}老师开始教授{course}课程。"
    def teach(self):
        if self.course:
            return f"{self.name}老师目前正在教授{self.course[-1]}课程。"
        else:
            return f"{self.name}教师目前没有安排课程。"

test1 = Person("张三" , 30)
print(test1.introduce())

test2 = Student("李四" , 20 , "2023001" , "计算机科学")
print(test2.introduce())
print(test2.study("Python课程"))

test3 = Teacher("王教授" , 45 , "T1001" , "计算机学院")
print(test3.introduce())
print(test3.add_course("Python编程"))
print(test3.teach())
