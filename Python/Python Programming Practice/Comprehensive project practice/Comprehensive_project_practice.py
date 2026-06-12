import random


class Poem:
    def __init__(self, title, author, lines):
        self.title = title
        self.author = author
        self.lines = lines
    
def load_poem(poemfiles):
    poems = []

    file = open(poemfiles, 'r', encoding='utf-8')

    for line in file:
        line = line.strip()

        if line == "":
            continue
        
        parts = line.split('|')

        title = parts[0]
        author = parts[1]
        text = parts[2]

        lines = text.split(',')

        poem = Poem(title, author, lines)

        poems.append(poem)
    
    file.close()
    return poems

def make_question(poems):
    poem = random.choice(poems)
    






