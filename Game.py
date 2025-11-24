import random
from Char import *
from colorama import Fore, Style, init # type: ignore

init(autoreset=True)

def colored_name(name):
    return f"{Fore.MAGENTA}{name}{Style.RESET_ALL}"

def colored_health(value):
    return f"{Fore.GREEN}{value}{Style.RESET_ALL}"

def colored_damage(value):
    return f"{Fore.RED}{value}{Style.RESET_ALL}"

def colored_charged_damage(value):
    return f"{Fore.YELLOW}{value}{Style.RESET_ALL}"

def colored_mana(value):
    return f"{Fore.BLUE}{value}{Style.RESET_ALL}"

def colored_skill(name):
    return f"{Fore.YELLOW}{name}{Style.RESET_ALL}"

def colored_defense(value):
    return f"{Fore.CYAN}{value}{Style.RESET_ALL}"

def colored_status_effect(name):
    return f"{Fore.YELLOW}{name}{Style.RESET_ALL}"

class Battle:
    def __init__(self, party, enemy):
        self.party = party
        self.enemy = enemy
        self.turn = 0
    
    def buff_check(self, character, status_name):
        if status_name in character.status:
            return True
        return False

    def update_status(self):
        # Update enemy status
        for status_name, turns in list(self.enemy.status.items()):
            if turns == "infinite":
                continue
            if turns > 0:
                self.enemy.status[status_name] -= 1
            elif turns <= 0:
                del self.enemy.status[status_name]
                print(f"{self.enemy.name}'s {status_name} has worn off.")
                if status_name == "Immense Gaze":
                    self.enemy.defense /= 0.75
        # Party status update
        for character in self.party:
            for status_name, turns in list(character.status.items()):
                if turns == "infinite":
                    continue
                if turns > 0:
                    character.status[status_name] -= 1
                elif turns <= 0:
                    del character.status[status_name]
                    print(f"{character.name}'s {status_name} has worn off.")
                    if status_name == "You can do it!":
                        character.attack /= 1.25
                    elif status_name == "Immense Gaze":
                        character.defense /= 0.75
            if character.defending:
                character.defense /= 1.5
                character.defending = False
    
    def status_effect(self, character, status_name):

        # Kiko's buffs/debuffs
        if status_name == "You can do it!":
            if self.buff_check(character, status_name):
                print(f"{colored_name(character.name)}'s attack buff is renewed.")
            else:
                character.attack *= 1.25
                print(f"{colored_name(character.name)}'s attack increased by 25% for 3 turns.")
            
            character.status[status_name] = 3
        elif status_name == "Kiko's Blessing":
            heal_amount = round(character.health * 0.2)
            character.health += heal_amount
            print(f"{colored_name(character.name)} healed for {colored_health(heal_amount)} health.")

        # Ampy's buffs/debuffs
        elif status_name == "A Demon's Instinct":
            if not self.buff_check(character, status_name):
                if character.name == "Ampy":
                    print(f"{colored_name(character.name)} is now charged and will deal 2.5x damage on the next attack.")
                    character.charged = 2.5
                    character.status[status_name] = "infinite"
                else:
                    print(f"Ampy rejects that thought and redirects the focus back to himself")
            
            else:
                print(f"{colored_name(character.name)} is already charged..? No need to do it again next time.")
            
        elif status_name == "Immense Gaze":
            if self.buff_check(character, status_name):
                print(f"{colored_name(character.name)}'s defense debuff is renewed.")
            else:
                character.defense *= 0.75
                print(f"{colored_name(character.name)}'s defense reduced by 25% for 3 turns.")
                character.status[status_name] = 3

    def perform_skill(self, character, skill_num, enemy):
        skill = character.skills[skill_num]
        print(skill.isHeal)
        character.mana -= skill.cost

        if skill.isHeal:
            print(f"{colored_name(character.name)} uses {colored_skill(skill.name)} to heal all allies.")
            for ally in self.party:
                self.status_effect(ally, skill.name)

        elif skill.isBuff:
            if skill.single:
                while True:
                    i = 0
                    for ally in self.party:
                        i += 1
                        print(f'({i}) {colored_name(ally.name)}')
                    try:
                        target = int(input("Choose a character to buff: ")) - 1
                        if target < 0 or target >= len(self.party):
                            print("Invalid choice. Please try again.")
                            continue
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue
                    
                    else:
                        target_character = self.party[target]
                        print(f"{colored_name(character.name)} uses {colored_skill(skill.name)} to buff {colored_name(target_character.name)}.")
                        self.status_effect(target_character, skill.name)
                        break
            else:
                print(f"{colored_name(character.name)} uses {colored_skill(skill.name)} to buff all allies.")
                for ally in self.party:
                    self.status_effect(ally, skill.name)
        
        elif skill.isDebuff:
            target_character = self.enemy
            print(f"{colored_name(character.name)} uses {colored_skill(skill.name)} to debuff {colored_name(target_character.name)}.")
            self.status_effect(target_character, skill.name)

        else:
            print(f"{colored_name(character.name)} uses {colored_skill(skill.name)} on {colored_name(enemy.name)}.")
            damage = round((character.attack - enemy.defense) * round(random.uniform(1, 1.6), 1) * skill.points)
            if character.charged > 1:
                damage *= character.charged
                character.charged = 1
                del character.status["A Demon's Instinct"]
                print(f"{colored_name(character.name)} is no longer charged.")
                
            enemy.health -= max(damage, 0)
            if character.charged > 1:
                print(f"{colored_name(enemy.name)} takes {colored_charged_damage(max(damage, 0))} damage. Remaining health: {colored_health(enemy.health)}")
            else:
                print(f"{colored_name(enemy.name)} takes {colored_damage(max(damage, 0))} damage. Remaining health: {colored_health(enemy.health)}")

    def game_loop(self):
        while self.enemy.health > 0:
            self.update_status()
            # Player's turn
            for character in self.party:
                if character.health <= 0:
                    print(f"{colored_name(character.name)} is defeated and cannot act.")
                    continue
                
                while True:
                    print(f"\n{colored_name(character.name)}'s turn:")
                    action = input(f"What do you wanna do?\n(a) Basic Attack\n(b) Skill\n(c) Defend\n(d) Status Check\n(e) Enemy Check\n").strip().lower()
                    if action == 'a':
                        damage = round((character.attack - self.enemy.defense) * round(random.uniform(1, 1.6), 1))
                        if character.charged > 1:
                            damage *= character.charged
                            character.charged = 1
                            del character.status["A Demon's Instinct"]
                            print(f"{colored_name(character.name)} is no longer charged.")
                            self.enemy.health -= max(damage, 0)
                            print(f"{colored_name(character.name)} attacks {colored_name(self.enemy.name)} for {colored_charged_damage(max(damage, 0))} damage. Enemy health: {colored_health(self.enemy.health)}")
                        else:
                            self.enemy.health -= max(damage, 0) 
                            print(f"{colored_name(character.name)} attacks {colored_name(self.enemy.name)} for {colored_damage(max(damage, 0))} damage. Enemy health: {colored_health(self.enemy.health)}")

                    elif action == 'b':
                        print("Available skills:")
                        i = 0
                        for skill in character.skills:
                            i += 1
                            print(f"({i}) {colored_skill(skill.name)} - {skill.description} (Cost: {colored_mana(skill.cost)} mana)")
                        try:
                            skill_choice = int(input("Choose a skill by number: ")) - 1
                            if skill_choice < 0 or skill_choice >= len(character.skills):
                                print("Invalid skill choice.")
                                continue
                            else:
                                if character.mana < character.skills[skill_choice].cost:
                                    print(f"{colored_name(character.name)} does not have enough mana to use {colored_skill(character.skills[skill_choice].name)}.")
                                    continue
                                self.perform_skill(character, skill_choice, self.enemy)
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                            continue
                    elif action == 'c':
                        character.defending = True
                        character.defense *= 1.5
                        print(f"{colored_name(character.name)} is defending this turn.")
                    
                    elif action == 'd':
                        print(f"{colored_name(character.name)}'s Status:")
                        print(f"Health: {colored_health(character.health)}/{colored_health(character.base_health)}")
                        print(f"Mana: {colored_mana(character.mana)}")
                        print(f"Attack: {colored_damage(character.attack)}")
                        print(f"Defense: {colored_defense(character.defense)}")
                        print(f"Active Status Effect(s):")
                        
                        if character.status:
                            for status_name, turns in character.status.items():
                                if turns == "infinite":
                                    print(f"{colored_status_effect(status_name)} is active indefinitely until a damaging skill is performed.")
                                else:
                                    print(f"{colored_status_effect(status_name)} will last for {turns} turns.")
                        else:
                            print(f"{colored_name(character.name)} has no active buffs.")
                        continue
                    
                    elif action == 'e':
                        print(f"Enemy's Status:")
                        print(f"Health: {colored_health(self.enemy.health)}/{colored_health(self.enemy.base_health)}")
                        print(f"Attack: {colored_damage(self.enemy.attack)}")
                        print(f"Defense: {colored_defense(self.enemy.defense)}")
                        print(f"Active Status Effect(s):")
                        
                        if self.enemy.status:
                            for status_name, turns in self.enemy.status.items():
                                if turns == "infinite":
                                    print(f"{colored_status_effect(status_name)} is active indefinitely.")
                                else:
                                    print(f"{colored_status_effect(status_name)} will last for {turns} turns.")
                        else:
                            print("No active debuffs/buffs on the enemy.")
                        continue
                    else:
                        print("Invalid action. Please choose again.")
                        continue
                    if self.enemy.health <= 0:
                        print(f"{colored_name(self.enemy.name)} has been defeated!")
                        return
                    break
            # Enemy's turn
            print("\nEnemy's turn:")
            if self.enemy.health > 0:
                enemy_action = random.choice(self.enemy.skills)
                if enemy_action.isDebuff:
                    print(f"{colored_name(self.enemy.name)} uses {colored_skill(enemy_action.name)} on {colored_name(random.choice(self.party).name)}.")
                    self.status_effect(random.choice(self.party), enemy_action.name)
                else:
                    target_character = random.choice(self.party)
                    damage = round((self.enemy.attack - target_character.defense) * round(random.uniform(1, 1.6), 1))
                    target_character.health -= max(damage, 0)
                    print(f"{colored_name(self.enemy.name)} attacks {colored_name(target_character.name)} for {colored_damage(max(damage, 0))} damage. {colored_name(target_character.name)}'s health: {colored_health(target_character.health)}")
                    if target_character.health <= 0:
                        print(f"{colored_name(target_character.name)} has been defeated.")
                        self.party.remove(target_character)
                        if not self.party:
                            print("All party members have been defeated. Game over.")
                            return
