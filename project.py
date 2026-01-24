# dungeon_rpg_mega_ultra_plus.py
import random, time
from dataclasses import dataclass, field, asdict
from typing import List, Dict

def slowprint(text, delay=0.010):
    for ch in str(text):
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def clamp(n, minn, maxn):
    return max(minn, min(n, maxn))

# ----------------- Artifacts -----------------
@dataclass
class Artifact:
    id: str
    name: str
    description: str
    rarity: str = "Common"
    damage_bonus: int = 0
    defense_bonus: int = 0
    hp_bonus: int = 0
    cooldown_reduction: float = 0.0

ARTIFACT_POOL = [
    Artifact(id="art_1", name="Ring of Might", description="Adds +5 damage", rarity="Common", damage_bonus=5),
    Artifact(id="art_2", name="Amulet of Fortitude", description="Adds +8 HP", rarity="Common", hp_bonus=8),
    Artifact(id="art_3", name="Boots of Haste", description="Reduces cooldowns 10%", rarity="Rare", cooldown_reduction=0.10),
    Artifact(id="art_4", name="Shield of Ages", description="Adds +3 defense", rarity="Rare", defense_bonus=3),
    Artifact(id="art_5", name="Crown of Kings", description="Adds +15 HP & +5 damage", rarity="Epic", hp_bonus=15, damage_bonus=5),
    Artifact(id="art_6", name="Blade of Time", description="Reduces ALL cooldowns by 25%", rarity="Epic", cooldown_reduction=0.25)
]

