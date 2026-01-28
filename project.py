import random, time, json, os
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from enum import Enum

def slowprint(text, delay=0.005):
    for ch in str(text):
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def clamp(n, minn, maxn):
    return max(minn, min(n, maxn))

class Element(Enum):
    PHYSICAL = "Physical"
    FIRE = "Fire"
    ICE = "Ice"
    LIGHTNING = "Lightning"
    DARK = "Dark"
    HOLY = "Holy"
    POISON = "Poison"
    WIND = "Wind"

class WeaponType(Enum):
    SWORD = "Sword"
    AXE = "Axe"
    BOW = "Bow"
    STAFF = "Staff"
    DAGGER = "Dagger"
    SPEAR = "Spear"
    HAMMER = "Hammer"
    SCYTHE = "Scythe"

class Weather(Enum):
    CLEAR = "Clear"
    RAIN = "Rain"
    STORM = "Storm"
    SNOW = "Snow"
    FOG = "Fog"
    HEAT = "Heat"

class Stance(Enum):
    BALANCED = "Balanced"
    OFFENSIVE = "Offensive"
    DEFENSIVE = "Defensive"
    COUNTER = "Counter"


@dataclass
class Companion:
    name: str
    class_type: str
    level: int = 1
    hp: int = 80
    max_hp: int = 80
    damage: int = 8
    defense: int = 2
    special_ability: str = ""
    loyalty: int = 50
    ai_behavior: str = "balanced"

@dataclass
class Pet:
    name: str
    species: str
    level: int = 1
    hp: int = 50
    max_hp: int = 50
    damage: int = 5
    bonus_type: str = "damage"
    bonus_amount: int = 3
    evolution_stage: int = 1
    xp: int = 0

@dataclass
class Soul:
    enemy_type: str
    power: int
    element: Element
    special_effect: str

@dataclass
class Reputation:
    faction: str
    level: int = 0
    rank: str = "Neutral"

@dataclass
class Weapon:
    name: str
    weapon_type: WeaponType
    damage: int
    element: Element = Element.PHYSICAL
    crit_chance: float = 0.05
    description: str = ""
    rarity: str = "Common"
    enchantment: Optional[str] = None
    enchant_power: int = 0
    is_legendary: bool = False
    legendary_effect: str = ""

@dataclass
class Armor:
    name: str
    slot: str
    defense: int
    hp_bonus: int = 0
    resistance: Optional[Element] = None
    description: str = ""
    rarity: str = "Common"
    enchantment: Optional[str] = None

@dataclass
class Consumable:
    name: str
    effect_type: str
    power: int
    description: str
    duration: int = 0

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
    element: Optional[Element] = None

@dataclass
class Material:
    name: str
    description: str
    rarity: str = "Common"

@dataclass
class Quest:
    id: str
    name: str
    description: str
    objective_type: str
    objective_target: str
    objective_count: int
    current_count: int = 0
    reward_gold: int = 0
    reward_xp: int = 0
    reward_item: Optional[str] = None
    completed: bool = False

@dataclass
class Achievement:
    id: str
    name: str
    description: str
    requirement_type: str
    requirement_value: int
    unlocked: bool = False
    reward: str = ""

@dataclass
class Bounty:
    target: str
    reward: int
    difficulty: str
    completed: bool = False

LEGENDARY_WEAPONS = {
    "Excalibur": Weapon("Excalibur", WeaponType.SWORD, 50, Element.HOLY, 0.25,
                       "The legendary blade of kings", "Legendary", None, 0, True,
                       "Heals 10% max HP on kill"),
    "Mjolnir": Weapon("Mjolnir", WeaponType.HAMMER, 55, Element.LIGHTNING, 0.20,
                     "The hammer of thunder", "Legendary", None, 0, True,
                     "Stuns all enemies for 1 turn"),
    "Frostmourne": Weapon("Frostmourne", WeaponType.SWORD, 60, Element.ICE, 0.30,
                         "The cursed runeblade", "Legendary", None, 0, True,
                         "Steals 20% damage as HP"),
    "Death's Scythe": Weapon("Death's Scythe", WeaponType.SCYTHE, 65, Element.DARK, 0.35,
                            "The reaper's tool", "Legendary", None, 0, True,
                            "15% instant kill chance"),
}

WEAPONS = {
    "Rusty Sword": Weapon("Rusty Sword", WeaponType.SWORD, 5, Element.PHYSICAL, 0.05, "A weathered blade", "Common"),
    "Iron Sword": Weapon("Iron Sword", WeaponType.SWORD, 12, Element.PHYSICAL, 0.08, "Standard iron blade", "Common"),
    "Steel Axe": Weapon("Steel Axe", WeaponType.AXE, 15, Element.PHYSICAL, 0.10, "Heavy chopping weapon", "Common"),
    "Hunting Bow": Weapon("Hunting Bow", WeaponType.BOW, 10, Element.PHYSICAL, 0.15, "Precise ranged weapon", "Common"),
    "Oak Staff": Weapon("Oak Staff", WeaponType.STAFF, 8, Element.PHYSICAL, 0.05, "Basic magic staff", "Common"),
    "Iron Dagger": Weapon("Iron Dagger", WeaponType.DAGGER, 9, Element.PHYSICAL, 0.20, "Quick strikes", "Common"),
    "Flaming Blade": Weapon("Flaming Blade", WeaponType.SWORD, 20, Element.FIRE, 0.12, "Engulfed in flames", "Rare"),
    "Frostbite": Weapon("Frostbite", WeaponType.SWORD, 22, Element.ICE, 0.10, "Freezes enemies", "Rare"),
    "Thunderstrike": Weapon("Thunderstrike", WeaponType.AXE, 25, Element.LIGHTNING, 0.15, "Crackling with energy", "Rare"),
    "Shadow Dagger": Weapon("Shadow Dagger", WeaponType.DAGGER, 18, Element.DARK, 0.25, "Strikes from shadows", "Rare"),
    "Holy Spear": Weapon("Holy Spear", WeaponType.SPEAR, 24, Element.HOLY, 0.12, "Blessed weapon", "Rare"),
    "War Hammer": Weapon("War Hammer", WeaponType.HAMMER, 28, Element.PHYSICAL, 0.08, "Crushes armor", "Rare"),
    "Dragon Slayer": Weapon("Dragon Slayer", WeaponType.SWORD, 35, Element.FIRE, 0.18, "Forged from dragon scales", "Epic"),
    "Void Scythe": Weapon("Void Scythe", WeaponType.SCYTHE, 32, Element.DARK, 0.22, "Harvests souls", "Epic"),
}