def shop():
    pass

def Char_info():
    pass

def explore():
    pass

def online():
    pass

def idle():
    while True:
        choice = input("What do you wanna do?\n(a) Go to shop\n(b) Characters\n(c) Fight Enemies\n(d) Explore the Cities\n(e) Online Section\n==> ")
        if choice == 'a':
            shop()
        elif choice == 'b':
            Char_info()
        elif choice == 'c':
            Battle()
        elif choice == 'd':
            explore()
        elif choice == 'e':
            online()
        else:
            print("Please choose correctly.\n")
    
chosen_char = ["Kiko", "Ampy"]
char_dict = {}

# with open(f'characters.csv', mode='r') as char_file:
#     chars = csv.reader(char_file, skipinitialspace=True)
#     i = 97
#     next(chars)
#     for char_name in chars:
#         char_dict.update({chr(i): char_name[0]})
#         i += 1

# def char_pick(option):
#     char_name = char_dict.get(option)
#     if char_name == None:
#         print("Please choose correctly\n")
#         return
    
#     init_char([char_name], 1)
#     confirm = input("Do you want to pick this character?  (Yes/No)\n")
#     if confirm == "yes" or confirm == 'Yes':
#         if char_name in chosen_char:
#             print("You already chose this character!\n")
#         else:
#             chosen_char.append(char_name)
#     else:
#         pass
    
# while True:
#     print(f"Current chosen characters: {', '.join(chosen_char)}")
#     print("Choose your characters (type 'done' if finished choosing):")
#     for key, value in char_dict.items():
#         print(f'({key}) {value}')
#     choice = input()
#     if choice == 'done' and chosen_char:
#         break
#     else:
#         print("You haven't chosen any character\n")
#     char_pick(choice)
        
Battle([*init_char([*chosen_char], 0)], Enemy()).game_loop()