# ----------------- Player -----------------
@dataclass
class Player:
    name: str = "Hero"
    class_name: str = "Adventurer"
    level: int = 1
    xp: int = 0
    xp_to_next: int = 100
    hp: int = 100
    max_hp: int = 100
    base_damage: int = 10
    defense: int = 2
    gold: int = 0
    artifacts: List[Artifact] = field(default_factory=list)
    cooldown_timers: Dict[str,float] = field(default_factory=dict)
    cheat_flags: Dict[str,object] = field(default_factory=lambda: {
        "hehe": False, "haha": False, "hihi": False, "hoho": False, "huhu": False,
        "dodge_next": False, "next_attack_boost": 1.0
    })
    class_ability: str = ""
    skill_tree_maxed: bool = False
    abilities: Dict[str, Dict] = field(default_factory=dict)

    # ----------------- Stats -----------------
    def compute_damage(self):
        dmg = self.base_damage + sum(a.damage_bonus for a in self.artifacts)
        if self.class_name == "Berserker" and self.hp < self.max_hp/2:
            dmg = int(dmg*1.5)
        return dmg

    def compute_defense(self):
        return self.defense + sum(a.defense_bonus for a in self.artifacts)

    def compute_cooldown(self, move):
        base = self.cooldown_timers.get(move, 0.0)
        total_reduction = sum(a.cooldown_reduction for a in self.artifacts)
        if self.class_name == "Assassin":
            total_reduction += 0.15
        if self.cheat_flags.get("haha", False):
            return 0.0
        return max(0.0, base*(1-total_reduction))

    def heal(self, amount):
        if self.cheat_flags.get("hehe", False):
            self.hp = 9999
        else:
            self.hp = clamp(self.hp + amount, 0, self.max_hp)

    def level_up(self, times=1):
        for _ in range(times):
            self.level += 1
            self.max_hp += 10
            self.hp = self.max_hp
            self.base_damage += 2
            self.defense += 1
        if self.level >= 10:
            self.skill_tree_maxed = True

    # ----------------- Class Abilities -----------------
    def init_class_abilities(self):
        if self.class_name == "Warrior":
            self.abilities = {
                "Power Strike": {"cooldown": 3, "desc": "2x damage", "action": self.ability_power_strike},
                "Shield Bash": {"cooldown": 4, "desc": "Damage + stun", "action": self.ability_shield_bash}
            }
        elif self.class_name == "Mage":
            self.abilities = {
                "Fireball": {"cooldown": 3, "desc": "High magic damage", "action": self.ability_fireball},
                "Ice Barrier": {"cooldown": 5, "desc": "Gain shield", "action": self.ability_ice_barrier}
            }
        elif self.class_name == "Rogue":
            self.abilities = {
                "Backstab": {"cooldown": 2.5, "desc": "Double damage", "action": self.ability_backstab},
                "Evasion": {"cooldown": 4, "desc": "Dodge next attack", "action": self.ability_evasion}
            }
        elif self.class_name == "Berserker":
            self.abilities = {
                "Rage Strike": {"cooldown": 3, "desc": "Extra dmg when HP<50%", "action": self.ability_rage_strike},
                "Bloodlust": {"cooldown": 5, "desc": "Deal dmg & heal %", "action": self.ability_bloodlust}
            }
        elif self.class_name == "Assassin":
            self.abilities = {
                "Poison Blade": {"cooldown": 3, "desc": "Damage over time", "action": self.ability_poison_blade},
                "Shadow Step": {"cooldown": 4, "desc": "Avoid next attack", "action": self.ability_shadow_step}
            }
        for name in self.abilities:
            self.cooldown_timers.setdefault(name, 0.0)
        self.cooldown_timers.setdefault("heal", 0.0)

    # ----------------- Ability Actions -----------------
    def ability_power_strike(self, enemy):
        dmg = self.compute_damage()*2
        enemy['hp'] -= dmg
        slowprint(f"Power Strike hits {enemy['name']} for {dmg} damage!")

    def ability_shield_bash(self, enemy):
        dmg = self.compute_damage()+3
        enemy['hp'] -= dmg
        enemy['stunned'] = True
        slowprint(f"Shield Bash hits {enemy['name']} for {dmg} damage! Enemy stunned!")

    def ability_fireball(self, enemy):
        dmg = self.compute_damage()+8
        enemy['hp'] -= dmg
        slowprint(f"Fireball burns {enemy['name']} for {dmg} damage!")

    def ability_ice_barrier(self, enemy=None):
        shield = 20
        self.hp = 9999 if self.cheat_flags.get("hehe", False) else clamp(self.hp+shield,0,self.max_hp)
        slowprint(f"Ice Barrier restores {shield} HP!")

    def ability_backstab(self, enemy):
        dmg = int(self.compute_damage()*2.5)
        enemy['hp'] -= dmg
        slowprint(f"Backstab hits {enemy['name']} for {dmg} critical damage!")

    def ability_evasion(self, enemy=None):
        slowprint("Evasion activated! You dodge the next attack.")
        self.cheat_flags["dodge_next"] = True

    def ability_rage_strike(self, enemy):
        dmg = self.compute_damage()
        if self.hp < self.max_hp/2:
            dmg = int(dmg*1.5)
        enemy['hp'] -= dmg
        slowprint(f"Rage Strike hits {enemy['name']} for {dmg} damage!")

    def ability_bloodlust(self, enemy):
        dmg = self.compute_damage()
        heal_amt = int(dmg*0.3)
        enemy['hp'] -= dmg
        self.heal(heal_amt)
        slowprint(f"Bloodlust hits {enemy['name']} for {dmg} damage and heals {heal_amt} HP!")

    def ability_poison_blade(self, enemy):
        dmg = self.compute_damage()
        enemy['hp'] -= dmg
        enemy['poison'] = enemy.get('poison',0)+3
        slowprint(f"Poison Blade hits {enemy['name']} for {dmg} damage! Enemy poisoned for 3 turns!")

    def ability_shadow_step(self, enemy=None):
        slowprint("Shadow Step activated! You avoid next attack and next attack is stronger.")
        self.cheat_flags["dodge_next"] = True
        self.cheat_flags["next_attack_boost"] = 1.5

