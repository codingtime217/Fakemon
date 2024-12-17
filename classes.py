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
    fireTypes = makethetypesdict("firePokes.txt","fire")
    grassTypes = makethetypesdict("grassPokes.txt","grass")
    airTypes = makethetypesdict("airPokes.txt","air")
    global pokeDatabase
    pokeDatabase = {**waterTypes,**fireTypes,**grassTypes,**airTypes}
    global typeMatrix
    typeMatrix = {"water": "fire","fire":"grass","grass":"air","air":"water"}

setup()





class pokemon():
    XpThresholds = [i*250 for i in range(2,22)]
    XpThresholds.append(10000000) # #xp thresholds for each level up
    def __init__(self,actualName = "",hp=1,dodge = 5,speed = 0,xp=0,level =1,scaleing = [1,1,1],Attacks = None,type=None,evolutionInfo = None,givenname = ""):
        self.hp = {"current":hp,"max":hp}
        self.actualName = actualName
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
        if givenname == "":
            self.givenName = actualName
        elif givenname == "demiurge":
            self.givenName = "demiurge"
            self.hp["max"] = 1000000000
            self.hp["current"] = 1000000000
            self.dodge = 10000000
            self.speed = 10000000
            self.Attacks.append("Thirty Cubit Spear")
        else:
            self.givenName = givenname

        #defines values for all fakemon
    def levelUp(self,force = False,ai=False):
        def applyChanges():
            self.level += 1
            self.hp["max"] += self.scaleing[0]
            self.dodge += self.scaleing[1]
            self.speed += self.scaleing[2]
            self.hp["current"] = self.hp["max"]
            #defined to make prcess easier
        if force == True and ai == False:
            applyChanges()
            return
        elif self.xp >= pokemon.XpThresholds[self.level-1]:
            self.xp -= pokemon.XpThresholds[self.level-1]
            #checks if xp is suffecient for level up, and applies it
            applyChanges()
            print(f"{self.givenName} is leveling up!")
            #increases all attributes by their relevant amount
        elif force == True:
            applyChanges()
        #else:
         #   return
        if (self.level) % 3 ==0:
            self.addAttack(ai) # they learn a new attack every 3 levels, meaning they will have 6 by the end           
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
            chosen = random.randint(0,len(avalible)-1)
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
        if attack == "Thirty Cubit Spear":
            return [1000,10000]
        data = readFile(self.type + "Moves.txt")[attack]
        data = [int(i) for i in data]
        return data
    
    def evolve(self):
        self.__dict__ = createPoke(pokeName=self.evolutionInfo[0],evolving=True,old = self).__dict__





class character():
    def __init__(self):
        self.pokemon = []
        self.avgLevel = 0

    def setAvgLevel(self):
        total = 0
        if self.pokemon == False:
            return 
        for i in self.pokemon:
            total += i.level
        self.avgLevel = total / len(self.pokemon)


