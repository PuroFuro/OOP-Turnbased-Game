import csv
def init_char():
    with open("characters.csv", mode='r') as char:
        reader = csv.reader(char, skipinitialspace=True)
        next(reader) 
        i = 0
        for row in reader:
            if row[0] == "Kiko":
                return row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]

name, level, weapon, base_attack, base_defense, base_health, mana, description = init_char()
def initialize_skills():
    with open(f"./skills/Kiko.csv", mode='r') as skill_file:
        skill_list = csv.reader(skill_file, skipinitialspace=True)
        next(skill_list)
        skills = []
        for skill in skill_list:
            skills.append([skill[1], float(skill[2]), int(skill[3]), skill[4], int(skill[5]), bool(skill[6]), bool(skill[7]), bool(skill[8]), bool(skill[9])]) 
        return skills

skills = initialize_skills()
print(skills)