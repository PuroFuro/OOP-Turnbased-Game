import random
import csv

class Characters:
    def __init__(self, name, level, weapon, base_attack, base_defense, base_health, mana, description, skills):
        self.name = name
        self.level = level
        self.weapon = weapon
        self.base_attack = base_attack
        self.base_defense = base_defense
        self.base_health = base_health
        self.health = base_health
        self.attack = base_attack
        self.defense = base_defense
        self.mana = mana
        self.skills = skills
        self.description = description
        self.status = {} #  python dictionary with : to store turns
        self.defending = False
        self.charged = 1

class Skill:
    def __init__(self, name, points, cost, description, level_req, isBuff, isDebuff, isHeal, single):
        self.name = name
        self.points = points
        self.cost = cost
        self.description = description
        self.level_req = level_req
        self.isBuff = isBuff
        self.isDebuff = isDebuff
        self.isHeal = isHeal
        self.single = single

def init_char(names, info):
    i = 0
    skills = []
    chars = []
    for name in names:
        with open(f"./skills/{name}.csv", mode='r') as skill_file:
            skill_list = csv.reader(skill_file, skipinitialspace=True)
            next(skill_list)
            for skill in skill_list:
                if info:
                    skills.append([skill[1], skill[4]])
                else:
                    skills.append(Skill(skill[1], float(skill[2]), int(skill[3]), skill[4], int(skill[5]), eval(skill[6]), eval(skill[7]), eval(skill[8]), eval(skill[9])))
                
        with open("characters.csv", mode='r') as char:
            reader = csv.reader(char, skipinitialspace=True)
            next(reader) 
            for char_info in reader:
                if name == char_info[0] and info:
                    x=' '
                    print(f'Name: {char_info[0]}{x*5}Attack: {char_info[3]}{x*5}Defense: {char_info[4]}{x*5}Health: {char_info[5]}{x*5}Mana: {char_info[6]}\nDescription:\n  {char_info[7]}\n\nSkills:')
                    for skill in skills:
                        print('  ' + '- ' + ', '.join(map(str,skill)))
                elif name == char_info[0] and not info:
                    chars.append(Characters(char_info[0], int(char_info[1]), char_info[2], int(char_info[3]), int(char_info[4]), int(char_info[5]), int(char_info[6]), char_info[7], skills[:]))
        del skills[:]
    return chars
                
class Enemy(Characters):
    def __init__(self):
        health = 10000 #random.randint(500, 1000)
        attack = random.randint(50, 150)
        defense = random.randint(10, 20)
        skills = [
            Skill("Normal Attack", random.randint(10, 30), 0, "A basic attack that deals moderate damage.", 1, False, False, False, True),
        ]
        super().__init__("Enemy", "1", "None", attack, defense, health, "an ordinary enemy", "A random enemy with varying stats and a basic attack skill.", skills)