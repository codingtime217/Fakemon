from classes import *
listOfTypes = ["Fire","Water","Grass","Air"]
levelsDict = {
1:{
    "Fire":["Charmander","Vulpix","Cyndaquil","Torchic"],
    "Water":["Wooper","Mudkip","Squirtle","Psyduck"],
    "Grass":["Bulbasaur","Tangela","Turtwig","Snivy"],
    "Air":["Rookidee","Pidgey","Noibat","Rufflet"]}
,6:{
    "Fire":["Charmeleon","Quilava","Combusken"],
    "Water":["Marshtomp","Wartortle"],
    "Grass":["Ivysaur","Grotle","Servine"],
    "Air":["Corvisquire","Pidgeotte"]}
,10:{
    "Fire":["Ninetales"],
    "Water":["Quagsire","Golduck"],
    "Grass":["Tangrowth"],
    "Air":["Noivern","Braviary"]}
,12:{
    "Fire":["Charizard","Typhlosion","Blaziken"],
    "Water":["Swampert","Blastoise"],
    "Grass":["Venasaur","Torterra","Serperior"],
    "Air":["Corviknight","Pidgeot"]} }
#big dictionary storing all the pokemon names sorted by type and by inital level
# need to make a system for - done
#generating sets of opponet pokeomn - deon
#gaining new pokemon as a player - done
#starting -sort of done
#healing pokemon every few battles
#victory message if you reach the end

def createEnemy(noPokes,level):
    enemy = character()
    level = min(1,level - 2)
    temp = [abs(x-level) for x in levelsDict.keys()]
    keys = list(levelsDict.keys())
    levelThreshold = keys[temp.index(min(temp))]
    possible = levelsDict[levelThreshold]
    #determines which range of pokemon to randomly select from, to ensure evolutions only appear after the player should have one
    for i in range(0,noPokes):
        type = listOfTypes[random.randint(0,3)]
        pokes = possible[type]
        pokeName = pokes[random.randint(0,len(pokes)-1)]
        poke = createPoke(pokeName,ai = True)
        poke.addAttack(True)
        while poke.level < level:
            poke.levelUp(force = True, ai = True)
        enemy.pokemon.append(poke)
        #adds pokemon
    enemy.setAvgLevel()
    return enemy
    
def runBattle(player):
    player.setAvgLevel() #update player's avergae pkemon level
    enemy = createEnemy(len(player.pokemon),player.avgLevel)#make an eneemy with the same number of pokemon with the same average level
    battle = combat(player,enemy)
    result = battle.oneRound()
    while result != True and result != False: # run combat until its joever
        result = battle.oneRound()
    if result == False:
        print("Unfortunately you lost this battle and the game")
        return False
    else:
        xp = min(1,enemy.avgLevel) * 500
        print(xp)
        print(f"You won! All your pokemon gain {xp} xp")
        for i in player.pokemon:
            i.hp["current"] += i.hp["max"] // 2
            i.xp += xp
            i.levelUp()
        #give xp if they win
        player.setAvgLevel()
        choices = options(["Do Not Capture Pokemon"]+[i.givenName for i in enemy.pokemon],["pokemon","capture"])
        if choices != 0:
            name = input("What would you like to name your pokemon? \n")
            newPokemon =enemy.pokemon[choices-1]
            newPokemon.givenName = name
            player.pokemon.append(newPokemon)
        #let them obtain a new pokemon if they want
        return True

def createCharacter():
    temp = character()
    type = listOfTypes[options(listOfTypes,["type of pokemon","start"])]
    availible = levelsDict[1][type]
    starter = availible[options(availible,["pokemon","pick"])]
    name = input("What would you like to name your pokemon? \n")
    #makes the player
    temp.pokemon.append(createPoke(starter,name))
    
    return temp

while options(["Play the game","Quit"],["option","do"]) == 0:
    player = createCharacter()
    while runBattle(player):
        if player.avgLevel == 20 and len(player.pokemon):
            print("You have become the very best, that no one ever was!")
            print("You win!!!!")

