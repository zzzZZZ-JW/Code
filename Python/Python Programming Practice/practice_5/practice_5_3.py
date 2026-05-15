import re

class Poem:
    def __init__(self, title, dynasty, author):
        self.title = title
        self.dynasty = dynasty
        self.author = author

    def setContent(self, contList=[]):
        self.contentList = contList[:]

    def getFcontent(self):
        lg = len(self.contentList[0])
        poet = self.dynasty + '·' + self.author
        poet = self.title.center(lg) + '\n' + poet.center(lg) + '\n'
        poet += '\n'.join(self.contentList)
        return poet


if __name__ == '__main__':
    poemA = Poem('登鹳雀楼', '唐', '李白')
    cont = '白日依山尽,黄河入海流。欲穷千里目,更上一层楼。'
    poemA.setContent(re.split(',|。', cont))
    print(poemA.getFcontent())

    poemB = Poem('山居秋暝', '唐', '王维')
    cont = '空山新雨后,天气晚来秋。明月松间照,清泉石上流。'
    poemB.setContent(re.split(',|。', cont))
    print(poemB.getFcontent())