# ----------------- Cheats -----------------
def check_cheats(player, code):
    code = code.lower().strip()
    if code == "hehe":
        player.cheat_flags["hehe"] = not player.cheat_flags["hehe"]
        slowprint(f"CHEAT TOGGLE: Infinite Health {'ON' if player.cheat_flags['hehe'] else 'OFF'}")
        if player.cheat_flags["hehe"]:
            player.hp = 9999
    elif code == "haha":
        player.cheat_flags["haha"] = not player.cheat_flags["haha"]
        slowprint(f"CHEAT TOGGLE: No cooldown {'ON' if player.cheat_flags['haha'] else 'OFF'}")
        if player.cheat_flags["haha"]:
            # Reset all cooldowns immediately
            for key in player.cooldown_timers:
                player.cooldown_timers[key] = 0.0
    elif code == "hihi":
        player.cheat_flags["hihi"] = not player.cheat_flags["hihi"]
        slowprint(f"CHEAT TOGGLE: One-hit next enemy {'ON' if player.cheat_flags['hihi'] else 'OFF'}")
    elif code == "hoho":
        # Apply all class buffs x10
        player.base_damage *= 10
        player.defense *= 10
        player.max_hp *= 10
        player.hp = player.max_hp
        for a in player.artifacts:
            a.damage_bonus *= 10
            a.defense_bonus *= 10
            a.hp_bonus *= 10
            a.cooldown_reduction = min(0.9, a.cooldown_reduction*10)
        slowprint("CHEAT ACTIVATED: All class buffs x10!")
    elif code == "huhu":
        player.level_up(10)
        player.skill_tree_maxed = True
        slowprint("CHEAT ACTIVATED: Level +10!")
# ----------------- Loot -----------------
def roll_loot(is_boss=False):
    common_chance, rare_chance, epic_chance = (0.7,0.25,0.05)
    if is_boss:
        common_chance, rare_chance, epic_chance = (0.3,0.5,0.2)
    roll=random.random()
    if roll < common_chance:
        rarity="Common"
    elif roll < common_chance + rare_chance:
        rarity="Rare"
    else:
        rarity="Epic"
    gold = random.randint(15,30)*(2 if rarity=="Epic" else 1)
    potions = 1 if random.random()<0.5 else 0
    artifact = None
    avail = [a for a in ARTIFACT_POOL if a.rarity==rarity]
    if avail and random.random()<0.5:
        art = random.choice(avail)
        artifact = Artifact(**asdict(art))
    return gold, potions, artifact

# ----------------- Skill Tree -----------------
def allocate_skill_points(player):
    slowprint("\n-- Skill Tree --")
    slowprint("You have 1 skill point to allocate.")
    slowprint("1) Increase base damage (+2)")
    slowprint("2) Increase defense (+1)")
    slowprint("3) Increase max HP (+10)")
    slowprint("4) Reduce cooldowns (-5%)")
    choice=input("> ").strip()
    if choice=="1":
        player.base_damage+=2
        slowprint("Base damage increased!")
    elif choice=="2":
        player.defense+=1
        slowprint("Defense increased!")
    elif choice=="3":
        player.max_hp+=10
        player.hp=clamp(player.hp+10,0,player.max_hp)
        slowprint("Max HP increased!")
    elif choice=="4":
        for a in player.artifacts:
            a.cooldown_reduction+=0.05
        slowprint("Cooldown reduction increased by 5%!")

def gain_xp(player, amount):
    player.xp+=amount
    slowprint(f"You gain {amount} XP!")
    while player.xp>=player.xp_to_next:
        player.xp-=player.xp_to_next
        player.level_up()
        slowprint(f"LEVEL UP! You are now level {player.level}!")
        if not player.skill_tree_maxed:
            allocate_skill_points(player)

# ----------------- Shop -----------------
def shop_menu(player, potions):
    slowprint("Welcome to the shop! You can buy potions (5 gold each).")
    buy=input("Buy potion? (y/n) ").lower().strip()
    if buy=="y" and player.gold>=5:
        potions+=1
        player.gold-=5
        slowprint("Potion purchased!")
    else:
        slowprint("Maybe next time.")
    return potions

