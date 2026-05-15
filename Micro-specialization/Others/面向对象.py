class Student:
    def __init__(self,name,score):
        self.name = name
        self.score = score

    def introduce(self):
        print('%s:%s'%(self.name,self.score))