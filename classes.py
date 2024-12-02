import random
import glob

def readFile(fileName,byIndex = False):
    path = glob.glob(f"Data/{fileName}",recursive=True)[0] # find the path to the file with glob - allows me to put them in a folder
    with open(path,"r") as file: #reads file in accordance to how I set it up, using with to ensure it is closed
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
    return data

def options(option=[],thingBeingChosen= ["noun","verb"]):
    newLine = "\n"
    check = ""
    toDisplay = f"Pick the {thingBeingChosen[0]} to {thingBeingChosen[1]}{newLine}"
    for i in range(0,len(option)):
        toDisplay = toDisplay + f"{i} - {option[i]}{newLine}"
    while True:
        try:
            choice = int(input(toDisplay).strip())
            if choice >= len(option) or choice < 0:
                raise IndexError
            return choice
        except (ValueError, IndexError):
            print("Not valid option")
            choice = None

def setup():
    def makethetypesdict(fileName,type):
        dictionary = readFile(fileName)
        for i in dictionary.keys():
            dictionary[i] = type
        return dictionary
    waterTypes = makethetypesdict("waterPokes.txt","water")
    fireTypes = {}
    grassTypes = {}
    airTypes = {}
    global pokeDatabase
    pokeDatabase = {**waterTypes,**fireTypes,**grassTypes,**airTypes}
    global typeMatrix
    typeMatrix = {"water": "fire","fire":"grass","grass":"air","air":"water"}

setup()





class pokemon():
    XpThresholds = [1000, 1090, 1188, 1295, 1412000, 1090, 1188, 1295, 1412, 1539, 1677, 1828, 1993, 2172, 2367, 2580, 2813, 3066, 3342, 3642, 3970, 4328, 4717, 5142] #xp thresholds for each level up
    def __init__(self,actualname = "",hp=1,dodge = 5,speed = 0,xp=0,level =1,scaleing = [1,1,1],Attacks = None,type=None,evolutionInfo = None,givenname = ""):
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
        self.Attacks = Attacks
        self.evolutionInfo = evolutionInfo
        if self.evolutionInfo == None:
            self.evolutionInfo == [None,1000000]

        #defines values for all fakemon
    def levelUp(self,force = False,ai=False):
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
        if self.xp >= pokemon.XpThresholds[self.level-1]:
            self.xp -= pokemon.XpThresholds[self.level-1]
            #checks if xp is suffecient for level up, and applies it
            applyChanges()
            #increases all attributes by their relevant amount
        if (self.level - 1) % 3 ==0:
            if ai == True:
                self.addAttack(True) # they learn a new attack every 3 levels, meaning they will have 6 by the end
            else:
                self.addAttack()           
        if self.level >= int(self.evolutionInfo[1]):
            print(f"{self.givenName} is evolving into a {self.evolutionInfo[0]}")
            self.evolve()
    
    def addAttack(self,npc = False):
        def removeDuplicates(current,new):
            output = [] # used to check for duplicate attacks (already learned)
            for i in range(0,len(new)):
                if not new[i] in current:
                    output.append(new[i])
            return output
        file = self.type + "Moves.txt"
        data = readFile(file,True)
        avalible = []
        for i in data.keys():
            if i <= self.level:
                try:
                    for j in data[i]:
                        avalible.append(j)
                except AttributeError:
                    avalible.append(data[i]) # makes a list of attack availible to learn
            avalible = removeDuplicates(self.Attacks,avalible)
        if npc == True:
            
            if len(self.Attacks) >= 6:
                self.Attacks.pop(0)
            chosen = random.randint(0,len(avalible))
            self.Attacks.append(avalible[chosen])
            return
        else: 
            print(f"{self.givenName} can learn a new move")
            
            newLine = "\n"
            if len(self.Attacks) >= 6:
                toShow = ""
                for i in self.Attacks[0:3]:
                    toShow = toShow + i + ", "
                toShow = toShow + self.Attacks[4] + " and " + self.Attacks[5]
                choice = input(f"Currently {self.givenName} has {toShow}. Would you like you like to replace an attack? Y/N {newLine}")
                while True:
                    if choice.lower() == "n":
                        print(f"{self.givenName} will keep their current Attacks")
                        return
                    elif choice.lower() == "y":
                        break
                    else:
                        choice = input("That was not a valid option, would you like to replace an attack? Y/N \n")
                while True:
                    try:
                        replace = input("Which attack would you like to replace \n").strip().lower()
                        self.Attacks.remove(replace.title())
                        break
                    except ValueError:
                        print(f"{self.givenName} does not have that move, they have {toShow}.")
            chosen = options(avalible,["attack", "learn"])
            self.Attacks.append(avalible[chosen])

    def attack(self,choice):
        attack = self.Attacks[choice]
        data = readFile(self.type + "Moves.txt")[attack]
        data = [int(i) for i in data]
        print(data)
        return data
    
    def evolve(self):
        self.__dict__ = createPoke(pokeName=self.evolutionInfo[0],evolving=True,old = self).__dict__








class character():
    def __init__(self,pokemon =[],level=0,name = "TestyMcTestFace"):
        self.pokemon = pokemon
        self.level = level
        self.name = name