# ----------------- Battle -----------------
def battle(player, enemy, potions, battle_count):
    enemy = dict(enemy)
    slowprint(f"\nA wild {enemy['name']} appears!")
    is_boss = enemy.get("boss",False)
    enemy['stunned']=False
    enemy['poison']=enemy.get('poison',0)

    while enemy['hp']>0 and player.hp>0:
        slowprint(f"\n{player.name} ({player.class_name}) HP:{player.hp}/{player.max_hp} | Level:{player.level} XP:{player.xp}/{player.xp_to_next} | {enemy['name']} HP:{enemy['hp']}")
        slowprint("Actions: [1] Slash [2] Ability1 [3] Ability2 [4] Heal [5] Potion [6] Shop [7] Cheat Code")
        choice=input("> ").strip()

        if choice=="7":
            code=input("Enter cheat code: ").strip().lower()
            check_cheats(player, code)
            continue

        if player.cheat_flags.get("hihi", False):
            enemy['hp']=0
            slowprint(f"You instantly defeat {enemy['name']}!")
            player.cheat_flags["hihi"]=False
            break

        if choice=="1":
            dmg=player.compute_damage()
            if player.cheat_flags.get("next_attack_boost",1.0)>1.0:
                dmg=int(dmg*player.cheat_flags["next_attack_boost"])
                player.cheat_flags["next_attack_boost"]=1.0
            enemy['hp']-=dmg
            slowprint(f"You slash for {dmg} damage!")

        elif choice in ["2","3"]:
            idx=int(choice)-2
            ability_keys=list(player.abilities.keys())
            if idx<0 or idx>=len(ability_keys):
                slowprint("Invalid ability selection.")
            else:
                ability_name=ability_keys[idx]
                ready=player.cooldown_timers.get(ability_name,0)<=0 or player.cheat_flags.get("haha",False)
                if ready:
                    player.abilities[ability_name]['action'](enemy)
                    player.cooldown_timers[ability_name]=0.0 if player.cheat_flags.get("haha",False) else player.abilities[ability_name]['cooldown']
                else:
                    slowprint(f"{ability_name} is on cooldown!")

        elif choice=="4":
            if player.cooldown_timers.get("heal",0)<=0 or player.cheat_flags.get("haha",False):
                heal_amt=20
                player.heal(heal_amt)
                player.cooldown_timers["heal"]=0.0 if player.cheat_flags.get("haha",False) else 5
                slowprint(f"You heal for {heal_amt} HP!")
            else:
                slowprint("Heal is on cooldown!")

        elif choice=="5":
            if potions>0:
                player.heal(30)
                potions-=1
                slowprint("You drink a potion!")
            else:
                slowprint("No potions left!")

        elif choice=="6":
            potions=shop_menu(player,potions)

        if enemy['hp']<=0:
            break

        if enemy.get('stunned',False):
            slowprint(f"{enemy['name']} is stunned and misses!")
            enemy['stunned']=False
        else:
            dmg=enemy.get('atk',10)
            if is_boss:
                if enemy['name']=="Minotaur" and enemy['hp']<enemy['max_hp']/2:
                    dmg*=2
                    slowprint("Minotaur enraged! Double damage!")
                elif enemy['name']=="Necromancer" and enemy['hp']<enemy['max_hp']/2:
                    slowprint("Necromancer summons skeletons!")
                    sk_dmg=max(0,6-player.compute_defense())
                    if sk_dmg>0:
                        player.hp-=sk_dmg
                        slowprint(f"A summoned skeleton hits you for {sk_dmg} damage!")
                elif enemy['name']=="Dragon" and enemy['hp']<enemy['max_hp']/2 and random.random()<0.5:
                    slowprint("Dragon dodges part of the incoming attack!")
                    dmg=0
            if player.cheat_flags.get("dodge_next",False):
                slowprint("You dodge the attack!")
                player.cheat_flags["dodge_next"]=False
                dmg=0
            dmg=max(0,int(dmg-player.compute_defense()))
            player.hp-=dmg
            if dmg>0:
                slowprint(f"{enemy['name']} hits you for {dmg} damage!")

        if enemy.get('poison',0)>0:
            pdmg=5
            enemy['hp']-=pdmg
            enemy['poison']=max(0,enemy.get('poison',0)-1)
            slowprint(f"{enemy['name']} takes {pdmg} poison damage!")

        for key in list(player.cooldown_timers.keys()):
            if player.cooldown_timers.get(key,0)>0:
                player.cooldown_timers[key]=max(0.0,player.cooldown_timers[key]-1.0)

    if player.hp>0:
        slowprint(f"You defeated {enemy['name']}!")
        gold,p_count,art=roll_loot(is_boss)
        player.gold+=gold
        potions+=p_count
        if art:
            player.artifacts.append(art)
            slowprint(f"You found artifact: {art.name} ({art.rarity})!")
        slowprint(f"Loot: {gold} gold, {p_count} potion(s)")
        gain_xp(player,50 if is_boss else 20)
    return potions

