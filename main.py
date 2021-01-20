from classes.game import person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

print("\n\n")

# Create Black Magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 12, 100, "white")
cura = Spell("Cura", 18, 100, "white")

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)
grenade = Item("Granade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
enemy_spells = [fire, thunder, meteor, cure]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2},
                {"item": grenade, "quantity": 4}]

# Instantiate People
player1 = person('Dima    :', 3260, 100, 138, 34, player_spells, player_items)
player2 = person('Rinat   :', 4160, 90, 139, 34, player_spells, player_items)
player3 = person('Alma    :', 3089, 123, 155, 34, player_spells, player_items)
player4 = person('Shay-Lee:', 3333, 70, 143, 34, player_spells, player_items)

# Instantiate enemies
enemy1 = person("Pogba   :", 200, 130, 560, 325, enemy_spells, [])
enemy2 = person("Bruno   :", 1500, 700, 525, 25, enemy_spells, [])
enemy3 = person("Rashford:", 1000, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3, player4]
enemies = [enemy1, enemy2, enemy3]

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("========================")
    print("\n\n")
    # print all player stats
    print("NAME              HP                                         MP")
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("Choose Action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_terget(enemies)
            enemies[enemy].take_dmg(dmg)
            print(bcolors.FAIL + bcolors.BOLD + "\nYou attacked " + enemies[enemy].name.replace(" ", "") + "for " + str(
                dmg),
                  " points of damage." + bcolors.ENDC)
            if enemies[enemy].get_hp() == 0:
                print(bcolors.OKBLUE + bcolors.BOLD + "\n" + enemies[enemy].name.replace(" ",
                                                                                         "") + " has died" + bcolors.ENDC)
                del enemies[enemy]
                if not enemies:
                    print(bcolors.OKGREEN + "\n\nYOU WIN!!!" + bcolors.ENDC)
                    running = False
                    break

        elif index == 1:
            player.choose_magic()
            magic_choice = input("Choose Item: ")
            if magic_choice == 'b':
                continue
            magic_choice = int(magic_choice) - 1
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_spell_damage()
            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNOT enough MP!\n" + bcolors.ENDC)
                continue
            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg) + "HP" + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_terget(enemies)
                enemies[enemy].take_dmg(magic_dmg)
                print(
                    bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg) + " points of damage to " + enemies[
                        enemy].name + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(bcolors.OKBLUE + bcolors.BOLD + "\n" + enemies[enemy].name.replace(" ",
                                                                                             "") + " has died" + bcolors.ENDC)
                    del enemies[enemy]
                    if not enemies:
                        print(bcolors.OKGREEN + "\n\nYOU WIN!!!" + bcolors.ENDC)
                        running = False
                        break

        elif index == 2:
            player.choose_item()
            item_choice = input("Choose Item: ")
            if item_choice == 'b':
                continue
            item_choice = int(item_choice) - 1

            item = player.items[item_choice]
            if item["quantity"] > 0:
                player.items[item_choice]["quantity"] -= 1
            else:
                print(bcolors.FAIL + "\n" + "The quantity of " + item["item"].name + "is 0" + bcolors.ENDC)
                continue

            if item["item"].type == "potion":
                player.heal(item["item"].prop)
                print(bcolors.OKGREEN + "\n" + item["item"].name + " heals for " + str(
                    item["item"].prop) + " HP" + bcolors.ENDC)
            elif item["item"].type == "elixer":
                if item.name == "Elixer":
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + item["item"].name + " fully restores HP/MP" + bcolors.ENDC)
                elif item.name == "MegaElixer":
                    for i in players:
                        player.hp = player.maxhp
                        player.mp = player.maxmp
                        print(bcolors.OKGREEN + "\n" + item[
                            "item"].name + " fully restores HP/MP of the whole party" + bcolors.ENDC)

            elif item["item"].type == "attack":
                enemy = player.choose_terget(enemies)
                enemies[enemy].take_dmg(item["item"].prop)
                print(bcolors.FAIL + "\n" + item["item"].name + " deals " + str(
                    item["item"].prop) + " points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(bcolors.OKBLUE + bcolors.BOLD + "\n" + enemies[enemy].name.replace(" ",
                                                                                             "") + " has died" + bcolors.ENDC)
                    del enemies[enemy]
                    if not enemies:
                        print(bcolors.OKGREEN + "\n\nYOU WIN!!!" + bcolors.ENDC)
                        running = False
                        break

    if not running:
        break

    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        enemy_target = random.randrange(0, 4)

        if enemy.hp < 100 and enemy.mp > 10:
            spell = enemy.magic[3]
            cost = spell.cost
            magic_dmg = spell.generate_spell_damage()
            enemy.reduce_mp(cost)
            enemy.heal(magic_dmg)
            print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + " heals for " + str(
                magic_dmg) + "HP" + bcolors.ENDC)
            continue

        if enemy_choice == 0:
            enemy_dmg = enemy.generate_damage()
            print(bcolors.FAIL + bcolors.BOLD + "\n" + enemy.name.replace(" ", "") + " attacks " + players[
                enemy_target].name.replace(" ", "") + " for " + str(enemy_dmg) + " points of damage" + bcolors.ENDC)
            players[enemy_target].take_dmg(enemy_dmg)

            if players[enemy_target] == 0:
                print(bcolors.FAIL + bcolors.BOLD + "\n" + players[enemy_target].name.replace(" ",
                                                                                              "") + " has died" + bcolors.ENDC)
                del players[enemy_target]
                if not players:
                    print(bcolors.FAIL + "\n\nGAME OVER!!! ALL PLAYERS ARE DEAD!!! " + bcolors.ENDC)
                    running = False
                    continue

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            cost = spell.cost
            enemy.reduce_mp(cost)
            print(bcolors.OKBLUE + bcolors.BOLD + "\n" + enemy.name.replace(" ",
                                                                            "") + " choose magic " + spell.name + " and attacks " +
                  players[enemy_target].name.replace(" ", "") + " for " + str(
                magic_dmg) + " points of damage" + bcolors.ENDC)

        if players[enemy_target] == 0:
            print(bcolors.FAIL + bcolors.BOLD + "\n" + players[enemy_target].name.replace(" ",
                                                                                          "") + " has died" + bcolors.ENDC)
            del players[enemy_target]
            if not players:
                print(bcolors.FAIL + "\n\nGAME OVER!!! ALL PLAYERS ARE DEAD!!! " + bcolors.ENDC)
                running = False
                break
