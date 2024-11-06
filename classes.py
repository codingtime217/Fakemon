

def readFile(fileName):
    file = open(fileName,"rt")#reads file in accordance to how I set it up
    data = {}
    for line in file:
        info = line.split(":")
        info[1] = info[1].strip("\n")
        info[1] = info[1].split(";")
        for i in range(0,len(info[1])):
            if "," in info[1][i]:
                info[1][i] = info[1][i].split(",")
        data[info[0]] = info[1]
    file.close()
    return data



def setup():
    def makethetypesdict(fileName,type,dict={}):
        list = readFile(fileName)
        for i in list.keys():
            dict[i] = type
        return dict
    waterTypes = makethetypesdict("waterPokes.txt","water")
    fireTypes = {}
    grassTypes = {}
    airTypes = {}
    global pokeDatabase
    pokeDatabase = {**waterTypes,**fireTypes,**grassTypes,**airTypes}
setup()






class pokemon():
    XpThresholds = [1000, 1090, 1188, 1295, 1412000, 1090, 1188, 1295, 1412, 1539, 1677, 1828, 1993, 2172, 2367, 2580, 2813, 3066, 3342, 3642, 3970, 4328, 4717, 5142] #xp thresholds for each level up
    def __init__(self,actualname = "",hp=1,dodge = 5,speed = 0,xp=0,level =1,scaleing = [1,1,1],attacks = None,type=None,evolution = None,givenname = ""):
        self.hp = {"current":hp,"max":hp}
        self.actualname = actualname
        if givenname == "":
            self.givenName = actualname
        else:
            self.givenName = givenname
        self.dodge = dodge
        self.speed = speed
        self.type = type
        self.xp = xp
        self.level = level
        self.scaleing = scaleing
        self.attacks = attacks
        self.evolution = evolution

        #defines values for all fakemon
    def levelUp(self,force = False):
        if force == True:
            self.level += 1
            self.hp["max"] += self.scaleing[0]
            self.dodge += self.scaleing[1]
            self.speed += self.scaleing[2]
            self.hp["current"] = self.hp["max"]
            return
        try:
            if self.xp >= pokemon.XpThresholds[self.level-1]:
                self.xp -= pokemon.XpThresholds[self.level-1]
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
        data = readFile(self.type + "Moves.txt")[attack]
        print(attack + str(data))
        return data
    

    def evolve(self):
        self.__dict__ = createPoke(self.evolution,True,self).__dict__


class character():
    def __init__(self,pokemon ={},level=0,name = "TestyMcTestFace"):
        self.pokemon = pokemon
        self.level = level
        self.name = name

class combat():
    def __init__(self,playerPs=character(),enemyPs=character(),currentPs=["",""]):
        self.playerPs = playerPs.pokemon
        self.enemyPs = enemyPs.pokemon
        self.currentPs = currentPs

    def turn(self):
        pass


class testType(pokemon):
    def __init__(self):
        pokemon.__init__(self = self,name = "TestyMcTestFace",type = "Test")



def createPoke(pokeName,evolving = False, old=pokemon()): #generalised fucntion to create pokemon objects of a given pokemon name (ie "Pikachu")
    type = pokeDatabase[pokeName]
    stats = readFile(type + "Pokes.txt")[pokeName]
    given = ""
    while len(stats) < 7:
        stats.append(None)
    if evolving == True:
        if old.givenName != old.actualname:
            given = old.givenName
        stats[5] = old.attacks
    else:
        stats[5] = [stats[5]]
    for i in range(0,5):
        if i == 4:
            for j in range(0,3):
                stats[i][j] = int(stats[i][j])
        else:
            stats[i] = int(stats[i])
    poke = pokemon(actualname=pokeName,hp=stats[0],dodge=stats[1],speed=stats[2],type=type,scaleing=stats[4],attacks=stats[5],evolution=stats[6],givenname=given)
    for i in range(0,stats[3]-1):
        poke.levelUp(force = True)
    return poke
