XpThresholds = [1000, 1090, 1188, 1295, 1412, 1539, 1677, 1828, 1993, 2172, 2367, 2580, 2813, 3066, 3342, 3642, 3970, 4328, 4717, 5142]

class pokemon():
    def __init__(self,name = "",hp=1,dodge = 5,speed = 0,type=None,xp=0,level =1,scaleing = [1,1,1],attacks = None):
        self.hp = {"current":hp,"max":hp}
        self.name = name
        self.dodge = dodge
        self.speed = speed
        self.type = type
        self.xp = xp
        self.level = level
        self.scaleing = scaleing
        self.attacks = attacks
        #defines values for all fakemon
    def levelUp(self):
        try:
            if self.xp >= XpThresholds[self.level-1]:
                self.xp -= XpThresholds[self.level-1]
                self.level += 1
                #checks if xp is suffecient for level up, and applies it
                self.hp["max"] += self.scaleing[0]
                self.dodge += self.scaleing[1]
                self.speed += self.scaleing[2]
                #increases all attributes by their relevant amount
        except:
            pass
    def attack(self,choice):
        attack = self.attacks[choice]
    def evolve(self):
        pass

class testType(pokemon):
    def __init__(self):
        pokemon.__init__(self = self,name = "TestyMcTestFace",type = "Test")
