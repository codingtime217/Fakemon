from classes import *
boi = createPoke("Wooper")
boi.xp = 10000000000000
for i in range(0,10):
    boi.levelUp()
    print(boi.level)
print(boi.attacks)