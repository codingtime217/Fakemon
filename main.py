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
# need to make a system for:
#generating sets of opponet pokeomn
#gaining new pokemon as a player
#starting
#victory message if you reach the end

def createEnemy(noPokes,level):
    enemy = character()
    print(f"enemy = {enemy.pokemon}")
    temp = [abs(x-level) for x in levelsDict.keys()]
    keys = list(levelsDict.keys())
    levelThreshold = keys[temp.index(min(temp))]
    possible = levelsDict[levelThreshold]
    for i in range(0,noPokes):
        type = listOfTypes[random.randint(0,3)]
        pokes = possible[type]
        pokeName = pokes[random.randint(0,len(pokes)-1)]
        poke = createPoke(pokeName,ai = True)
        poke.addAttack(True)
        while poke.level < level:
            poke.levelUp(force = True, ai = True)
        enemy.pokemon.append(poke)
    enemy.setAvgLevel()
    return enemy
    
def runBattle(player):
    player.setAvgLevel()
    enemy = createEnemy(len(player.pokemon),player.avgLevel)
    print(f"enemy: {enemy.pokemon}")
    battle = combat(player,enemy)
    result = battle.oneRound()
    while result != True and result != False:
        result = battle.oneRound()
    if result == False:
        print("Unfortunately you lost this battle and the game")
        return False
    else:
        xp = enemy.avgLevel * 100
        print(f"You won! All your pokemon gain {xp}")
        for i in player.pokemon:
            i.xp += xp
            i.levelUp()
        player.setAvgLevel

def createCharacter():
    temp = character()
    type = listOfTypes[options(listOfTypes,["type of pokemon","start"])]
    availible = levelsDict[1][type]
    starter = availible[options(availible,["pokemon","pick"])]
    name = input("What would you like to name your pokemon? \n")
    temp.pokemon.append(createPoke(starter,name))
    return temp

player = createCharacter()
print(f"Plater :{player.pokemon}")
runBattle(player)