ARMOR_SETS = {
    "Leather Cap": Armor("Leather Cap", "head", 2, 5, None, "Basic head protection", "Common"),
    "Iron Helmet": Armor("Iron Helmet", "head", 5, 10, None, "Sturdy metal helm", "Common"),
    "Dragon Helm": Armor("Dragon Helm", "head", 12, 25, Element.FIRE, "Resists fire damage", "Epic"),
    "Leather Tunic": Armor("Leather Tunic", "chest", 3, 10, None, "Light chest armor", "Common"),
    "Iron Chestplate": Armor("Iron Chestplate", "chest", 8, 20, None, "Heavy protection", "Common"),
    "Frost Mail": Armor("Frost Mail", "chest", 15, 30, Element.ICE, "Resists ice damage", "Rare"),
    "Leather Pants": Armor("Leather Pants", "legs", 2, 5, None, "Basic leg protection", "Common"),
    "Iron Greaves": Armor("Iron Greaves", "legs", 6, 15, None, "Metal leg armor", "Common"),
    "Shadow Leggings": Armor("Shadow Leggings", "legs", 10, 20, Element.DARK, "Resists dark magic", "Rare"),
    "Leather Boots": Armor("Leather Boots", "boots", 1, 5, None, "Basic footwear", "Common"),
    "Iron Boots": Armor("Iron Boots", "boots", 4, 10, None, "Heavy metal boots", "Common"),
    "Lightning Treads": Armor("Lightning Treads", "boots", 8, 15, Element.LIGHTNING, "Swift as lightning", "Rare"),
}

CONSUMABLES = {
    "Health Potion": Consumable("Health Potion", "heal", 30, "Restores 30 HP"),
    "Super Potion": Consumable("Super Potion", "heal", 80, "Restores 80 HP"),
    "Max Potion": Consumable("Max Potion", "heal", 9999, "Fully restores HP"),
    "Strength Elixir": Consumable("Strength Elixir", "buff_damage", 10, "Increases damage by 10 for 3 turns", 3),
    "Defense Tonic": Consumable("Defense Tonic", "buff_defense", 5, "Increases defense by 5 for 3 turns", 3),
    "Speed Boost": Consumable("Speed Boost", "buff_speed", 1, "Reduces all cooldowns for 3 turns", 3),
    "Phoenix Down": Consumable("Phoenix Down", "revive", 50, "Revives with 50% HP"),
}

MATERIALS = {
    "Iron Ore": Material("Iron Ore", "Common metal ore", "Common"),
    "Dragon Scale": Material("Dragon Scale", "Rare and powerful", "Epic"),
    "Frost Crystal": Material("Frost Crystal", "Contains ice magic", "Rare"),
    "Lightning Shard": Material("Lightning Shard", "Crackling with energy", "Rare"),
    "Dark Essence": Material("Dark Essence", "Mysterious dark power", "Epic"),
    "Holy Water": Material("Holy Water", "Blessed by clerics", "Rare"),
    "Soul Fragment": Material("Soul Fragment", "Essence of defeated foes", "Rare"),
    "Enchant Scroll": Material("Enchant Scroll", "Magical enhancement", "Rare"),
}

ENCHANTMENTS = {
    "Fire": {"damage": 5, "element": Element.FIRE},
    "Ice": {"damage": 5, "element": Element.ICE},
    "Lightning": {"damage": 7, "element": Element.LIGHTNING},
    "Sharpness": {"damage": 10, "element": None},
    "Fortify": {"defense": 5, "hp": 20},
    "Lifesteal": {"lifesteal": 0.15},
}

COMPANIONS_POOL = [
    Companion("Sir Reginald", "Knight", 1, 100, 100, 12, 5, "Shield Wall", 50, "defensive"),
    Companion("Aria", "Archer", 1, 70, 70, 15, 2, "Rapid Shot", 50, "aggressive"),
    Companion("Gandor", "Mage", 1, 60, 60, 18, 1, "Fireball", 50, "balanced"),
    Companion("Shadow", "Rogue", 1, 75, 75, 14, 3, "Backstab", 50, "aggressive"),
]

PETS_POOL = [
    Pet("Wolf Pup", "Wolf", 1, 50, 50, 5, "damage", 3, 1, 0),
    Pet("Fire Fox", "Fox", 1, 40, 40, 7, "damage", 5, 1, 0),
    Pet("Healing Sprite", "Sprite", 1, 30, 30, 2, "healing", 5, 1, 0),
    Pet("Lucky Cat", "Cat", 1, 35, 35, 3, "luck", 10, 1, 0),
]

