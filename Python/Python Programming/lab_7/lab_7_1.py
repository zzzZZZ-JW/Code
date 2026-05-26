from datetime import date

class Student:
    def __init__(self,student_id,name,birthday):
        self.student_id = student_id
        self.name = name
        self.birthday = birthday

    def get_age(self):
        today = date.today()
        age = today.year - self.birthday.year
        if today.month < self.birthday.month:
            age = age - 1
        elif today.month == self.birthday.month and today.day < self.birthday.day:
            age = age - 1
        return age

s = Student("2506456052","张佳伟",date(2007,2,27))

print(s.student_id)
print(s.name)
print(s.birthday)
print(s.get_age())