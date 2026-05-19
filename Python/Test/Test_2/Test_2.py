import random
import re

with open(r'poems.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

lines = random.choice(lines)
pmlist = re.