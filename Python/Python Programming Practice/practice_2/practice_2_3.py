import random

blood = random.randint(1, 100)

while blood > 0:
    npc = random.randint(1,4)
    print("血量：", blood)
    print("本次遇到的NPC：", npc)
    if npc == 1:
        print("捡到金币，血量加10")
        blood = blood + 10
    elif npc == 2:
        print("捡到银币，血量加5")
        blood = blood + 5
    elif npc == 3:
        print("捡到铜币，血量加1")
        blood = blood + 1
    elif npc == 4:
        print("遇到怪兽，血量减50")
        blood = blood - 50

print("游戏结束")