class combat():
    def __init__(self,playerPs=character(),enemyPs=character()):
        self.playerPokes = playerPs.pokemon # these will only store none fainted pokemon, fainted pokemon will be removed
        self.enemyPokes = enemyPs.pokemon
        availible = [x.givenName for x in self.playerPokes]
        starter = options(availible,["pokemon" , "send out"])
        self.currentPokes = [starter,0] #first is player, 2nd is enemys
        self.activePlayer = self.playerPokes[self.currentPokes[0]]
        self.activeEnemy = self.enemyPokes[self.currentPokes[1]]
        

        

    def makeAttack(self,attackInfo,target):
        hitchance = (attackInfo[1] + target.dodge) / 2
        if random.randint(1,101) <= hitchance:
            return attackInfo[0]
        else:
            return 0

    def oneRound(self):
        
        player = self.playerDecide()
        npc = self.npcDecide()
        self.resolve(player,npc)
        #pick npc attack
        #choose player action
        #determine resolution order
        #resolve
        #process status effects
        #check for fainting
        if self.activePlayer.hp["current"] <= 0:
            print(f"{self.playerPokes[self.currentPokes[0]].actualname} has fainted!")
            if len(self.playerPokes) == 1:
                #player lost end combat
                print("You lost lol")
                pass
            else:
                
                self.playerPokes.pop(self.currentPokes[0])
                self.swapPoke()
            pass
            #player fainting - select replacement
        elif self.activeEnemy.hp["current"] <= 0:
            #enemey fainted - select replacement
            print(f"The opponenet's {self.activeEnemy.actualname} has fainted!")
            if len(self.enemyPokes) == 1:
                #player won end combat
                pass
            else:
                self.enemyPokes.pop(self.currentPokes[1])
                self.swapPoke(npc=True)
        pass

    def playerDecide(self):
        #choose player action
        while True:
            choice = options(["Choose an attack","View your Pokemon", "Swap Pokemon"],["action", "take"])
            if choice == 0:
                #choose the attack
                chosenAttack = options(["Cancel Attack"]+self.activePlayer.Attacks,["attack","use"])
                if chosenAttack == 0:
                    continue
                else:
                    attack = self.activePlayer.attack(chosenAttack-1)
                    return [["Attack",self.activePlayer.speed],attack]
                pass
            elif choice == 1:
                #show them their pokemone
                pass
            elif choice == 2:
                return [["Swap",50],] #swap pokemon

        pass

    def npcDecide(self):
        #determine the AI's action
        return [["Skip turn",100],]
        pass
    def resolve(self,player=[["Skip Turn",100],],npc = [["Skip Turn",100],]):
        def playerAction(player = [[["Skip Turn",100],]]):
            if player[0][0] == "Attack":
                result = self.makeAttack(player[1],target = self.activeEnemy)
                if result != 0:
                    #do damage
                    damage = result
                    if typeMatrix[self.activePlayer.type] == self.activeEnemy.type:
                        #it was super effective so do more damage + tell the player to trigger the dopamine
                        damage *= 2
                        print(f"")
                    else:
                        #deal damage normally
                        pass
                    pass
                else:
                    print("You missed lol")
                    #you missed       
                    pass
            elif player[0][0] == "Swap":
                self.swapPoke()
            elif player[0][0] == "Skip Turn":
                pass #skip the turn
            pass
            #do player action first
        def npcAction(npc):
            if npc[0][0] == "Swap":
                self.swapPoke("npc")
            #resolve npc actions
            pass
        #determine whose action goes first and resolve that one
        #format of action info is [["Action Name",speed],infomation needed for action]

        if player[0][1] >= npc[0][1]:
            playerAction(player)
            npcAction()
        else:
            npcAction()
            playerAction(player)
            pass
            #do npc action first
        pass

    def swapPoke(self,who = None):
        #swapout the currently selected pokemon
        if who == "npc":
            scores = [x.hp["current"] for x in self.enemyPokes]
            swapIn = scores.index(max(scores))
            self.currentPokes[1] = swapIn
            self.activeEnemy = self.enemyPokes[self.currentPokes[1]]
        else:
            availible = [x.givenName for x in self.playerPokes]
            swapIn = options(availible,["pokemon" , "swap in"])
            self.currentPokes[0] = swapIn
            self.activePlayer = self.playerPokes[self.currentPokes[0]]

    


def createPoke(pokeName,given = "",evolving = False, old=pokemon()): #generalised fucntion to create pokemon objects of a given pokemon name (ie "Pikachu")
    type = pokeDatabase[pokeName]
    stats = readFile(type + "Pokes.txt")[pokeName]
    xp = old.xp
    while len(stats) < 7:
        stats.append(None)
    if evolving == True:
        if old.givenName != old.actualname:
            given = old.givenName
            
        stats[5] = old.Attacks
    else:
        stats[5] = [stats[5]]
    for i in range(0,5):
        if i == 4:
            for j in range(0,3):
                stats[i][j] = int(stats[i][j])
        else:
            stats[i] = int(stats[i])
    if stats[6] == "":
        stats[6] = ["",100000]
    poke = pokemon(actualname=pokeName,hp=stats[0],dodge=stats[1],speed=stats[2],type=type,scaleing=stats[4],Attacks=stats[5],evolutionInfo=stats[6],givenname=given)
    for i in range(0,stats[3]-1):
        poke.levelUp(force = True,ai = False)
    poke.xp = xp
    return poke

player = character([createPoke("Wooper"),createPoke("Mudkip"),createPoke("Quagsire")])
enemy = character([createPoke("Mudkip"),createPoke("Wooper")],0,"Enemy Man")
fight = combat(player,enemy)