@dataclass
class Player:
    name: str = "Hero"
    class_name: str = "Adventurer"
    secondary_class: Optional[str] = None
    level: int = 1
    prestige_level: int = 0
    xp: int = 0
    xp_to_next: int = 100
    hp: int = 100
    max_hp: int = 100
    base_damage: int = 10
    defense: int = 2
    gold: int = 0
    skill_points: int = 0
    talent_points: int = 0

    weapon: Optional[Weapon] = None
    equipped_armor: Dict[str, Armor] = field(default_factory=dict)
    inventory_weapons: List[Weapon] = field(default_factory=list)
    inventory_armor: List[Armor] = field(default_factory=list)
    consumables: Dict[str, int] = field(default_factory=dict)
    materials: Dict[str, int] = field(default_factory=dict)
    artifacts: List[Artifact] = field(default_factory=list)

    companions: List[Companion] = field(default_factory=list)
    active_companions: List[Companion] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)
    active_pet: Optional[Pet] = None

    cooldown_timers: Dict[str,float] = field(default_factory=dict)
    abilities: Dict[str, Dict] = field(default_factory=dict)
    talent_abilities: Dict[str, Dict] = field(default_factory=dict)
    ultimate_charge: int = 0
    ultimate_max: int = 100
    stance: Stance = Stance.BALANCED
    combo_count: int = 0
    last_action: str = ""

    class_ability: str = ""
    skill_tree_maxed: bool = False
    skill_branches: Dict[str, int] = field(default_factory=dict)
    evolution_stage: int = 1

    souls: List[Soul] = field(default_factory=list)
    reputation: Dict[str, Reputation] = field(default_factory=dict)
    active_quests: List[Quest] = field(default_factory=list)
    completed_quests: List[str] = field(default_factory=list)
    achievements: List[Achievement] = field(default_factory=list)
    bounties: List[Bounty] = field(default_factory=list)

    kills: Dict[str, int] = field(default_factory=dict)
    total_damage_dealt: int = 0
    critical_hits: int = 0
    bosses_defeated: int = 0
    perfect_parries: int = 0
    sacrifices_made: int = 0

    active_buffs: Dict[str, int] = field(default_factory=dict)

    cheat_flags: Dict[str,object] = field(default_factory=lambda: {
        "hehe": False, "haha": False, "hihi": False, "hoho": False, "huhu": False,
        "013113": False, "6767": False,
        "dodge_next": False, "next_attack_boost": 1.0
    })

    def compute_damage(self):
        dmg = self.base_damage

        if self.weapon:
            dmg += self.weapon.damage
            if self.weapon.enchantment:
                dmg += ENCHANTMENTS.get(self.weapon.enchantment, {}).get("damage", 0)

        dmg += sum(a.damage_bonus for a in self.artifacts)
        if self.active_pet and self.active_pet.bonus_type == "damage":
            dmg += self.active_pet.bonus_amount

        if self.class_name == "Berserker" and self.hp < self.compute_max_hp()/2:
            dmg = int(dmg*1.5)

        if self.stance == Stance.OFFENSIVE:
            dmg = int(dmg * 1.3)
        elif self.stance == Stance.DEFENSIVE:
            dmg = int(dmg * 0.7)

        if "damage_buff" in self.active_buffs:
            dmg += 10

        dmg += self.prestige_level * 2

        return dmg

    def compute_defense(self):
        defense = self.defense

        for armor in self.equipped_armor.values():
            defense += armor.defense
            if armor.enchantment:
                defense += ENCHANTMENTS.get(armor.enchantment, {}).get("defense", 0)

        defense += sum(a.defense_bonus for a in self.artifacts)

        if self.active_pet and self.active_pet.bonus_type == "defense":
            defense += self.active_pet.bonus_amount

        if self.stance == Stance.DEFENSIVE:
            defense = int(defense * 1.5)
        elif self.stance == Stance.OFFENSIVE:
            defense = int(defense * 0.8)

        if "defense_buff" in self.active_buffs:
            defense += 5

        return defense

    def compute_max_hp(self):
        hp = self.max_hp + sum(a.hp_bonus for a in self.artifacts)
        for armor in self.equipped_armor.values():
            hp += armor.hp_bonus
        if self.active_pet and self.active_pet.bonus_type == "hp":
            hp += self.active_pet.bonus_amount * 5
        hp += self.prestige_level * 10
        return hp

    def get_luck_bonus(self):
        luck = 0
        if self.active_pet and self.active_pet.bonus_type == "luck":
            luck += self.active_pet.bonus_amount
        return luck / 100.0

    def heal(self, amount):
        if self.cheat_flags.get("hehe", False):
            self.hp = 9999
        else:
            self.hp = clamp(self.hp + amount, 0, self.compute_max_hp())

    def level_up(self, times=1):
        for _ in range(times):
            self.level += 1
            self.max_hp += 10
            self.hp = self.compute_max_hp()
            self.base_damage += 2
            self.defense += 1
            self.skill_points += 1
            self.talent_points += 1

            if self.level == 10 and self.evolution_stage == 1:
                self.evolution_stage = 2
                slowprint(f"\n🌟 EVOLUTION! {self.class_name} → Elite {self.class_name}")
                self.base_damage += 5
                self.defense += 2
            elif self.level == 20 and self.evolution_stage == 2:
                self.evolution_stage = 3
                slowprint(f"\n🌟 ULTIMATE EVOLUTION! Elite {self.class_name} → Master {self.class_name}")
                self.base_damage += 10
                self.defense += 5
                self.max_hp += 50

    def prestige(self):
        if self.level >= 30:
            self.prestige_level += 1
            self.level = 1
            self.xp = 0
            self.hp = 100
            self.max_hp = 100
            slowprint(f"\n⭐ PRESTIGE {self.prestige_level}! Starting over with permanent bonuses!")
            slowprint(f"Permanent Bonuses: +{self.prestige_level*2} damage, +{self.prestige_level*10} HP")
        else:
            slowprint("Must be level 30 to prestige!")

    def add_multiclass(self, class_name):
        if not self.secondary_class:
            self.secondary_class = class_name
            slowprint(f"You are now a {self.class_name}/{class_name}!")
            self.init_class_abilities()
        else:
            slowprint("You already have a secondary class!")

    def init_class_abilities(self):
        abilities = {}

        if self.class_name == "Warrior":
            abilities.update({
                "Power Strike": {"cooldown": 3, "desc": "2x damage", "action": self.ability_power_strike},
                "Shield Bash": {"cooldown": 4, "desc": "Damage + stun", "action": self.ability_shield_bash}
            })
        elif self.class_name == "Mage":
            abilities.update({
                "Fireball": {"cooldown": 3, "desc": "High magic damage", "action": self.ability_fireball},
                "Ice Barrier": {"cooldown": 5, "desc": "Gain shield", "action": self.ability_ice_barrier}
            })
        elif self.class_name == "Rogue":
            abilities.update({
                "Backstab": {"cooldown": 2.5, "desc": "Double damage", "action": self.ability_backstab},
                "Evasion": {"cooldown": 4, "desc": "Dodge next attack", "action": self.ability_evasion}
            })
        elif self.class_name == "Berserker":
            abilities.update({
                "Rage Strike": {"cooldown": 3, "desc": "Extra dmg when HP<50%", "action": self.ability_rage_strike},
                "Bloodlust": {"cooldown": 5, "desc": "Deal dmg & heal", "action": self.ability_bloodlust}
            })
        elif self.class_name == "Assassin":
            abilities.update({
                "Poison Blade": {"cooldown": 3, "desc": "Damage over time", "action": self.ability_poison_blade},
                "Shadow Step": {"cooldown": 4, "desc": "Avoid next attack", "action": self.ability_shadow_step}
            })

        if self.secondary_class:
            if self.secondary_class == "Warrior":
                abilities["Shield Bash"] = {"cooldown": 4, "desc": "Stun", "action": self.ability_shield_bash}
            elif self.secondary_class == "Mage":
                abilities["Fireball"] = {"cooldown": 3, "desc": "Fire dmg", "action": self.ability_fireball}

        self.abilities = abilities
        for name in self.abilities:
            self.cooldown_timers.setdefault(name, 0.0)
        self.cooldown_timers.setdefault("heal", 0.0)

    def ability_power_strike(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage() * 2
        dmg = apply_elemental_damage(dmg, self.weapon.element if self.weapon else Element.PHYSICAL, target)
        target['hp'] -= dmg
        self.total_damage_dealt += dmg
        self.ultimate_charge += 10
        slowprint(f"⚔️  Power Strike hits {target['name']} for {dmg} damage!")

    def ability_shield_bash(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage() + 5
        target['hp'] -= dmg
        target['stunned'] = 2
        self.total_damage_dealt += dmg
        slowprint(f"🛡️  Shield Bash! {target['name']} stunned for 2 turns!")

    def ability_fireball(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage() + 15
        dmg = apply_elemental_damage(dmg, Element.FIRE, target)
        target['hp'] -= dmg
        if random.random() < 0.3:
            target['burning'] = 3
        self.total_damage_dealt += dmg
        self.ultimate_charge += 12
        slowprint(f"🔥 Fireball burns {target['name']} for {dmg} damage!")

    def ability_ice_barrier(self, enemies):
        self.heal(20)
        slowprint("🧊 Ice Barrier restores 20 HP!")

    def ability_backstab(self, enemies):
        target = enemies[0]
        dmg = int(self.compute_damage() * 2.5)
        target['hp'] -= dmg
        self.total_damage_dealt += dmg
        self.ultimate_charge += 15
        slowprint(f"🗡️  Backstab! {dmg} critical damage!")

    def ability_evasion(self, enemies):
        self.cheat_flags["dodge_next"] = True
        slowprint("💨 Evasion activated!")

    def ability_rage_strike(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage()
        if self.hp < self.compute_max_hp()/2:
            dmg = int(dmg * 1.8)
        target['hp'] -= dmg
        self.total_damage_dealt += dmg
        slowprint(f"😡 Rage Strike! {dmg} damage!")

    def ability_bloodlust(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage()
        heal_amt = int(dmg * 0.3)
        target['hp'] -= dmg
        self.heal(heal_amt)
        self.total_damage_dealt += dmg
        slowprint(f"🩸 Bloodlust! {dmg} damage, healed {heal_amt} HP!")

    def ability_poison_blade(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage()
        target['hp'] -= dmg
        target['poison'] = target.get('poison', 0) + 3
        self.total_damage_dealt += dmg
        slowprint(f"☠️  Poison Blade! {target['name']} poisoned!")

    def ability_shadow_step(self, enemies):
        self.cheat_flags["dodge_next"] = True
        self.cheat_flags["next_attack_boost"] = 1.5
        slowprint("🌑 Shadow Step! Dodge + damage boost!")

def get_current_weather():
    return random.choice(list(Weather))

def apply_weather_effects(weather, damage, element):
    """Weather affects elemental damage"""
    if weather == Weather.RAIN:
        if element == Element.FIRE:
            damage = int(damage * 0.7)
            slowprint("  🌧️  Rain weakens fire!")
        elif element == Element.LIGHTNING:
            damage = int(damage * 1.3)
            slowprint("  ⚡ Storm amplifies lightning!")
    elif weather == Weather.STORM:
        if element == Element.LIGHTNING:
            damage = int(damage * 1.5)
            slowprint("  ⚡ Storm empowers lightning!")
    elif weather == Weather.SNOW:
        if element == Element.ICE:
            damage = int(damage * 1.3)
            slowprint("  ❄️  Snow strengthens ice!")
    elif weather == Weather.HEAT:
        if element == Element.FIRE:
            damage = int(damage * 1.4)
            slowprint("  🔥 Heat empowers fire!")
        elif element == Element.ICE:
            damage = int(damage * 0.6)
            slowprint("  ❄️  Heat weakens ice!")
    return damage

def apply_elemental_damage(base_dmg, element, enemy):
    weakness = enemy.get('weakness', None)
    resistance = enemy.get('resistance', None)

    if element == weakness:
        base_dmg = int(base_dmg * 1.5)
        slowprint(f"  💥 SUPER EFFECTIVE! ({element.value})")
    elif element == resistance:
        base_dmg = int(base_dmg * 0.5)
        slowprint(f"  🛡️  Resisted! ({element.value})")

    return base_dmg

def check_critical_hit(player):
    crit_chance = 0.10
    if player.weapon:
        crit_chance = player.weapon.crit_chance
    if player.combo_count >= 3:
        crit_chance += 0.05
    if player.combo_count >= 5:
        crit_chance += 0.10

    crit_chance += player.get_luck_bonus()

    if random.random() < crit_chance:
        player.critical_hits += 1
        return True
    return False

def check_parry(player):
    """Chance to parry an attack"""
    parry_chance = 0.15 if player.stance == Stance.COUNTER else 0.05
    if random.random() < parry_chance:
        player.perfect_parries += 1
        return True
    return False

def capture_soul(player, enemy_name, enemy_element):
    """Capture soul from defeated enemy"""
    if random.random() < 0.3 + player.get_luck_bonus():
        power = random.randint(5, 15)
        soul = Soul(enemy_name, power, enemy_element, "")
        player.souls.append(soul)
        player.materials["Soul Fragment"] = player.materials.get("Soul Fragment", 0) + 1
        slowprint(f"✨ Captured {enemy_name}'s soul! (Power: {power})")

def sacrifice_system(player):
    """Sacrifice HP for power"""
    slowprint("\n╔══════════ BLOOD SACRIFICE ══════════╗")
    slowprint(f"  Current HP: {player.hp}/{player.compute_max_hp()}")
    slowprint("  Sacrifice HP for temporary power:")
    slowprint("  1) 20 HP → +10 damage (3 turns)")
    slowprint("  2) 50 HP → +25 damage (5 turns)")
    slowprint("  3) Back")
    slowprint("╚═════════════════════════════════════╝")

    choice = input("> ").strip()
    if choice == "1" and player.hp > 20:
        player.hp -= 20
        player.active_buffs["damage_buff"] = 3
        player.sacrifices_made += 1
        slowprint(" Sacrificed 20 HP! Damage increased!")
    elif choice == "2" and player.hp > 50:
        player.hp -= 50
        player.active_buffs["damage_buff"] = 5
        player.base_damage += 15
        player.sacrifices_made += 1
        slowprint(" Sacrificed 50 HP! Massive damage boost!")

def update_reputation(player, faction, amount):
    if faction not in player.reputation:
        player.reputation[faction] = Reputation(faction, 0, "Neutral")

    player.reputation[faction].level += amount
    level = player.reputation[faction].level

    if level >= 80:
        player.reputation[faction].rank = "Hero"
    elif level >= 50:
        player.reputation[faction].rank = "Champion"
    elif level >= 20:
        player.reputation[faction].rank = "Ally"
    elif level >= -20:
        player.reputation[faction].rank = "Neutral"
    elif level >= -50:
        player.reputation[faction].rank = "Enemy"
    else:
        player.reputation[faction].rank = "Hated"

def blacksmith_menu(player):
    while True:
        slowprint("\n╔═══════════ BLACKSMITH ═══════════╗")
        slowprint("  1) Upgrade Weapon (+5 dmg) - 100g")
        slowprint("  2) Upgrade Armor (+3 def) - 80g")
        slowprint("  3) Repair Equipment - 20g")
        slowprint("  4) Enchant Weapon - 150g + materials")
        slowprint("  5) Back")
        slowprint("╚══════════════════════════════════╝")

        choice = input("> ").strip()

        if choice == "1" and player.gold >= 100 and player.weapon:
            player.gold -= 100
            player.weapon.damage += 5
            slowprint(f"🔨 Weapon upgraded! Now deals {player.weapon.damage} damage!")
        elif choice == "2" and player.gold >= 80:
            if player.equipped_armor:
                slot = random.choice(list(player.equipped_armor.keys()))
                player.gold -= 80
                player.equipped_armor[slot].defense += 3
                slowprint(f"🔨 {player.equipped_armor[slot].name} upgraded!")
        elif choice == "4" and player.gold >= 150:
            enchant_weapon(player)
        elif choice == "5":
            break

def enchant_weapon(player):
    if not player.weapon:
        slowprint("No weapon equipped!")
        return

    slowprint("\n╔════════ ENCHANTMENTS ════════╗")
    slowprint("  1) Fire (+5 fire dmg) - 1 Dragon Scale")
    slowprint("  2) Ice (+5 ice dmg) - 2 Frost Crystals")
    slowprint("  3) Lightning (+7 lightning) - 2 Lightning Shards")
    slowprint("  4) Sharpness (+10 dmg) - 3 Iron Ore")
    slowprint("╚══════════════════════════════╝")

    choice = input("> ").strip()

    if choice == "1" and player.materials.get("Dragon Scale", 0) >= 1:
        player.materials["Dragon Scale"] -= 1
        player.gold -= 150
        player.weapon.enchantment = "Fire"
        slowprint("🔥 Weapon enchanted with Fire!")
    elif choice == "2" and player.materials.get("Frost Crystal", 0) >= 2:
        player.materials["Frost Crystal"] -= 2
        player.gold -= 150
        player.weapon.enchantment = "Ice"
        slowprint("❄️  Weapon enchanted with Ice!")

def potion_shop(player):
    while True:
        slowprint("\n╔══════════ POTION SHOP ═══════════╗")
        slowprint("  1) Health Potion (30 HP) - 5g")
        slowprint("  2) Super Potion (80 HP) - 15g")
        slowprint("  3) Max Potion (Full HP) - 50g")
        slowprint("  4) Strength Elixir (+10 dmg) - 25g")
        slowprint("  5) Defense Tonic (+5 def) - 20g")
        slowprint("  6) Back")
        slowprint("╚══════════════════════════════════╝")

        choice = input("> ").strip()

        if choice == "1" and player.gold >= 5:
            player.gold -= 5
            player.consumables["Health Potion"] = player.consumables.get("Health Potion", 0) + 1
            slowprint("Purchased Health Potion!")
        elif choice == "2" and player.gold >= 15:
            player.gold -= 15
            player.consumables["Super Potion"] = player.consumables.get("Super Potion", 0) + 1
            slowprint("Purchased Super Potion!")
        elif choice == "3" and player.gold >= 50:
            player.gold -= 50
            player.consumables["Max Potion"] = player.consumables.get("Max Potion", 0) + 1
            slowprint("Purchased Max Potion!")
        elif choice == "4" and player.gold >= 25:
            player.gold -= 25
            player.consumables["Strength Elixir"] = player.consumables.get("Strength Elixir", 0) + 1
            slowprint("Purchased Strength Elixir!")
        elif choice == "6":
            break

def weapon_shop(player):
    weapons_for_sale = ["Iron Sword", "Steel Axe", "Hunting Bow", "Flaming Blade"]
    prices = {"Iron Sword": 50, "Steel Axe": 60, "Hunting Bow": 55, "Flaming Blade": 120}

    slowprint("\n╔═════════ WEAPON SHOP ══════════╗")
    for i, weapon_name in enumerate(weapons_for_sale, 1):
        weapon = WEAPONS[weapon_name]
        price = prices[weapon_name]
        slowprint(f"  {i}) {weapon.name} - {price}g")
        slowprint(f"     +{weapon.damage} {weapon.element.value} dmg")
    slowprint(f"  {len(weapons_for_sale)+1}) Back")
    slowprint("╚════════════════════════════════╝")

    choice = input("> ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(weapons_for_sale):
            weapon_name = weapons_for_sale[idx]
            price = prices[weapon_name]
            if player.gold >= price:
                player.gold -= price
                player.inventory_weapons.append(WEAPONS[weapon_name])
                slowprint(f"Purchased {weapon_name}!")

def gambling_den(player):
    slowprint("\n╔══════════ GAMBLING DEN ═══════════╗")
    slowprint(f"  Gold: {player.gold}")
    slowprint("  1) Dice Game (Bet: 10g)")
    slowprint("  2) Card Flip (Bet: 20g)")
    slowprint("  3) Slots (Bet: 50g)")
    slowprint("  4) Back")
    slowprint("╚═══════════════════════════════════╝")

    choice = input("> ").strip()

    if choice == "1" and player.gold >= 10:
        dice_game(player)
    elif choice == "2" and player.gold >= 20:
        card_flip(player)
    elif choice == "3" and player.gold >= 50:
        slots(player)

def dice_game(player):
    player.gold -= 10
    player_roll = random.randint(1, 6) + random.randint(1, 6)
    dealer_roll = random.randint(1, 6) + random.randint(1, 6)

    slowprint(f"🎲 You rolled: {player_roll}")
    slowprint(f"🎲 Dealer rolled: {dealer_roll}")

    if player_roll > dealer_roll:
        winnings = 25
        player.gold += winnings
        slowprint(f"🎉 You win {winnings} gold!")
    elif player_roll == dealer_roll:
        slowprint("Push! Bet returned.")
        player.gold += 10
    else:
        slowprint(" You lose!")

def card_flip(player):
    player.gold -= 20
    cards = ["♠️", "♥️", "♦️", "♣️"]
    guess = random.choice(cards)
    actual = random.choice(cards)

    slowprint(f"Guess: {guess}")
    slowprint(f"Actual: {actual}")

    if guess == actual:
        winnings = 80
        player.gold += winnings
        slowprint(f" JACKPOT! Won {winnings} gold!")
    else:
        slowprint(" Wrong suit!")

def slots(player):
    player.gold -= 50
    symbols = ["🍒", "🍋", "⭐", "💎", "7️⃣"]
    result = [random.choice(symbols) for _ in range(3)]

    slowprint(f"🎰 {result[0]} | {result[1]} | {result[2]}")

    if result[0] == result[1] == result[2]:
        if result[0] == "7️⃣":
            winnings = 500
            slowprint(f"🎊 MEGA JACKPOT! Won {winnings} gold!")
        elif result[0] == "💎":
            winnings = 300
            slowprint(f"💎= Diamond win! {winnings} gold!")
        else:
            winnings = 150
            slowprint(f" Three of a kind! {winnings} gold!")
        player.gold += winnings
    elif result[0] == result[1] or result[1] == result[2]:
        winnings = 75
        player.gold += winnings
        slowprint(f"Two match! Won {winnings} gold!")
    else:
        slowprint(" No match!")

def init_achievements(player):
    achievements = [
        Achievement("ach_kills_10", "Slayer", "Defeat 10 enemies", "total_kills", 10, False, "50 gold"),
        Achievement("ach_kills_50", "Veteran", "Defeat 50 enemies", "total_kills", 50, False, "200 gold"),
        Achievement("ach_boss_1", "Boss Hunter", "Defeat first boss", "bosses", 1, False, "Epic Artifact"),
        Achievement("ach_crit_10", "Critical Master", "Land 10 crits", "crits", 10, False, "+5% crit chance"),
        Achievement("ach_parry_5", "Parry God", "Perfect parry 5 times", "parries", 5, False, "Counter stance unlocked"),
        Achievement("ach_prestige", "Reborn", "Reach prestige 1", "prestige", 1, False, "Legendary weapon"),
    ]
    player.achievements = achievements

def check_achievements(player):
    total_kills = sum(player.kills.values())

    for ach in player.achievements:
        if not ach.unlocked:
            if ach.requirement_type == "total_kills" and total_kills >= ach.requirement_value:
                ach.unlocked = True
                slowprint(f"\n ACHIEVEMENT UNLOCKED: {ach.name}!")
                slowprint(f"   {ach.description}")
                slowprint(f"   Reward: {ach.reward}")
                if "gold" in ach.reward:
                    amount = int(ach.reward.split()[0])
                    player.gold += amount
            elif ach.requirement_type == "bosses" and player.bosses_defeated >= ach.requirement_value:
                ach.unlocked = True
                slowprint(f"\n ACHIEVEMENT: {ach.name}!")
            elif ach.requirement_type == "crits" and player.critical_hits >= ach.requirement_value:
                ach.unlocked = True
                slowprint(f"\n ACHIEVEMENT: {ach.name}!")

def bounty_board(player):
    if not player.bounties:
        init_bounties(player)

    slowprint("\n╔═══════════ BOUNTY BOARD ══════════╗")
    for i, bounty in enumerate(player.bounties, 1):
        status = "✓" if bounty.completed else " "
        slowprint(f"  [{status}] {i}) {bounty.target} - {bounty.reward}g ({bounty.difficulty})")
    slowprint("╚═══════════════════════════════════╝")
    input("Press Enter...")

def init_bounties(player):
    bounties = [
        Bounty("Goblin King", 200, "Medium", False),
        Bounty("Ancient Dragon", 500, "Hard", False),
        Bounty("Shadow Assassin", 300, "Medium", False),
    ]
    player.bounties = bounties

def check_bounty_completion(player, enemy_name):
    for bounty in player.bounties:
        if bounty.target == enemy_name and not bounty.completed:
            bounty.completed = True
            player.gold += bounty.reward
            slowprint(f"\n BOUNTY COMPLETED! Earned {bounty.reward} gold!")

def talent_menu(player):
    while player.talent_points > 0:
        slowprint(f"\n╔═════ TALENT TREE ({player.talent_points} points) ════╗")
        slowprint("  1) Whirlwind Strike (AOE attack)")
        slowprint("  2) Life Drain (Heal on hit)")
        slowprint("  3) Berserker Rage (Ultimate)")
        slowprint("  4) Shadow Clone (Summon copy)")
        slowprint("  5) Save points")
        slowprint("╚══════════════════════════════════════╝")

        choice = input("> ").strip()

        if choice == "1" and "Whirlwind" not in player.talent_abilities:
            player.talent_abilities["Whirlwind"] = {
                "cooldown": 5,
                "desc": "Hit all enemies",
                "action": lambda enemies: talent_whirlwind(player, enemies)
            }
            player.talent_points -= 1
            slowprint("Learned Whirlwind Strike!")
        elif choice == "5":
            break

def talent_whirlwind(player, enemies):
    dmg = player.compute_damage()
    slowprint("  WHIRLWIND STRIKE!")
    for enemy in enemies:
        if enemy['hp'] > 0:
            enemy['hp'] -= dmg
            slowprint(f"   Hit {enemy['name']} for {dmg} damage!")

def recruit_companion_menu(player):
    available = [c for c in COMPANIONS_POOL if c not in player.companions]

    if not available:
        slowprint("No companions available to recruit!")
        return

    slowprint("\n╔════════ RECRUIT COMPANION ═══════╗")
    for i, comp in enumerate(available, 1):
        slowprint(f"  {i}) {comp.name} ({comp.class_type})")
        slowprint(f"     HP:{comp.max_hp} ATK:{comp.damage} DEF:{comp.defense}")
    slowprint(f"  {len(available)+1}) Back")
    slowprint("╚══════════════════════════════════╝")

    choice = input("> ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(available):
            companion = available[idx]
            if player.gold >= 100:
                player.gold -= 100
                player.companions.append(companion)
                slowprint(f"{companion.name} joined your party!")
            else:
                slowprint("Need 100 gold to recruit!")

def manage_party(player):
    slowprint("\n╔════════ PARTY MANAGEMENT ════════╗")
    slowprint("  Active Companions:")
    for comp in player.active_companions:
        slowprint(f"    - {comp.name} (Lv.{comp.level})")
    slowprint("\n  Available Companions:")
    for i, comp in enumerate(player.companions, 1):
        if comp not in player.active_companions:
            slowprint(f"    {i}) {comp.name} ({comp.class_type})")
    slowprint("╚══════════════════════════════════╝")

def battle(player, enemies, battle_count, weather):
    slowprint(f"\n⚔️  Battle {battle_count} - Weather: {weather.value}")

    is_boss = any(e.get("boss", False) for e in enemies)

    if is_boss:
        slowprint("="*50)
        slowprint("★★★ BOSS BATTLE ★★★")
        slowprint("="*50)

    for enemy in enemies:
        slowprint(f"  {enemy['name']} (HP: {enemy['hp']})")
        enemy['stunned'] = 0
        enemy['poison'] = 0
        enemy['burning'] = 0

    turn = 0

    while any(e['hp'] > 0 for e in enemies) and player.hp > 0:
        turn += 1
        slowprint(f"\n{'─'*50}")
        slowprint(f"Turn {turn} | Stance: {player.stance.value}")
        slowprint(f"{player.name} HP:{player.hp}/{player.compute_max_hp()} | Ultimate:{player.ultimate_charge}/{player.ultimate_max}")

        for i, enemy in enumerate(enemies, 1):
            if enemy['hp'] > 0:
                slowprint(f"  [{i}] {enemy['name']} HP:{enemy['hp']}/{enemy['max_hp']}")

        for comp in player.active_companions:
            if comp.hp > 0 and enemies:
                alive_enemies = [e for e in enemies if e['hp'] > 0]
                if alive_enemies:
                    target = alive_enemies[0]
                    dmg = comp.damage
                    target['hp'] -= dmg
                    slowprint(f" {comp.name} attacks {target['name']} for {dmg}!")

        slowprint("\n[1] Attack [2] Ability [3] Item [4] Stance")
        slowprint("[5] Companions [6] Ultimate [7] Sacrifice [8] Flee [0] Cheat")
        choice = input("> ").strip()

        if choice == "0":
            code = input("Cheat code: ").strip()
            check_cheats(player, code)
            continue

        if choice == "4":
            change_stance(player)
            continue

        if choice == "7":
            sacrifice_system(player)
            continue

        if choice == "6" and player.ultimate_charge >= player.ultimate_max:
            use_ultimate(player, enemies)
            player.ultimate_charge = 0
            continue

        alive_enemies = [e for e in enemies if e['hp'] > 0]
        if not alive_enemies:
            break

        if choice == "1":
            target_idx = 0
            if len(alive_enemies) > 1:
                target_idx = int(input("Target enemy #: ").strip()) - 1
                target_idx = clamp(target_idx, 0, len(alive_enemies) - 1)

            target = alive_enemies[target_idx]
            dmg = player.compute_damage()

            if check_critical_hit(player):
                dmg = int(dmg * 2)
                slowprint(" CRITICAL HIT!")

            element = player.weapon.element if player.weapon else Element.PHYSICAL
            dmg = apply_weather_effects(weather, dmg, element)
            dmg = apply_elemental_damage(dmg, element, target)

            target['hp'] -= dmg
            player.total_damage_dealt += dmg
            player.ultimate_charge += 5
            slowprint(f"  {dmg} damage to {target['name']}!")

            if player.weapon and player.weapon.is_legendary:
                if "Heals" in player.weapon.legendary_effect and target['hp'] <= 0:
                    heal_amt = int(player.compute_max_hp() * 0.1)
                    player.heal(heal_amt)
                    slowprint(f"   {player.weapon.name} heals {heal_amt} HP!")

        elif choice == "2":
            use_ability(player, alive_enemies)

        elif choice == "3":
            use_item(player)

        if all(e['hp'] <= 0 for e in enemies):
            break

        for enemy in enemies:
            if enemy['hp'] > 0:
                if enemy['stunned'] > 0:
                    enemy['stunned'] -= 1
                    slowprint(f" {enemy['name']} is stunned!")
                    continue

                if check_parry(player):
                    slowprint(f"  PERFECT PARRY! Countered {enemy['name']}!")
                    counter_dmg = player.compute_damage()
                    enemy['hp'] -= counter_dmg
                    slowprint(f"   Counter: {counter_dmg} damage!")
                    continue

                dmg = enemy.get('atk', 10)
                dmg = max(0, dmg - player.compute_defense())
                player.hp -= dmg
                if dmg > 0:
                    slowprint(f" {enemy['name']} hits for {dmg}!")

        for enemy in enemies:
            if enemy.get('poison', 0) > 0:
                enemy['hp'] -= 5
                enemy['poison'] -= 1
                slowprint(f"  {enemy['name']} takes poison damage!")
            if enemy.get('burning', 0) > 0:
                enemy['hp'] -= 7
                enemy['burning'] -= 1
                slowprint(f" {enemy['name']} takes burn damage!")

        for key in player.cooldown_timers:
            if player.cooldown_timers[key] > 0:
                player.cooldown_timers[key] -= 1

        for buff in list(player.active_buffs.keys()):
            player.active_buffs[buff] -= 1
            if player.active_buffs[buff] <= 0:
                del player.active_buffs[buff]

    if player.hp > 0:
        slowprint("\n VICTORY!")

        total_gold = 0
        total_xp = 0

        for enemy in enemies:
            player.kills[enemy['name']] = player.kills.get(enemy['name'], 0) + 1

            gold = random.randint(20, 50) * (2 if enemy.get('boss') else 1)
            total_gold += gold
            total_xp += 50 if enemy.get('boss') else 20

            enemy_element = enemy.get('element', Element.PHYSICAL)
            capture_soul(player, enemy['name'], enemy_element)

            check_bounty_completion(player, enemy['name'])

        player.gold += total_gold
        slowprint(f"💰 Earned {total_gold} gold, {total_xp} XP")

        gain_xp(player, total_xp)
        check_achievements(player)

        return True
    else:
        return False

def change_stance(player):
    slowprint("\n╔════════ CHANGE STANCE ═══════╗")
    slowprint("  1) Balanced (Normal)")
    slowprint("  2) Offensive (+30% dmg, -20% def)")
    slowprint("  3) Defensive (+50% def, -30% dmg)")
    slowprint("  4) Counter (High parry chance)")
    slowprint("╚══════════════════════════════╝")

    choice = input("> ").strip()
    if choice == "1":
        player.stance = Stance.BALANCED
    elif choice == "2":
        player.stance = Stance.OFFENSIVE
    elif choice == "3":
        player.stance = Stance.DEFENSIVE
    elif choice == "4":
        player.stance = Stance.COUNTER
    slowprint(f"Stance: {player.stance.value}")

def use_ultimate(player, enemies):
    slowprint("\n💫 ULTIMATE ATTACK!")

    if player.class_name == "Warrior":
        slowprint("⚔️  TITAN'S WRATH!")
        for enemy in enemies:
            if enemy['hp'] > 0:
                dmg = player.compute_damage() * 3
                enemy['hp'] -= dmg
                enemy['stunned'] = 2
                slowprint(f"  💥 {dmg} damage to {enemy['name']}! Stunned!")

    elif player.class_name == "Mage":
        slowprint("🔥 METEOR STORM!")
        for enemy in enemies:
            if enemy['hp'] > 0:
                dmg = player.compute_damage() * 2.5
                enemy['hp'] -= dmg
                enemy['burning'] = 3
                slowprint(f"  🔥 {dmg} fire damage to {enemy['name']}!")

    else:
        target = [e for e in enemies if e['hp'] > 0][0]
        dmg = player.compute_damage() * 4
        target['hp'] -= dmg
        slowprint(f"  💥 {dmg} massive damage!")

def use_ability(player, enemies):
    abilities = list(player.abilities.keys())
    slowprint("\nAbilities:")
    for i, ability in enumerate(abilities, 1):
        cd = player.cooldown_timers.get(ability, 0)
        status = f"CD: {cd}" if cd > 0 else "Ready"
        slowprint(f"  {i}) {ability} ({status})")

    choice = input("Select ability: ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(abilities):
            ability_name = abilities[idx]
            if player.cooldown_timers.get(ability_name, 0) <= 0:
                player.abilities[ability_name]['action'](enemies)
                player.cooldown_timers[ability_name] = player.abilities[ability_name]['cooldown']

def use_item(player):
    if not player.consumables:
        slowprint("No consumables!")
        return

    slowprint("\n╔════════ CONSUMABLES ════════╗")
    items = list(player.consumables.items())
    for i, (name, count) in enumerate(items, 1):
        slowprint(f"  {i}) {name} x{count}")
    slowprint("╚═════════════════════════════╝")

    choice = input("Use item: ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(items):
            item_name = items[idx][0]
            if player.consumables[item_name] > 0:
                consumable = CONSUMABLES[item_name]
                player.consumables[item_name] -= 1

                if consumable.effect_type == "heal":
                    player.heal(consumable.power)
                    slowprint(f"💚 Healed {consumable.power} HP!")
                elif consumable.effect_type == "buff_damage":
                    player.active_buffs["damage_buff"] = consumable.duration
                    slowprint("💪 Damage increased!")

def check_cheats(player, code):
    code = code.strip()
    original_code = code
    code_lower = code.lower()

    if code_lower == "hehe":
        player.cheat_flags["hehe"] = not player.cheat_flags["hehe"]
        slowprint(f"CHEAT: Infinite Health {'ON' if player.cheat_flags['hehe'] else 'OFF'}")
        if player.cheat_flags["hehe"]:
            player.hp = 9999
    elif code_lower == "haha":
        player.cheat_flags["haha"] = not player.cheat_flags["haha"]
        slowprint(f"CHEAT: No cooldown {'ON' if player.cheat_flags['haha'] else 'OFF'}")
    elif code_lower == "hihi":
        player.cheat_flags["hihi"] = not player.cheat_flags["hihi"]
        slowprint(f"CHEAT: One-hit {'ON' if player.cheat_flags['hihi'] else 'OFF'}")
    elif code_lower == "hoho":
        player.base_damage *= 10
        player.defense *= 10
        slowprint("CHEAT: Stats x10!")
    elif code_lower == "huhu":
        player.level_up(10)
        slowprint("CHEAT: Level +10!")
    elif original_code == "013113":
        player.gold += 1000
        slowprint("CHEAT: +1000 Gold!")
    elif original_code == "6767":
        player.skill_points += 10
        player.talent_points += 10
        slowprint("CHEAT: +10 Skill & Talent Points!")

def gain_xp(player, amount):
    player.xp += amount
    while player.xp >= player.xp_to_next:
        player.xp -= player.xp_to_next
        player.xp_to_next = int(player.xp_to_next * 1.2)
        player.level_up()
        slowprint(f"🌟 LEVEL UP! Now level {player.level}!")

def character_creation():
    slowprint("="*60)
    slowprint("  🗡️  DUNGEON RPG: ULTIMATE EDITION 🗡️")
    slowprint("="*60)

    name = input("\nHero name: ").strip() or "Hero"

    slowprint("\nChoose class:")
    slowprint("1) Warrior - Tank with high HP")
    slowprint("2) Mage - High magic damage")
    slowprint("3) Rogue - Fast attacks")
    slowprint("4) Berserker - High risk High reward")
    slowprint("5) Assassin - Poison master")

    choice = input("> ").strip()
    player = Player(name=name)

    if choice == "1":
        player.class_name = "Warrior"
        player.max_hp += 30
        player.hp = player.max_hp
        player.base_damage += 3
    elif choice == "2":
        player.class_name = "Mage"
        player.base_damage += 12
    elif choice == "3":
        player.class_name = "Rogue"
        player.base_damage += 5
    elif choice == "4":
        player.class_name = "Berserker"
        player.base_damage += 8
    elif choice == "5":
        player.class_name = "Assassin"
        player.base_damage += 6

    player.weapon = WEAPONS["Rusty Sword"]
    player.init_class_abilities()
    init_achievements(player)
    init_bounties(player)

    player.consumables["Health Potion"] = 3

    slowprint(f"\n{name} the {player.class_name} is ready!")
    return player

def main():
    player = character_creation()
    battle_count = 0

    regular_enemies = [
        {"name": "Goblin", "hp": 50, "max_hp": 50, "atk": 8, "element": Element.PHYSICAL},
        {"name": "Wolf", "hp": 45, "max_hp": 45, "atk": 12, "element": Element.PHYSICAL},
        {"name": "Skeleton", "hp": 60, "max_hp": 60, "atk": 7, "element": Element.DARK},
        {"name": "Ogre", "hp": 80, "max_hp": 80, "atk": 15, "element": Element.PHYSICAL},
    ]

    bosses = [
        {"name": "Dragon", "hp": 200, "max_hp": 200, "atk": 25, "boss": True, "element": Element.FIRE,
         "weakness": Element.ICE, "resistance": Element.FIRE},
        {"name": "Lich King", "hp": 180, "max_hp": 180, "atk": 22, "boss": True, "element": Element.DARK,
         "weakness": Element.HOLY, "resistance": Element.DARK},
    ]

    while player.hp > 0:
        battle_count += 1
        weather = get_current_weather()

        slowprint("\n╔════════ TOWN ═══════╗")
        slowprint("  1) Next Battle")
        slowprint("  2) Blacksmith")
        slowprint("  3) Potion Shop")
        slowprint("  4) Weapon Shop")
        slowprint("  5) Gambling Den")
        slowprint("  6) Bounty Board")
        slowprint("  7) Recruit Companion")
        slowprint("  8) Cresthaven Tree")
        slowprint("  9) Hostel (Full heal)")
        slowprint("╚═════════════════════╝")

        choice = input("> ").strip()

        if choice == "2":
            blacksmith_menu(player)
            continue
        elif choice == "3":
            potion_shop(player)
            continue
        elif choice == "4":
            weapon_shop(player)
            continue
        elif choice == "5":
            gambling_den(player)
            continue
        elif choice == "6":
            bounty_board(player)
            continue
        elif choice == "7":
            recruit_companion_menu(player)
            continue
        elif choice == "8":
            talent_menu(player)
            continue
        elif choice == "9":
            player.hp = player.compute_max_hp()
            slowprint("💚 Fully healed!")
            continue

        if battle_count % 10 == 0:
            enemies = [dict(random.choice(bosses))]
        else:
            party_size = len(player.active_companions) + 1
            num_enemies = min(random.randint(1, party_size), 3)
            enemies = [dict(random.choice(regular_enemies)) for _ in range(num_enemies)]

        if not battle(player, enemies, battle_count, weather):
            slowprint("\n💀 GAME OVER")
            slowprint(f"Final Level: {player.level}")
            slowprint(f"Total Kills: {sum(player.kills.values())}")
            slowprint(f"Gold Earned: {player.gold}")
            break

if __name__ == "__main__":
    main()
#HI
#WYD
#IM-BORED
#NO THIS IS NOT AI
# LOOKIN AT ARYA ARYA!!!!
# YES YOU HELPED WITH LIKE 3 LINES A YEAR AGO
#I MADE THIS
#CREDIT GOES TO AKSHAY KOTTA
# A.K.A THE TACO GOD :D
# A.K.A THE PIZZA GOD :D
# A.K.A POTATO MAN :D
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#HEHEHEHHEHEHEHHEHEHEH
#1.5k lines including my horrendous laugh IYKYK