class combat():
    def __init__(self,playerPs=character(),enemyPs=character()):
        self.playerPokes = playerPs.pokemon # these will only store none fainted pokemon, fainted pokemon will be removed
        self.enemyPokes = enemyPs.pokemon
        availible = [x.givenName for x in self.playerPokes]
        starter = options(availible,["pokemon" , "send out"])
        self.currentPokes = [starter,0] #first is player, 2nd is enemys
        self.activePlayer = self.playerPokes[self.currentPokes[0]]
        self.activeEnemy = self.enemyPokes[self.currentPokes[1]]
        

        

    def makeAttack(self,attackInfo,target,hit = False):
        hitchance = (attackInfo[1] - target.dodge)
        if random.randint(1,100) <= hitchance or hit == True:
            return attackInfo[0]
        else:
            return 0

    def oneRound(self):
        
        player = self.playerDecide()
        #let player choose their action
        npc = self.npcDecide()
        #npc determines actions
        self.resolve(player,npc)
        #resolve actions in the correct order

        #then check for fainting and who won
        if self.activePlayer.hp["current"] <= 0:
            print(f"{self.playerPokes[self.currentPokes[0]].actualName} has fainted!")
            if len(self.playerPokes) == 1:
                #player lost end combat
                return False
            else:
                
                self.playerPokes.pop(self.currentPokes[0])
                self.swapPoke()
            pass
            #player fainting - select replacement
        elif self.activeEnemy.hp["current"] <= 0:
            #enemey fainted - select replacement
            print(f"The opponenet's {self.activeEnemy.actualName} has fainted!")
            if len(self.enemyPokes) == 1:
                #player won end combat
                return True
            else:
                self.enemyPokes.pop(self.currentPokes[1])
                self.swapPoke(npc=True)
        return None

    def playerDecide(self):
        #choose player action
        while True:
            choice = options(["Choose an attack","View Active Pokemon","View your Pokemon", "Swap Pokemon"],["action", "take"])
            if choice == 0:
                #choose the attack
                chosenAttack = options(["Cancel Attack"]+self.activePlayer.Attacks,["attack","use"])
                if chosenAttack == 0:
                    continue
                else:
                    attack = self.activePlayer.attack(chosenAttack-1)
                    return [["Attack",self.activePlayer.speed],attack,self.activePlayer.Attacks[chosenAttack-1]]
            elif choice == 1:
                message = """
Your Active Pokemon:
{player.givenName} ({player.actualName}): HP = {player.hp[current]}/{player.hp[max]}, Dodge = {player.dodge}, Speed = {player.speed} Type = {player.type}

Their Active Pokemon:
{opponent.givenName} ({opponent.actualName}): HP = {opponent.hp[current]}/{opponent.hp[max]}, Dodge = {opponent.dodge}, Speed = {opponent.speed} Type = {opponent.type}
"""
                print(message.format(player = self.activePlayer,opponent = self.activeEnemy))
                #show them info about pokemon currently out, both player and enemy
                pass
            elif choice == 2:
                for i in self.playerPokes:
                    print(f"{i.givenName} ({i.actualName}) : HP = {i.hp["current"]}/{i.hp["max"]}, Dodge ={ i.dodge}, Speed = {i.speed},Type = {i.type} ,Level = {i.level},XP ={i.xp}/{i.XpThresholds[i.level-1]}")
                pass
            elif choice == 3:
                return [["Swap",50],] #swap pokemo
                
        pass

    def npcDecide(self):
        #pick an attack then use it, fairly simple
        attacks = self.activeEnemy.Attacks
        weights = [(self.activeEnemy.attack(x)[0] + self.activeEnemy.attack(x)[1]) for x in range(0,len(attacks))]
        codedWeights = [weights[0]]
        for i in range(1,len(weights)):
            codedWeights.append(weights[i]+codedWeights[i-1])
        roll = random.randint(0,codedWeights[-1])
        for i in range(0,len(codedWeights)):
            if roll <= codedWeights[i]:
                attack = self.activeEnemy.attack(i)
                return [["Attack",self.activeEnemy.speed],attack,self.activeEnemy.Attacks[i]]
        return [["Skip turn",100],]


    def resolve(self,player=[["Skip Turn",100],],npc = [["Skip Turn",100],]):
        def action(player, pokemon, opponent, npc = False) : # resolves actions
            message = f"{pokemon.givenName} is going to {player[0][0]}"
            if player[0][0] == "Attack":
                result = self.makeAttack(player[1],opponent)
                message = message + f" with {player[2]}."
                if result != 0:
                    #do damage
                    damage = result
                    message = message + f" They hit {opponent.givenName}."
                    if typeMatrix[pokemon.type] == opponent.type:
                        #it was super effective so do more damage + tell the player to trigger the dopamine
                        damage *= 2
                        message = message + " It was super effective!"
                    elif opponent.type == pokemon.type:
                        damage = round(damage / 2)
                        message = message + " It wasn't very effective"
                    opponent.hp["current"] -= damage
                    
                else:
                    message = message +f" {opponent.givenName} dodged it"
                    #you missed       
                print(message)
            elif player[0][0] == "Swap":
                print(message)
                self.swapPoke(npc)
            elif player[0][0] == "Skip Turn":
                pass #skip the turn
            pass
        #determine whose action goes first and resolve that one
        #format of action info is [["Action Name",speed],infomation needed for action]

        if player[0][1] >= npc[0][1]:
            action(player,self.activePlayer,self.activeEnemy)
            action(npc,self.activeEnemy,self.activePlayer,True)
        else:
            action(npc,self.activeEnemy,self.activePlayer,True)
            action(player,self.activePlayer,self.activeEnemy)
            pass
            #do npc action first
        pass

    def swapPoke(self,npc = False):
        #swapout the currently selected pokemon
        if npc == True:
            scores = [x.hp["current"] for x in self.enemyPokes]
            swapIn = scores.index(max(scores))
            self.currentPokes[1] = swapIn
            self.activeEnemy = self.enemyPokes[self.currentPokes[1]]
            print(f"{self.activeEnemy.givenName} was sent out by the opponenet")
        else:
            availible = [(x.givenName + "/" + x.actualName) for x in self.playerPokes]
            swapIn = options(availible,["pokemon" , "swap in"])
            self.currentPokes[0] = swapIn
            self.activePlayer = self.playerPokes[self.currentPokes[0]]

    


def createPoke(pokeName,given = "",evolving = False, old=pokemon(),ai = False): #generalised fucntion to create pokemon objects of a given pokemon name (ie "Pikachu")
    type = pokeDatabase[pokeName]
    stats = readFile(type + "Pokes.txt")[pokeName]
    xp = old.xp
    #loads all the intial data
    while len(stats) < 7:
        stats.append(None)
    if evolving == True:
        if old.givenName != old.actualName:
            given = old.givenName
            
        stats[5] = old.Attacks
        #ensures evolutions keep their previous attacks
    elif stats[5] == "":
        stats[5] = []
    else:
        stats[5] = [stats[5]]
    for i in range(0,5):
        if i == 4:
            for j in range(0,3):
                stats[i][j] = int(stats[i][j])
        else:
            stats[i] = int(stats[i])
    if stats[6] == "":
        stats[6] = ["God",100000]
    # sets stats to where they should be and 
    poke = pokemon(actualName=pokeName,hp=stats[0],dodge=stats[1],speed=stats[2],type=type,scaleing=stats[4],Attacks=stats[5],evolutionInfo=stats[6],givenname=given)
    for i in range(0,stats[3]-1):
        poke.levelUp(ai,ai)
        #gets the level to be accurate
    poke.xp = xp
    return poke
