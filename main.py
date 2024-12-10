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

name = input("What would you like to called: \n")
player = character(name = name)
type = listOfTypes[options(listOfTypes,["type of pokemon","start"])]
availible = levelsDict[1][type]
starter = availible[options(availible,["pokemon","pick"])]
name = input("What would you like to nmae your pokemon? \n")
player.pokemon.append(createPoke(starter,name))
print(player.pokemon)
