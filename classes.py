

def readFile(fileName,byIndex = False):
    file = open(fileName,"rt")#reads file in accordance to how I set it up
    data = {}
    for line in file:
        info = line.split(":")
        info[1] = info[1].strip("\n")
        info[1] = info[1].split(";")
        for i in range(0,len(info[1])):
            if "," in info[1][i]:
                info[1][i] = info[1][i].split(",")
        if byIndex == False:
            if "," in info[0]:          
                info[0] = info[0].split(",")
                data[info[0][0]] = info[1]
            else:
                data[info[0]] = info[1]    
            #turns the file into a dictionary based on the name of each record
        else:
            info[0] = info[0].split(",")
            info[0][1] = int(info[0][1])
            if info[0][1] not in data.keys():
                data[info[0][1]] = [info[0][0]]
            else:
                data[info[0][1]].append(info[0][0])
            #turns the file into a dictionary based on the number attached to each record
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
        def applyChanges():
            self.level += 1
            self.hp["max"] += self.scaleing[0]
            self.dodge += self.scaleing[1]
            self.speed += self.scaleing[2]
            self.hp["current"] = self.hp["max"]
            #defined to make prcess easier
        if force == True:
            applyChanges()
            return
        try:
            if self.xp >= pokemon.XpThresholds[self.level-1]:
                self.xp -= pokemon.XpThresholds[self.level-1]
                #checks if xp is suffecient for level up, and applies it
                applyChanges()
                #increases all attributes by their relevant amount
            if (self.level - 1) % 3 ==0:
                print("learning new attack")
                self.addAttack() # they learn a new attack every 3 levels, meaning they will have 6 by the end
        except:
            pass
    
    def addAttack(self):
        def removeDuplicates(current,new):
            output = [] # used to check for duplicate attacks (already learned)
            for i in range(0,len(new)):
                if not new[i] in current:
                    output.append(new[i])
            return output
        print("running function")
        file = self.type + "Moves.txt"
        data = readFile(file,True)
        avalible = []
        for i in data.keys():
            if i <= self.level:
                try:
                    for j in data[i]:
                        avalible.append(j)
                except:
                    avalible.append(data[i]) # makes a list of attack availible to learn
        avalible = removeDuplicates(self.attacks,avalible)
        print(avalible)
        toDisplay = (f"""{self.givenName} can learn a new move, enter the associated number to pick the new move:
""")
        newLine = "\n"
        for i in range(0,len(avalible)):
            toDisplay = toDisplay + f"{i} - {avalible[i]}{newLine}"
        toDisplay = toDisplay + "\n"

        while True:
            try:
                chosen = int(input(toDisplay))
                break
            except:
                print("Enter the integer that corresponds with the attack")
        self.attacks.append(avalible[chosen])

    def attack(self,choice):
        attack = self.attacks[choice]
        data = readFile(self.type + "Moves.txt")[attack][1]
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
        self.playerPokes = playerPs.pokemon
        self.enemyPokes = enemyPs.pokemon
        self.currentPokes = currentPs

    def oneRound(self):
        #pick npc attack
        #choose player action
        #determine resolution order
        #resolve
        #process status effects
        #check for fainting
        #if fainting - select replacement
        pass



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