# ----------------- Character Creation -----------------
def character_creation():
    slowprint("Welcome to Dungeon RPG!")
    name=input("Enter your hero's name: ").strip() or "Hero"
    slowprint("Choose class:")
    slowprint("1) Warrior (+20 HP, +2 dmg)")
    slowprint("2) Mage (+10 dmg, -5 HP)")
    slowprint("3) Rogue (+15% cooldown reduction)")
    slowprint("4) Berserker (+50% dmg when HP<50%)")
    slowprint("5) Assassin (+15% cooldown reduction)")
    choice=input("> ").strip()
    player=Player(name=name)
    if choice=="1":
        player.class_name="Warrior"
        player.max_hp+=20
        player.hp=player.max_hp
        player.base_damage+=2
        player.class_ability="Strong & durable fighter"
    elif choice=="2":
        player.class_name="Mage"
        player.base_damage+=10
        player.max_hp=max(1,player.max_hp-5)
        player.hp=player.max_hp
        player.class_ability="Powerful magic attacks"
    elif choice=="3":
        player.class_name="Rogue"
        player.artifacts.append(Artifact(id="start_rogue",name="Quick Gloves",description="Reduces cooldowns 15%",cooldown_reduction=0.15))
        player.class_ability="Fast and nimble"
    elif choice=="4":
        player.class_name="Berserker"
        player.max_hp+=10
        player.hp=player.max_hp
        player.base_damage+=3
        player.class_ability="Deals more damage at low HP"
    elif choice=="5":
        player.class_name="Assassin"
        player.artifacts.append(Artifact(id="start_assassin",name="Silent Dagger",description="Reduces cooldowns 15%",cooldown_reduction=0.15))
        player.class_ability="High cooldown reduction"
    player.init_class_abilities()
    return player

# ----------------- Main Game -----------------
def main():
    player=character_creation()
    potions=1
    battle_count=0
    bosses=[
        {"name":"Minotaur","hp":150,"max_hp":150,"atk":20,"boss":True,"location":"Labyrinth"},
        {"name":"Necromancer","hp":120,"max_hp":120,"atk":15,"boss":True,"location":"Shadow Crypt"},
        {"name":"Dragon","hp":200,"max_hp":200,"atk":25,"boss":True,"location":"Golden Lair"}
    ]

    while player.hp>0:
        battle_count+=1
        if battle_count%10==0:
            enemy_template=random.choice(bosses)
            enemy=dict(enemy_template)
        else:
            enemy={"name":"Goblin","hp":50,"max_hp":50,"atk":8}
        potions=battle(player,enemy,potions,battle_count)
        if player.hp<=0:
            slowprint("You died! Game Over.")
            break

if __name__=="__main__":
    main()
