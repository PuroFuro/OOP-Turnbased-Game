class Kiko(Characters):
    def __init__(self):
        name, level, weapon, base_attack, base_defense, base_health, mana, description = initialize_char("Kiko")
        skills = initialize_skills("Kiko")
        super().__init__(name, level, weapon, base_attack, base_defense, base_health, mana, description, skills)

class Ampy(Characters):
    def __init__(self):
        name, level, weapon, base_attack, base_defense, base_health, mana, description = initialize_char("Ampy")
        skills = initialize_skills("Ampy")
        super().__init__(name, level, weapon, base_attack, base_defense, base_health, mana, description, skills)

class Cyrus(Characters):
    def __init__(self):
        name, level, weapon, base_attack, base_defense, base_health, mana, description = initialize_char("Cyrus")
        skills = initialize_skills("Cyrus")
        super().__init__(name, level, weapon, base_attack, base_defense, base_health, mana, description, skills)

class Rhats(Characters):
    def __init__(self):
        name, level, weapon, base_attack, base_defense, base_health, mana, description = initialize_char("Rhats")
        skills = initialize_skills("Rhats")
        super().__init__(name, level, weapon, base_attack, base_defense, base_health, mana, description, skills)