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

# Hybrid class combinations - ALL CLASSES
HYBRID_CLASSES = {
    # Warrior Hybrids
    ("Warrior", "Mage"): {
        "name": "Spellblade",
        "bonus_hp": 20,
        "bonus_damage": 8,
        "special": "Magic-infused strikes deal bonus elemental damage"
    },
    ("Warrior", "Rogue"): {
        "name": "Duelist",
        "bonus_hp": 15,
        "bonus_damage": 6,
        "special": "Critical strikes deal 3x damage instead of 2x"
    },
    ("Warrior", "Berserker"): {
        "name": "Warlord",
        "bonus_hp": 40,
        "bonus_damage": 10,
        "special": "Gain damage and defense as HP decreases"
    },
    ("Warrior", "Assassin"): {
        "name": "Shadowknight",
        "bonus_hp": 20,
        "bonus_damage": 8,
        "special": "Attacks have chance to poison and stun"
    },
    ("Warrior", "Paladin"): {
        "name": "Crusader",
        "bonus_hp": 35,
        "bonus_damage": 7,
        "special": "Holy strikes that heal on hit"
    },
    ("Warrior", "Necromancer"): {
        "name": "Death Knight",
        "bonus_hp": 25,
        "bonus_damage": 9,
        "special": "Drain life from enemies with each attack"
    },
    ("Warrior", "Monk"): {
        "name": "Battle Monk",
        "bonus_hp": 20,
        "bonus_damage": 8,
        "special": "Counter attacks with increased damage"
    },
    ("Warrior", "Ranger"): {
        "name": "Warden",
        "bonus_hp": 25,
        "bonus_damage": 7,
        "special": "Beast companion adds damage to attacks"
    },
    ("Warrior", "Druid"): {
        "name": "Guardian",
        "bonus_hp": 30,
        "bonus_damage": 6,
        "special": "Shapeshift for bonus defense or offense"
    },
    ("Warrior", "Samurai"): {
        "name": "Sword Saint",
        "bonus_hp": 25,
        "bonus_damage": 9,
        "special": "Perfect counters deal massive damage"
    },
    ("Warrior", "Warlock"): {
        "name": "Hellknight",
        "bonus_hp": 20,
        "bonus_damage": 10,
        "special": "Demonic armor absorbs damage"
    },

    # Mage Hybrids
    ("Mage", "Rogue"): {
        "name": "Trickster",
        "bonus_hp": 10,
        "bonus_damage": 12,
        "special": "Spells can critically strike"
    },
    ("Mage", "Berserker"): {
        "name": "Blood Mage",
        "bonus_hp": 15,
        "bonus_damage": 15,
        "special": "Sacrifice HP to amplify spell damage"
    },
    ("Mage", "Assassin"): {
        "name": "Hexblade",
        "bonus_hp": 10,
        "bonus_damage": 13,
        "special": "Curses enemies reducing their damage"
    },
    ("Mage", "Paladin"): {
        "name": "Cleric",
        "bonus_hp": 20,
        "bonus_damage": 10,
        "special": "Holy magic heals allies and smites foes"
    },
    ("Mage", "Necromancer"): {
        "name": "Lich",
        "bonus_hp": 15,
        "bonus_damage": 14,
        "special": "Undead servants fight alongside you"
    },
    ("Mage", "Monk"): {
        "name": "Mystic",
        "bonus_hp": 12,
        "bonus_damage": 11,
        "special": "Chi-infused spells with reduced cooldowns"
    },
    ("Mage", "Ranger"): {
        "name": "Arcane Archer",
        "bonus_hp": -95,
        "bonus_damage": 2000,
        "special": "Arrows explode with elemental magic"
    },
    ("Mage", "Druid"): {
        "name": "Archdruid",
        "bonus_hp": 18,
        "bonus_damage": 10,
        "special": "Nature and arcane magic combined"
    },
    ("Mage", "Samurai"): {
        "name": "Battlemage",
        "bonus_hp": 15,
        "bonus_damage": 11,
        "special": "Weapon strikes trigger spell effects"
    },
    ("Mage", "Warlock"): {
        "name": "Sorcerer",
        "bonus_hp": 10,
        "bonus_damage": 16,
        "special": "Chaotic magic with random powerful effects"
    },

    # Rogue Hybrids
    ("Rogue", "Berserker"): {
        "name": "Ravager",
        "bonus_hp": 20,
        "bonus_damage": 12,
        "special": "High crit chance with lifesteal"
    },
    ("Rogue", "Assassin"): {
        "name": "Nightblade",
        "bonus_hp": 10,
        "bonus_damage": 10,
        "special": "Extreme evasion and critical damage"
    },
    ("Rogue", "Paladin"): {
        "name": "Inquisitor",
        "bonus_hp": 15,
        "bonus_damage": 9,
        "special": "Holy strikes from stealth deal bonus damage"
    },
    ("Rogue", "Necromancer"): {
        "name": "Soul Reaper",
        "bonus_hp": 12,
        "bonus_damage": 11,
        "special": "Steal souls with critical hits"
    },
    ("Rogue", "Monk"): {
        "name": "Ninja",
        "bonus_hp": 10,
        "bonus_damage": 10,
        "special": "Lightning-fast combo attacks"
    },
    ("Rogue", "Ranger"): {
        "name": "Stalker",
        "bonus_hp": 15,
        "bonus_damage": 9,
        "special": "Perfect ambush with beast companion"
    },
    ("Rogue", "Druid"): {
        "name": "Shapeshifter",
        "bonus_hp": 18,
        "bonus_damage": 8,
        "special": "Transform for stealth or savage attacks"
    },
    ("Rogue", "Samurai"): {
        "name": "Shinobi",
        "bonus_hp": 12,
        "bonus_damage": 10,
        "special": "Shadow techniques with honorable finishers"
    },
    ("Rogue", "Warlock"): {
        "name": "Shadow Pact",
        "bonus_hp": 10,
        "bonus_damage": 12,
        "special": "Dark powers enhance stealth abilities"
    },

    # Berserker Hybrids
    ("Berserker", "Assassin"): {
        "name": "Reaper",
        "bonus_hp": 15,
        "bonus_damage": 14,
        "special": "Killing enemies extends berserk mode"
    },
    ("Berserker", "Paladin"): {
        "name": "Zealot",
        "bonus_hp": 30,
        "bonus_damage": 11,
        "special": "Holy rage increases with damage taken"
    },
    ("Berserker", "Necromancer"): {
        "name": "Bloodlord",
        "bonus_hp": 20,
        "bonus_damage": 13,
        "special": "Blood magic fuels berserk frenzy"
    },
    ("Berserker", "Monk"): {
        "name": "Ragemaster",
        "bonus_hp": 18,
        "bonus_damage": 11,
        "special": "Channel rage into devastating combos"
    },
    ("Berserker", "Ranger"): {
        "name": "Beastmaster",
        "bonus_hp": 22,
        "bonus_damage": 10,
        "special": "Beast companion enters rage mode with you"
    },
    ("Berserker", "Druid"): {
        "name": "Savage",
        "bonus_hp": 25,
        "bonus_damage": 12,
        "special": "Primal fury in any form"
    },
    ("Berserker", "Samurai"): {
        "name": "Ronin",
        "bonus_hp": 20,
        "bonus_damage": 12,
        "special": "Dishonored fury with precise strikes"
    },
    ("Berserker", "Warlock"): {
        "name": "Chaos Warrior",
        "bonus_hp": 18,
        "bonus_damage": 14,
        "special": "Demonic rage with random effects"
    },

    # Assassin Hybrids
    ("Assassin", "Paladin"): {
        "name": "Divine Assassin",
        "bonus_hp": 15,
        "bonus_damage": 10,
        "special": "Holy poison purifies as it kills"
    },
    ("Assassin", "Necromancer"): {
        "name": "Plague Bringer",
        "bonus_hp": 12,
        "bonus_damage": 12,
        "special": "Poison spreads like undead plague"
    },
    ("Assassin", "Monk"): {
        "name": "Silent Fist",
        "bonus_hp": 10,
        "bonus_damage": 11,
        "special": "Pressure point strikes with poison"
    },
    ("Assassin", "Ranger"): {
        "name": "Sniper",
        "bonus_hp": 12,
        "bonus_damage": 10,
        "special": "Poison arrows from extreme range"
    },
    ("Assassin", "Druid"): {
        "name": "Venom Druid",
        "bonus_hp": 15,
        "bonus_damage": 9,
        "special": "Natural toxins in any form"
    },
    ("Assassin", "Samurai"): {
        "name": "Shadow Samurai",
        "bonus_hp": 12,
        "bonus_damage": 11,
        "special": "Honorable kills with deadly precision"
    },
    ("Assassin", "Warlock"): {
        "name": "Cult Assassin",
        "bonus_hp": 10,
        "bonus_damage": 13,
        "special": "Cursed blades that damn victims"
    },

    # Paladin Hybrids
    ("Paladin", "Necromancer"): {
        "name": "Gray Paladin",
        "bonus_hp": 25,
        "bonus_damage": 10,
        "special": "Balance life and death magic"
    },
    ("Paladin", "Monk"): {
        "name": "Holy Fist",
        "bonus_hp": 20,
        "bonus_damage": 9,
        "special": "Divine chi enhances martial arts"
    },
    ("Paladin", "Ranger"): {
        "name": "Holy Warden",
        "bonus_hp": 25,
        "bonus_damage": 8,
        "special": "Blessed beasts fight evil"
    },
    ("Paladin", "Druid"): {
        "name": "Nature's Champion",
        "bonus_hp": 28,
        "bonus_damage": 7,
        "special": "Divine nature magic heals and protects"
    },
    ("Paladin", "Samurai"): {
        "name": "Holy Blade",
        "bonus_hp": 25,
        "bonus_damage": 9,
        "special": "Sacred honor empowers strikes"
    },
    ("Paladin", "Warlock"): {
        "name": "Fallen Paladin",
        "bonus_hp": 20,
        "bonus_damage": 12,
        "special": "Corrupted holy power"
    },

    # Necromancer Hybrids
    ("Necromancer", "Monk"): {
        "name": "Death Monk",
        "bonus_hp": 12,
        "bonus_damage": 11,
        "special": "Life-draining martial arts"
    },
    ("Necromancer", "Ranger"): {
        "name": "Bone Ranger",
        "bonus_hp": 15,
        "bonus_damage": 10,
        "special": "Skeletal beasts as companions"
    },
    ("Necromancer", "Druid"): {
        "name": "Blight Druid",
        "bonus_hp": 18,
        "bonus_damage": 10,
        "special": "Decay magic corrupts nature"
    },
    ("Necromancer", "Samurai"): {
        "name": "Undead Samurai",
        "bonus_hp": 15,
        "bonus_damage": 11,
        "special": "Cursed blade never rests"
    },
    ("Necromancer", "Warlock"): {
        "name": "Dark Summoner",
        "bonus_hp": 12,
        "bonus_damage": 14,
        "special": "Demons and undead fight together"
    },

    # Monk Hybrids
    ("Monk", "Ranger"): {
        "name": "Way of the Beast",
        "bonus_hp": 15,
        "bonus_damage": 8,
        "special": "Chi flows through beast companion"
    },
    ("Monk", "Druid"): {
        "name": "Jade Druid",
        "bonus_hp": 18,
        "bonus_damage": 7,
        "special": "Harmony between all forms"
    },
    ("Monk", "Samurai"): {
        "name": "Kensei",
        "bonus_hp": 15,
        "bonus_damage": 9,
        "special": "Master of blade and fist"
    },
    ("Monk", "Warlock"): {
        "name": "Demon Monk",
        "bonus_hp": 12,
        "bonus_damage": 11,
        "special": "Dark chi corrupts strikes"
    },

    # Ranger Hybrids
    ("Ranger", "Druid"): {
        "name": "Wildlord",
        "bonus_hp": 20,
        "bonus_damage": 8,
        "special": "Command all beasts and nature"
    },
    ("Ranger", "Samurai"): {
        "name": "Bow Saint",
        "bonus_hp": 18,
        "bonus_damage": 9,
        "special": "Perfect shots with honorable precision"
    },
    ("Ranger", "Warlock"): {
        "name": "Dark Ranger",
        "bonus_hp": 15,
        "bonus_damage": 11,
        "special": "Cursed arrows and demon beasts"
    },

    # Druid Hybrids
    ("Druid", "Samurai"): {
        "name": "Primal Samurai",
        "bonus_hp": 20,
        "bonus_damage": 8,
        "special": "Honor in natural and warrior forms"
    },
    ("Druid", "Warlock"): {
        "name": "Corruptor",
        "bonus_hp": 18,
        "bonus_damage": 10,
        "special": "Twisted nature serves dark masters"
    },

    # Samurai Hybrids
    ("Samurai", "Warlock"): {
        "name": "Cursed Blade",
        "bonus_hp": 15,
        "bonus_damage": 12,
        "special": "Demon-possessed weapon techniques"
    },
}


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
    # Common Weapons
    "Rusty Sword": Weapon("Rusty Sword", WeaponType.SWORD, 5, Element.PHYSICAL, 0.05, "A weathered blade", "Common"),
    "Iron Sword": Weapon("Iron Sword", WeaponType.SWORD, 12, Element.PHYSICAL, 0.08, "Standard iron blade", "Common"),
    "Steel Axe": Weapon("Steel Axe", WeaponType.AXE, 15, Element.PHYSICAL, 0.10, "Heavy chopping weapon", "Common"),
    "Hunting Bow": Weapon("Hunting Bow", WeaponType.BOW, 10, Element.PHYSICAL, 0.15, "Precise ranged weapon", "Common"),
    "Oak Staff": Weapon("Oak Staff", WeaponType.STAFF, 8, Element.PHYSICAL, 0.05, "Basic magic staff", "Common"),
    "Iron Dagger": Weapon("Iron Dagger", WeaponType.DAGGER, 9, Element.PHYSICAL, 0.20, "Quick strikes", "Common"),
    "Bronze Spear": Weapon("Bronze Spear", WeaponType.SPEAR, 11, Element.PHYSICAL, 0.07, "Simple spear", "Common"),
    "Wooden Club": Weapon("Wooden Club", WeaponType.HAMMER, 10, Element.PHYSICAL, 0.05, "Primitive weapon", "Common"),

    # Rare Weapons
    "Flaming Blade": Weapon("Flaming Blade", WeaponType.SWORD, 20, Element.FIRE, 0.12, "Engulfed in flames", "Rare"),
    "Frostbite": Weapon("Frostbite", WeaponType.SWORD, 22, Element.ICE, 0.10, "Freezes enemies", "Rare"),
    "Thunderstrike": Weapon("Thunderstrike", WeaponType.AXE, 25, Element.LIGHTNING, 0.15, "Crackling with energy", "Rare"),
    "Shadow Dagger": Weapon("Shadow Dagger", WeaponType.DAGGER, 18, Element.DARK, 0.25, "Strikes from shadows", "Rare"),
    "Holy Spear": Weapon("Holy Spear", WeaponType.SPEAR, 24, Element.HOLY, 0.12, "Blessed weapon", "Rare"),
    "War Hammer": Weapon("War Hammer", WeaponType.HAMMER, 28, Element.PHYSICAL, 0.08, "Crushes armor", "Rare"),
    "Venom Dagger": Weapon("Venom Dagger", WeaponType.DAGGER, 17, Element.POISON, 0.18, "Drips with toxin", "Rare"),
    "Gale Bow": Weapon("Gale Bow", WeaponType.BOW, 21, Element.WIND, 0.16, "Shoots wind arrows", "Rare"),
    "Inferno Staff": Weapon("Inferno Staff", WeaponType.STAFF, 23, Element.FIRE, 0.10, "Burns with hellfire", "Rare"),
    "Glacier Axe": Weapon("Glacier Axe", WeaponType.AXE, 24, Element.ICE, 0.11, "Freezing cold", "Rare"),

    # Epic Weapons
    "Dragon Slayer": Weapon("Dragon Slayer", WeaponType.SWORD, 35, Element.FIRE, 0.18, "Forged from dragon scales", "Epic"),
    "Void Scythe": Weapon("Void Scythe", WeaponType.SCYTHE, 32, Element.DARK, 0.22, "Harvests souls", "Epic"),
    "Stormbringer": Weapon("Stormbringer", WeaponType.SPEAR, 36, Element.LIGHTNING, 0.19, "Calls down lightning", "Epic"),
    "Demon's Embrace": Weapon("Demon's Embrace", WeaponType.SCYTHE, 34, Element.DARK, 0.20, "Cursed by demons", "Epic"),
    "Phoenix Bow": Weapon("Phoenix Bow", WeaponType.BOW, 33, Element.FIRE, 0.21, "Reborn from ashes", "Epic"),
    "Celestial Staff": Weapon("Celestial Staff", WeaponType.STAFF, 37, Element.HOLY, 0.15, "Blessed by angels", "Epic"),
    "Abyssal Blade": Weapon("Abyssal Blade", WeaponType.SWORD, 38, Element.DARK, 0.17, "Forged in the abyss", "Epic"),
    "Worldbreaker": Weapon("Worldbreaker", WeaponType.HAMMER, 40, Element.PHYSICAL, 0.12, "Shatters mountains", "Epic"),
    "Soul Render": Weapon("Soul Render", WeaponType.DAGGER, 31, Element.DARK, 0.28, "Tears at the soul", "Epic"),
    "Typhoon Blade": Weapon("Typhoon Blade", WeaponType.SWORD, 35, Element.WIND, 0.19, "Cuts like the wind", "Epic"),
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
    "Thunder":{"damage": 5, "element": Element.LIGHTNING},
    "Lightning": {"damage": 7, "element": Element.LIGHTNING},
    "Sharpness": {"damage": 10, "element": None},
    "Fortify": {"defense": 5, "hp": 20},
    "Lifesteal": {"lifesteal": 0.15},
    "Holy": {"damage": 6, "element": Element.HOLY},
    "Dark": {"damage": 6, "element": Element.DARK},
    "Poison": {"damage": 4, "element": Element.POISON},
    "Wind": {"damage": 5, "element": Element.WIND},
    "Vorpal": {"damage": 12, "crit": 0.05},
    "Vampiric": {"lifesteal": 0.20},
    "Giant Slayer": {"damage": 8, "boss_bonus": 1.5},
    "Dragonbane": {"damage": 10, "dragon_bonus": 2.0},
    "Smite": {"damage": 7, "undead_bonus": 1.8},
    "Berserking": {"damage": 5, "low_hp_bonus": 1.3},
    "Swift": {"cooldown": -10},
    "Soulbound": {"damage": 8, "hp": 15},
    "Chaos": {"damage_random": (5, 20)},
}

COMPANIONS_POOL = [
    Companion("Sir Reginald", "Knight", 1, 100, 100, 12, 5, "Shield Wall", 50, "defensive"),
    Companion("Aria", "Archer", 1, 70, 70, 15, 2, "Rapid Shot", 50, "aggressive"),
    Companion("Gandor", "Mage", 1, 60, 60, 18, 1, "Fireball", 50, "balanced"),
    Companion("Shadow", "Rogue", 1, 75, 75, 14, 3, "Backstab", 50, "aggressive"),
    Companion("Eragon", "Rider", 1, 100, 100, 12, 5, "Dragon Waves", 55, "Balanced"),
    Companion("Uzoth", "Knight", 1, 70, 70, 15, 2, "Dragon Talon ", 50, "defensive"),
    Companion("Griffith", "Rouge", 1, 60, 60, 18, 1, "Meteor Strike", 50, "Counter"),
    Companion("Bolt", "Knight", 1, 75, 75, 14, 3, "Flurry Rush", 50, "Counter"),
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
    hybrid_class_name: Optional[str] = None
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
    skill_levels: Dict[str, int] = field(default_factory=dict)  # Track skill levels
    evolution_stage: int = 1
    prestige_bonuses: Dict[str, int] = field(default_factory=dict)  # Track prestige bonuses

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
    berserk_mode: bool = False
    curse_active: bool = False

    cheat_flags: Dict[str,object] = field(default_factory=lambda: {
        "hehe": False, "haha": False, "hihi": False, "hoho": False, "huhu": False,
        "013113": False, "6767": False,
        "dodge_next": False, "next_attack_boost": 1.0
    })

    def get_hybrid_info(self):
        """Get hybrid class bonuses if applicable"""
        if self.secondary_class:
            key1 = (self.class_name, self.secondary_class)
            key2 = (self.secondary_class, self.class_name)
            return HYBRID_CLASSES.get(key1) or HYBRID_CLASSES.get(key2)
        return None

    def compute_damage(self):
        dmg = self.base_damage

        # Prestige bonuses
        dmg += self.prestige_bonuses.get('permanent_damage', 0)

        # Hybrid class bonus
        hybrid = self.get_hybrid_info()
        if hybrid:
            dmg += hybrid["bonus_damage"]

        if self.weapon:
            dmg += self.weapon.damage
            if self.weapon.enchantment:
                dmg += ENCHANTMENTS.get(self.weapon.enchantment, {}).get("damage", 0)

        dmg += sum(a.damage_bonus for a in self.artifacts)
        if self.active_pet and self.active_pet.bonus_type == "damage":
            dmg += self.active_pet.bonus_amount

        if self.class_name == "Berserker" and self.hp < self.compute_max_hp()/2:
            dmg = int(dmg*1.5)

        # Warlord hybrid bonus
        if self.hybrid_class_name == "Warlord":
            hp_percent = self.hp / self.compute_max_hp()
            if hp_percent < 0.5:
                dmg = int(dmg * (1.0 + (0.5 - hp_percent)))

        if self.stance == Stance.OFFENSIVE:
            dmg = int(dmg * 1.3)
        elif self.stance == Stance.DEFENSIVE:
            dmg = int(dmg * 0.7)

        if "damage_buff" in self.active_buffs:
            dmg += 10

        if self.berserk_mode:
            dmg = int(dmg * 1.4)

        dmg += self.prestige_level * 2

        return dmg

    def compute_defense(self):
        defense = self.defense

        # Prestige bonuses
        defense += self.prestige_bonuses.get('permanent_defense', 0)

        # Skill tree bonus
        defense += get_skill_bonus(self, "Iron Skin")

        # Warlord hybrid bonus
        if self.hybrid_class_name == "Warlord":
            hp_percent = self.hp / self.compute_max_hp()
            if hp_percent < 0.5:
                defense += int(5 * (0.5 - hp_percent) * 10)

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
        hp = self.max_hp

        # Prestige bonuses
        hp += self.prestige_bonuses.get('permanent_hp', 0)

        # Skill tree bonus
        hp += get_skill_bonus(self, "Titan's Endurance")

        # Hybrid class bonus
        hybrid = self.get_hybrid_info()
        if hybrid:
            hp += hybrid["bonus_hp"]

        hp += sum(a.hp_bonus for a in self.artifacts)
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
                class_display = self.hybrid_class_name or self.class_name
                slowprint(f"\n🌟 EVOLUTION! {class_display} → Elite {class_display}")
                self.base_damage += 5
                self.defense += 2
            elif self.level == 20 and self.evolution_stage == 2:
                self.evolution_stage = 3
                class_display = self.hybrid_class_name or self.class_name
                slowprint(f"\n🌟 ULTIMATE EVOLUTION! Elite {class_display} → Master {class_display}")
                self.base_damage += 10
                self.defense += 5
                self.max_hp += 50

    def prestige(self):
        if self.level >= 30:
            self.prestige_level += 1

            # Store prestige bonuses
            if 'permanent_damage' not in self.prestige_bonuses:
                self.prestige_bonuses['permanent_damage'] = 0
            if 'permanent_hp' not in self.prestige_bonuses:
                self.prestige_bonuses['permanent_hp'] = 0
            if 'permanent_defense' not in self.prestige_bonuses:
                self.prestige_bonuses['permanent_defense'] = 0
            if 'crit_bonus' not in self.prestige_bonuses:
                self.prestige_bonuses['crit_bonus'] = 0

            # Add new prestige bonuses
            self.prestige_bonuses['permanent_damage'] += 5
            self.prestige_bonuses['permanent_hp'] += 20
            self.prestige_bonuses['permanent_defense'] += 2
            self.prestige_bonuses['crit_bonus'] += 2

            # Keep hybrid class and abilities
            kept_hybrid = self.hybrid_class_name
            kept_secondary = self.secondary_class
            kept_skills = dict(self.skill_levels)
            kept_achievements = [a for a in self.achievements if a.unlocked]

            # Reset to level 1
            self.level = 1
            self.xp = 0
            self.hp = 100
            self.max_hp = 100
            self.base_damage = 10
            self.defense = 2

            # Restore hybrid class
            self.hybrid_class_name = kept_hybrid
            self.secondary_class = kept_secondary

            # Restore some skill levels (half of what you had)
            for skill, level in kept_skills.items():
                self.skill_levels[skill] = max(1, level // 2)

            # Restore achievements
            self.achievements = kept_achievements + [a for a in self.achievements if not a.unlocked]

            slowprint(f"\n⭐ PRESTIGE {self.prestige_level}! ⭐")
            slowprint("="*50)
            slowprint(f"✨ Permanent Bonuses Gained:")
            slowprint(f"   💪 +{self.prestige_bonuses['permanent_damage']} Total Damage")
            slowprint(f"   ❤️  +{self.prestige_bonuses['permanent_hp']} Total HP")
            slowprint(f"   🛡️  +{self.prestige_bonuses['permanent_defense']} Total Defense")
            slowprint(f"   ⚡ +{self.prestige_bonuses['crit_bonus']}% Crit Chance")
            slowprint(f"\n🔄 Retained:")
            slowprint(f"   • Hybrid Class: {self.hybrid_class_name}")
            slowprint(f"   • Half of your skill levels")
            slowprint(f"   • All achievements")
            slowprint("="*50)
        else:
            slowprint("❌ Must be level 30 to prestige!")
            slowprint(f"   Current level: {self.level}/30")

    def add_multiclass(self, class_name):
        if not self.secondary_class:
            self.secondary_class = class_name
            hybrid = self.get_hybrid_info()
            if hybrid:
                self.hybrid_class_name = hybrid["name"]
                slowprint(f"\n✨ HYBRID CLASS UNLOCKED: {hybrid['name']}!")
                slowprint(f"   Special: {hybrid['special']}")
                slowprint(f"   Bonuses: +{hybrid['bonus_hp']} HP, +{hybrid['bonus_damage']} Damage")
            else:
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
        elif self.class_name == "Paladin":
            abilities.update({
                "Holy Strike": {"cooldown": 3, "desc": "Holy damage", "action": self.ability_holy_strike},
                "Divine Heal": {"cooldown": 5, "desc": "Restore HP", "action": self.ability_divine_heal}
            })
        elif self.class_name == "Necromancer":
            abilities.update({
                "Death Bolt": {"cooldown": 3, "desc": "Dark damage", "action": self.ability_death_bolt},
                "Raise Undead": {"cooldown": 6, "desc": "Summon skeleton", "action": self.ability_raise_undead}
            })
        elif self.class_name == "Monk":
            abilities.update({
                "Chi Strike": {"cooldown": 2, "desc": "Fast combo", "action": self.ability_chi_strike},
                "Inner Peace": {"cooldown": 5, "desc": "Heal & focus", "action": self.ability_inner_peace}
            })
        elif self.class_name == "Ranger":
            abilities.update({
                "Multi-Shot": {"cooldown": 3, "desc": "Hit 2 enemies", "action": self.ability_multishot},
                "Nature's Call": {"cooldown": 5, "desc": "Summon beast", "action": self.ability_natures_call}
            })
        elif self.class_name == "Druid":
            abilities.update({
                "Bear Form": {"cooldown": 4, "desc": "Tank mode", "action": self.ability_bear_form},
                "Rejuvenation": {"cooldown": 4, "desc": "Heal over time", "action": self.ability_rejuvenation}
            })
        elif self.class_name == "Samurai":
            abilities.update({
                "Iaijutsu": {"cooldown": 3, "desc": "Quick draw", "action": self.ability_iaijutsu},
                "Perfect Parry": {"cooldown": 5, "desc": "Counter stance", "action": self.ability_perfect_parry}
            })
        elif self.class_name == "Warlock":
            abilities.update({
                "Eldritch Blast": {"cooldown": 2, "desc": "Dark bolt", "action": self.ability_eldritch_blast},
                "Life Tap": {"cooldown": 4, "desc": "HP to damage", "action": self.ability_life_tap}
            })

        # Add secondary class abilities
        if self.secondary_class:
            if self.secondary_class == "Warrior":
                abilities["Shield Bash"] = {"cooldown": 4, "desc": "Stun", "action": self.ability_shield_bash}
            elif self.secondary_class == "Mage":
                abilities["Fireball"] = {"cooldown": 3, "desc": "Fire dmg", "action": self.ability_fireball}
            elif self.secondary_class == "Rogue":
                abilities["Backstab"] = {"cooldown": 2.5, "desc": "High crit dmg", "action": self.ability_backstab}
            elif self.secondary_class == "Berserker":
                abilities["Rage Strike"] = {"cooldown": 3, "desc": "Berserk dmg", "action": self.ability_rage_strike}
            elif self.secondary_class == "Assassin":
                abilities["Poison Blade"] = {"cooldown": 3, "desc": "Poison", "action": self.ability_poison_blade}

        # Add hybrid-specific abilities
        if self.hybrid_class_name:
            abilities.update(self.get_hybrid_abilities())

        self.abilities = abilities
        for name in self.abilities:
            self.cooldown_timers.setdefault(name, 0.0)
        self.cooldown_timers.setdefault("heal", 0.0)

    def get_hybrid_abilities(self):
        """Get special hybrid abilities"""
        hybrid_abilities = {}

        if self.hybrid_class_name == "Spellblade":
            hybrid_abilities["Arcane Slash"] = {
                "cooldown": 4,
                "desc": "Magic-enhanced strike",
                "action": self.ability_arcane_slash
            }
        elif self.hybrid_class_name == "Blood Mage":
            hybrid_abilities["Blood Sacrifice"] = {
                "cooldown": 5,
                "desc": "HP to damage",
                "action": self.ability_blood_sacrifice
            }
        elif self.hybrid_class_name == "Nightblade":
            hybrid_abilities["Assassinate"] = {
                "cooldown": 6,
                "desc": "Massive critical strike",
                "action": self.ability_assassinate
            }
        elif self.hybrid_class_name == "Reaper":
            hybrid_abilities["Harvest"] = {
                "cooldown": 5,
                "desc": "Kill for berserk extension",
                "action": self.ability_harvest
            }

        return hybrid_abilities

    def ability_power_strike(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage() * 2

        # Duelist bonus
        if self.hybrid_class_name == "Duelist" and check_critical_hit(self):
            dmg = int(dmg * 1.5)
            slowprint("  ⚡ DUELIST CRIT BONUS!")

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

        # Shadowknight bonus
        if self.hybrid_class_name == "Shadowknight" and random.random() < 0.4:
            target['poison'] = target.get('poison', 0) + 2
            slowprint("  ☠️ Shadowknight poison applied!")

        self.total_damage_dealt += dmg
        slowprint(f"🛡️  Shield Bash! {target['name']} stunned for 2 turns!")

    def ability_fireball(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage() + 15

        # Trickster: spells can crit
        if self.hybrid_class_name == "Trickster" and random.random() < 0.25:
            dmg = int(dmg * 2)
            slowprint("  ✨ TRICKSTER SPELL CRIT!")

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
        multiplier = 2.5

        # Duelist: enhanced crits
        if self.hybrid_class_name == "Duelist":
            multiplier = 3.0

        dmg = int(self.compute_damage() * multiplier)
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

        # Ravager: enhanced lifesteal
        if self.hybrid_class_name == "Ravager":
            heal_amt = int(dmg * 0.5)

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

    # Hybrid-specific abilities
    def ability_arcane_slash(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage() * 2
        elements = [Element.FIRE, Element.ICE, Element.LIGHTNING]
        element = random.choice(elements)
        dmg = apply_elemental_damage(dmg, element, target)
        target['hp'] -= dmg
        self.total_damage_dealt += dmg
        slowprint(f"⚔️✨ Arcane Slash! {dmg} {element.value} damage!")

    def ability_blood_sacrifice(self, enemies):
        if self.hp > 30:
            sacrifice = int(self.hp * 0.3)
            self.hp -= sacrifice
            target = enemies[0]
            dmg = self.compute_damage() + (sacrifice * 2)
            target['hp'] -= dmg
            self.total_damage_dealt += dmg
            slowprint(f"🩸 Blood Sacrifice! {sacrifice} HP → {dmg} damage!")

    def ability_assassinate(self, enemies):
        target = enemies[0]
        dmg = int(self.compute_damage() * 4)
        if random.random() < 0.2:
            dmg = target['hp']  # Instant kill
            slowprint("  💀 INSTANT KILL!")
        target['hp'] -= dmg
        self.total_damage_dealt += dmg
        slowprint(f"🗡️💀 Assassinate! {dmg} damage!")

    def ability_harvest(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage() * 2
        target['hp'] -= dmg
        self.total_damage_dealt += dmg
        if target['hp'] <= 0:
            self.berserk_mode = True
            slowprint(f"💀 Harvest! {dmg} damage - BERSERK MODE ACTIVATED!")
        else:
            slowprint(f"💀 Harvest! {dmg} damage!")

    # New class abilities
    def ability_holy_strike(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage() + 10
        dmg = apply_elemental_damage(dmg, Element.HOLY, target)
        target['hp'] -= dmg
        self.heal(5)
        self.total_damage_dealt += dmg
        slowprint(f"✨ Holy Strike! {dmg} damage + healed 5 HP!")

    def ability_divine_heal(self, enemies):
        heal_amt = int(self.compute_max_hp() * 0.4)
        self.heal(heal_amt)
        slowprint(f"🙏 Divine Heal! Restored {heal_amt} HP!")

    def ability_death_bolt(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage() + 12
        dmg = apply_elemental_damage(dmg, Element.DARK, target)
        target['hp'] -= dmg
        self.total_damage_dealt += dmg
        if random.random() < 0.3:
            target['hp'] -= 10
            slowprint(f"💀 Death Bolt! {dmg} damage + 10 curse damage!")
        else:
            slowprint(f"💀 Death Bolt! {dmg} damage!")

    def ability_raise_undead(self, enemies):
        slowprint("💀 Raised a skeleton minion! (Companion for 5 turns)")
        # Simplified - just heal player for now
        self.heal(20)

    def ability_chi_strike(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage()
        for i in range(3):
            target['hp'] -= dmg // 3
            slowprint(f"👊 Chi Strike {i+1}! {dmg // 3} damage!")
        self.total_damage_dealt += dmg

    def ability_inner_peace(self, enemies):
        self.heal(25)
        self.ultimate_charge += 20
        slowprint("🧘 Inner Peace! +25 HP and +20 ultimate charge!")

    def ability_multishot(self, enemies):
        dmg = self.compute_damage()
        targets = enemies[:2]
        for target in targets:
            if target['hp'] > 0:
                target['hp'] -= dmg
                slowprint(f"🏹 Multi-Shot hits {target['name']} for {dmg}!")
        self.total_damage_dealt += dmg * len(targets)

    def ability_natures_call(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage()
        target['hp'] -= dmg
        self.heal(15)
        slowprint(f"🐺 Nature's Call! {dmg} damage + 15 HP healed!")

    def ability_bear_form(self, enemies):
        self.active_buffs['bear_form'] = 3
        self.defense += 10
        slowprint("🐻 Bear Form! +10 defense for 3 turns!")

    def ability_rejuvenation(self, enemies):
        self.active_buffs['rejuvenation'] = 3
        slowprint("🌿 Rejuvenation! Healing 15 HP per turn for 3 turns!")

    def ability_iaijutsu(self, enemies):
        target = enemies[0]
        dmg = int(self.compute_damage() * 2.2)
        target['hp'] -= dmg
        self.total_damage_dealt += dmg
        slowprint(f"⚔️ Iaijutsu! Swift {dmg} damage!")

    def ability_perfect_parry(self, enemies):
        self.active_buffs['perfect_parry'] = 2
        slowprint("🛡️ Perfect Parry stance! Next 2 attacks countered!")

    def ability_eldritch_blast(self, enemies):
        target = enemies[0]
        dmg = self.compute_damage() + 8
        dmg = apply_elemental_damage(dmg, Element.DARK, target)
        target['hp'] -= dmg
        self.total_damage_dealt += dmg
        slowprint(f"👁️ Eldritch Blast! {dmg} dark damage!")

    def ability_life_tap(self, enemies):
        if self.hp > 20:
            sacrifice = 20
            self.hp -= sacrifice
            target = enemies[0]
            dmg = self.compute_damage() + 30
            target['hp'] -= dmg
            self.total_damage_dealt += dmg
            slowprint(f"🩸 Life Tap! Sacrificed {sacrifice} HP for {dmg} damage!")

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

    # Prestige crit bonus
    crit_chance += player.prestige_bonuses.get('crit_bonus', 0) / 100.0

    # Skill tree bonus
    crit_chance += get_skill_bonus(player, "Lucky Strike") / 100.0

    # Duelist bonus
    if player.hybrid_class_name == "Duelist":
        crit_chance += 0.10

    # Ravager bonus
    if player.hybrid_class_name == "Ravager":
        crit_chance += 0.15

    # Nightblade bonus
    if player.hybrid_class_name == "Nightblade":
        crit_chance += 0.20

    crit_chance += player.get_luck_bonus()

    if random.random() < crit_chance:
        player.critical_hits += 1
        return True
    return False

def check_parry(player):
    """Chance to parry an attack"""
    parry_chance = 0.15 if player.stance == Stance.COUNTER else 0.05

    # Nightblade enhanced evasion
    if player.hybrid_class_name == "Nightblade":
        parry_chance += 0.15

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

    # Blood Mage gets extra option
    if player.hybrid_class_name == "Blood Mage":
        slowprint("  3) 30 HP → +20 damage + lifesteal (4 turns) [Blood Mage]")

    slowprint("  4) Back")
    slowprint("╚═════════════════════════════════════╝")

    choice = input("> ").strip()
    if choice == "1" and player.hp > 20:
        player.hp -= 20
        player.active_buffs["damage_buff"] = 3
        player.sacrifices_made += 1
        slowprint("🩸 Sacrificed 20 HP! Damage increased!")
    elif choice == "2" and player.hp > 50:
        player.hp -= 50
        player.active_buffs["damage_buff"] = 5
        player.base_damage += 15
        player.sacrifices_made += 1
        slowprint("🩸 Sacrificed 50 HP! Massive damage boost!")
    elif choice == "3" and player.hybrid_class_name == "Blood Mage" and player.hp > 30:
        player.hp -= 30
        player.active_buffs["damage_buff"] = 4
        player.base_damage += 20
        player.sacrifices_made += 1
        slowprint("🩸💀 BLOOD MAGE SACRIFICE! Damage + Lifesteal!")

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

    slowprint("\n╔════════════ ENCHANTMENTS ════════════╗")
    slowprint("  1) Fire (+5 fire dmg) - 1 Dragon Scale")
    slowprint("  2) Ice (+5 ice dmg) - 2 Frost Crystals")
    slowprint("  3) Lightning (+7 lightning) - 2 Lightning Shards")
    slowprint("  4) Sharpness (+10 dmg) - 3 Iron Ore")
    slowprint("  5) Holy (+6 holy dmg) - 1 Holy Water")
    slowprint("  6) Dark (+6 dark dmg) - 1 Dark Essence")
    slowprint("  7) Lifesteal (15% heal) - 2 Soul Fragments")
    slowprint("  8) Vorpal (+12 dmg, +5% crit) - 1 Dragon Scale + 1 Enchant Scroll")
    slowprint("  9) Back")
    slowprint("╚══════════════════════════════════════╝")

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
    elif choice == "3" and player.materials.get("Lightning Shard", 0) >= 2:
        player.materials["Lightning Shard"] -= 2
        player.gold -= 150
        player.weapon.enchantment = "Lightning"
        slowprint("⚡ Weapon enchanted with Lightning!")
    elif choice == "4" and player.materials.get("Iron Ore", 0) >= 3:
        player.materials["Iron Ore"] -= 3
        player.gold -= 150
        player.weapon.enchantment = "Sharpness"
        slowprint("✨ Weapon enchanted with Sharpness!")
    elif choice == "5" and player.materials.get("Holy Water", 0) >= 1:
        player.materials["Holy Water"] -= 1
        player.gold -= 150
        player.weapon.enchantment = "Holy"
        slowprint("✨ Weapon enchanted with Holy!")
    elif choice == "6" and player.materials.get("Dark Essence", 0) >= 1:
        player.materials["Dark Essence"] -= 1
        player.gold -= 150
        player.weapon.enchantment = "Dark"
        slowprint("💀 Weapon enchanted with Dark!")
    elif choice == "7" and player.materials.get("Soul Fragment", 0) >= 2:
        player.materials["Soul Fragment"] -= 2
        player.gold -= 150
        player.weapon.enchantment = "Lifesteal"
        slowprint("🩸 Weapon enchanted with Lifesteal!")
    elif choice == "8" and player.materials.get("Dragon Scale", 0) >= 1 and player.materials.get("Enchant Scroll", 0) >= 1:
        player.materials["Dragon Scale"] -= 1
        player.materials["Enchant Scroll"] -= 1
        player.gold -= 200
        player.weapon.enchantment = "Vorpal"
        slowprint("⚔️ Weapon enchanted with Vorpal!")

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

def multiclass_trainer(player):
    """Menu for selecting a secondary class"""
    if player.secondary_class:
        slowprint(f"\nYou are already a {player.hybrid_class_name or player.class_name}!")
        return

    slowprint("\n╔════════ MULTICLASS TRAINER ═══════╗")
    slowprint(f"  Current Class: {player.class_name}")
    slowprint(f"  Cost: 500 gold")
    slowprint(f"  Your Gold: {player.gold}")
    slowprint("\n  Choose Secondary Class:")

    classes = ["Warrior", "Mage", "Rogue", "Berserker", "Assassin", "Paladin",
               "Necromancer", "Monk", "Ranger", "Druid", "Samurai", "Warlock"]
    classes = [c for c in classes if c != player.class_name]

    for i, class_name in enumerate(classes, 1):
        # Show potential hybrid
        key1 = (player.class_name, class_name)
        key2 = (class_name, player.class_name)
        hybrid = HYBRID_CLASSES.get(key1) or HYBRID_CLASSES.get(key2)
        if hybrid:
            slowprint(f"  {i:2}) {class_name:<15} → {hybrid['name']}")
        else:
            slowprint(f"  {i:2}) {class_name}")
    slowprint(f"  {len(classes)+1}) Back")
    slowprint("╚═══════════════════════════════════╝")

    choice = input("> ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(classes):
            if player.gold >= 500:
                player.gold -= 500
                player.add_multiclass(classes[idx])
            else:
                slowprint("Not enough gold!")

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
        slowprint("😔 You lose!")

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
        slowprint(f"🎊 JACKPOT! Won {winnings} gold!")
    else:
        slowprint("😔 Wrong suit!")

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
            slowprint(f"💎 Diamond win! {winnings} gold!")
        else:
            winnings = 150
            slowprint(f"🎉 Three of a kind! {winnings} gold!")
        player.gold += winnings
    elif result[0] == result[1] or result[1] == result[2]:
        winnings = 75
        player.gold += winnings
        slowprint(f"Two match! Won {winnings} gold!")
    else:
        slowprint("😔 No match!")

def init_achievements(player):
    achievements = [
        Achievement("ach_kills_10", "Slayer", "Defeat 10 enemies", "total_kills", 10, False, "50 gold"),
        Achievement("ach_kills_50", "Veteran", "Defeat 50 enemies", "total_kills", 50, False, "200 gold"),
        Achievement("ach_boss_1", "Boss Hunter", "Defeat first boss", "bosses", 1, False, "Epic Artifact"),
        Achievement("ach_crit_10", "Critical Master", "Land 10 crits", "crits", 10, False, "+5% crit chance"),
        Achievement("ach_parry_5", "Parry God", "Perfect parry 5 times", "parries", 5, False, "Counter stance unlocked"),
        Achievement("ach_prestige", "Reborn", "Reach prestige 1", "prestige", 1, False, "Legendary weapon"),
        Achievement("ach_hybrid", "Hybrid Warrior", "Unlock hybrid class", "hybrid", 1, False, "100 gold"),
    ]
    player.achievements = achievements

def check_achievements(player):
    total_kills = sum(player.kills.values())

    for ach in player.achievements:
        if not ach.unlocked:
            if ach.requirement_type == "total_kills" and total_kills >= ach.requirement_value:
                ach.unlocked = True
                slowprint(f"\n🏆 ACHIEVEMENT UNLOCKED: {ach.name}!")
                slowprint(f"   {ach.description}")
                slowprint(f"   Reward: {ach.reward}")
                if "gold" in ach.reward:
                    amount = int(ach.reward.split()[0])
                    player.gold += amount
            elif ach.requirement_type == "bosses" and player.bosses_defeated >= ach.requirement_value:
                ach.unlocked = True
                slowprint(f"\n🏆 ACHIEVEMENT: {ach.name}!")
            elif ach.requirement_type == "crits" and player.critical_hits >= ach.requirement_value:
                ach.unlocked = True
                slowprint(f"\n🏆 ACHIEVEMENT: {ach.name}!")
            elif ach.requirement_type == "hybrid" and player.hybrid_class_name:
                ach.unlocked = True
                slowprint(f"\n🏆 ACHIEVEMENT: {ach.name}!")
                player.gold += 100

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
            slowprint(f"\n💰 BOUNTY COMPLETED! Earned {bounty.reward} gold!")

def talent_menu(player):
    """Enhanced skill tree with multiple levels per skill"""

    # Define all available skills with max levels
    SKILL_TREE = {
        "Whirlwind Strike": {
            "max_level": 5,
            "base_cost": 1,
            "desc": "AOE attack hitting all enemies",
            "scaling": lambda lvl: f"Damage: {100 + (lvl * 20)}% | Targets: All"
        },
        "Life Drain": {
            "max_level": 5,
            "base_cost": 1,
            "desc": "Heal based on damage dealt",
            "scaling": lambda lvl: f"Lifesteal: {10 + (lvl * 5)}%"
        },
        "Berserker Rage": {
            "max_level": 3,
            "base_cost": 2,
            "desc": "Boost damage when low HP",
            "scaling": lambda lvl: f"Damage: +{20 + (lvl * 15)}% when HP < 50%"
        },
        "Shadow Clone": {
            "max_level": 3,
            "base_cost": 2,
            "desc": "Summon a copy to fight",
            "scaling": lambda lvl: f"Clone Power: {30 + (lvl * 20)}% | Duration: {lvl + 2} turns"
        },
        "Iron Skin": {
            "max_level": 5,
            "base_cost": 1,
            "desc": "Permanent defense boost",
            "scaling": lambda lvl: f"Defense: +{2 + (lvl * 2)}"
        },
        "Swift Strike": {
            "max_level": 5,
            "base_cost": 1,
            "desc": "Reduce ability cooldowns",
            "scaling": lambda lvl: f"Cooldown: -{5 + (lvl * 5)}%"
        },
        "Elemental Mastery": {
            "max_level": 3,
            "base_cost": 2,
            "desc": "Boost elemental damage",
            "scaling": lambda lvl: f"Elemental Damage: +{15 + (lvl * 10)}%"
        },
        "Battle Trance": {
            "max_level": 4,
            "base_cost": 1,
            "desc": "Gain HP per kill",
            "scaling": lambda lvl: f"HP per kill: {10 + (lvl * 8)}"
        },
        "Lucky Strike": {
            "max_level": 5,
            "base_cost": 1,
            "desc": "Increase critical hit chance",
            "scaling": lambda lvl: f"Crit Chance: +{3 + (lvl * 2)}%"
        },
        "Titan's Endurance": {
            "max_level": 5,
            "base_cost": 1,
            "desc": "Permanent HP boost",
            "scaling": lambda lvl: f"Max HP: +{15 + (lvl * 10)}"
        }
    }

    while True:
        slowprint(f"\n╔{'═'*60}╗")
        slowprint(f"║{'SKILL TREE':^60}║")
        slowprint(f"║{f'Skill Points Available: {player.skill_points}':^60}║")
        slowprint(f"╠{'═'*60}╣")

        skills_list = list(SKILL_TREE.items())
        for i, (skill_name, skill_info) in enumerate(skills_list, 1):
            current_level = player.skill_levels.get(skill_name, 0)
            max_level = skill_info["max_level"]
            cost = skill_info["base_cost"]

            # Show level progress
            level_bar = "█" * current_level + "░" * (max_level - current_level)
            status = f"[{level_bar}] {current_level}/{max_level}"

            # Show current and next level stats
            if current_level < max_level:
                next_level = current_level + 1
                scaling_text = skill_info["scaling"](next_level)
                cost_text = f"Cost: {cost}"
                slowprint(f"║ {i:2}) {skill_name:<20} {status:<15} {cost_text:<10}║")
                slowprint(f"║     {skill_info['desc']:<55}║")
                slowprint(f"║     Next: {scaling_text:<50}║")
            else:
                slowprint(f"║ {i:2}) {skill_name:<20} {status:<15} ✓ MAXED    ║")
                scaling_text = skill_info["scaling"](current_level)
                slowprint(f"║     {scaling_text:<55}║")

            slowprint(f"╠{'─'*60}╣")

        slowprint(f"║ {len(skills_list)+1:2}) View Stats                                              ║")
        slowprint(f"║ {len(skills_list)+2:2}) Save Points & Exit                                       ║")
        slowprint(f"╚{'═'*60}╝")

        choice = input("> ").strip()

        if choice == str(len(skills_list)+1):
            show_skill_stats(player, SKILL_TREE)
            continue
        elif choice == str(len(skills_list)+2):
            break
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(skills_list):
                skill_name = skills_list[idx][0]
                skill_info = skills_list[idx][1]
                current_level = player.skill_levels.get(skill_name, 0)

                if current_level >= skill_info["max_level"]:
                    slowprint(f"❌ {skill_name} is already maxed!")
                    input("Press Enter...")
                elif player.skill_points >= skill_info["base_cost"]:
                    player.skill_points -= skill_info["base_cost"]
                    player.skill_levels[skill_name] = current_level + 1
                    apply_skill_bonus(player, skill_name, player.skill_levels[skill_name])
                    slowprint(f"✨ {skill_name} leveled up to {player.skill_levels[skill_name]}!")
                    input("Press Enter...")
                else:
                    slowprint(f"❌ Not enough skill points! Need {skill_info['base_cost']}")
                    input("Press Enter...")

def show_skill_stats(player, skill_tree):
    """Show all active skill bonuses"""
    slowprint(f"\n╔{'═'*50}╗")
    slowprint(f"║{'ACTIVE SKILL BONUSES':^50}║")
    slowprint(f"╠{'═'*50}╣")

    if not player.skill_levels:
        slowprint(f"║{'No skills learned yet':^50}║")
    else:
        for skill_name, level in player.skill_levels.items():
            if level > 0:
                scaling = skill_tree[skill_name]["scaling"](level)
                slowprint(f"║ {skill_name:<25} Lv.{level:<2} {'':<20}║")
                slowprint(f"║   → {scaling:<45}║")

    slowprint(f"╚{'═'*50}╝")
    input("Press Enter...")

def apply_skill_bonus(player, skill_name, level):
    """Apply the passive bonuses from skills"""
    if skill_name == "Iron Skin":
        # Already tracked in skill_levels, applied in compute_defense
        pass
    elif skill_name == "Titan's Endurance":
        # Already tracked in skill_levels, applied in compute_max_hp
        player.hp = min(player.hp, player.compute_max_hp())
    elif skill_name == "Lucky Strike":
        # Applied in check_critical_hit
        pass
    # Other skills are applied when their effects trigger

def get_skill_bonus(player, skill_name):
    """Get the current bonus from a skill"""
    level = player.skill_levels.get(skill_name, 0)
    if level == 0:
        return 0

    bonuses = {
        "Whirlwind Strike": 20 * level,  # % damage per level
        "Life Drain": 5 * level,  # % lifesteal per level
        "Berserker Rage": 15 * level,  # % damage bonus per level
        "Shadow Clone": 20 * level,  # % clone power per level
        "Iron Skin": 2 * level + 2,  # flat defense per level
        "Swift Strike": 5 * level,  # % cooldown reduction per level
        "Elemental Mastery": 10 * level,  # % elemental damage per level
        "Battle Trance": 8 * level,  # HP per kill per level
        "Lucky Strike": 2 * level,  # % crit chance per level
        "Titan's Endurance": 10 * level + 15,  # flat HP per level
    }

    return bonuses.get(skill_name, 0)

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
        enemy['cursed'] = False

    turn = 0

    while any(e['hp'] > 0 for e in enemies) and player.hp > 0:
        turn += 1
        slowprint(f"\n{'─'*50}")
        slowprint(f"Turn {turn} | Stance: {player.stance.value}")

        class_display = player.hybrid_class_name or player.class_name
        slowprint(f"{player.name} ({class_display}) HP:{player.hp}/{player.compute_max_hp()} | Ultimate:{player.ultimate_charge}/{player.ultimate_max}")

        for i, enemy in enumerate(enemies, 1):
            if enemy['hp'] > 0:
                status = ""
                if enemy.get('cursed'):
                    status = " [CURSED]"
                slowprint(f"  [{i}] {enemy['name']} HP:{enemy['hp']}/{enemy['max_hp']}{status}")

        for comp in player.active_companions:
            if comp.hp > 0 and enemies:
                alive_enemies = [e for e in enemies if e['hp'] > 0]
                if alive_enemies:
                    target = alive_enemies[0]
                    dmg = comp.damage
                    target['hp'] -= dmg
                    slowprint(f"🤝 {comp.name} attacks {target['name']} for {dmg}!")

        # ── INITIATIVE ROLL ──────────────────────────────────────────────────
        # 35% chance enemies ambush the player and attack BEFORE they can act.
        # Bosses are more aggressive: 50% chance to go first.
        initiative_threshold = 0.50 if is_boss else 0.35
        enemy_goes_first = random.random() < initiative_threshold

        if enemy_goes_first and any(e['hp'] > 0 for e in enemies):
            slowprint(f"\n⚡ {'BOSS' if is_boss else 'Enemies'} strike first!")
            for enemy in enemies:
                if enemy['hp'] > 0 and player.hp > 0:
                    if enemy['stunned'] > 0:
                        enemy['stunned'] -= 1
                        slowprint(f"😵 {enemy['name']} is stunned — can't act!")
                        continue
                    # Parry check still applies
                    if check_parry(player) or 'perfect_parry' in player.active_buffs:
                        slowprint(f"  🛡️ PERFECT PARRY! You counter {enemy['name']}!")
                        counter_dmg = player.compute_damage()
                        if 'perfect_parry' in player.active_buffs:
                            counter_dmg = int(counter_dmg * 1.5)
                        enemy['hp'] -= counter_dmg
                        slowprint(f"   ⚔️ Counter strike: {counter_dmg} damage!")
                        continue
                    # Dodge check
                    if player.cheat_flags.get("dodge_next"):
                        player.cheat_flags["dodge_next"] = False
                        slowprint(f"💨 You dodge {enemy['name']}'s early attack!")
                        continue
                    dmg = enemy.get('atk', 10)
                    if enemy.get('cursed'):
                        dmg = int(dmg * 0.7)
                        slowprint("  🌑 Curse weakens the attack!")
                    dmg = max(0, dmg - player.compute_defense())
                    if player.cheat_flags.get("hehe", False):
                        player.hp = 9999
                    else:
                        player.hp -= dmg
                    if dmg > 0:
                        slowprint(f"💢 {enemy['name']} hits you for {dmg}! (ambush)")
            if player.hp <= 0:
                break
        else:
            slowprint("\n✅ You have the initiative this turn!")
        # ────────────────────────────────────────────────────────────────────

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

            is_crit = check_critical_hit(player)
            if is_crit:
                crit_mult = 2
                # Duelist enhanced crit
                if player.hybrid_class_name == "Duelist":
                    crit_mult = 3
                # Nightblade enhanced crit
                if player.hybrid_class_name == "Nightblade":
                    crit_mult = 3.5
                dmg = int(dmg * crit_mult)
                slowprint("⚡ CRITICAL HIT!")

            element = player.weapon.element if player.weapon else Element.PHYSICAL
            dmg = apply_weather_effects(weather, dmg, element)
            dmg = apply_elemental_damage(dmg, element, target)

            # Berserker Rage skill bonus
            if player.hp < player.compute_max_hp() / 2:
                rage_bonus = get_skill_bonus(player, "Berserker Rage")
                if rage_bonus > 0:
                    dmg = int(dmg * (1 + rage_bonus / 100))
                    slowprint(f"  😡 Berserker Rage: +{rage_bonus}% damage!")

            # Elemental Mastery skill bonus
            if element != Element.PHYSICAL:
                elem_bonus = get_skill_bonus(player, "Elemental Mastery")
                if elem_bonus > 0:
                    dmg = int(dmg * (1 + elem_bonus / 100))
                    slowprint(f"  ✨ Elemental Mastery: +{elem_bonus}% damage!")

            # Spellblade bonus
            if player.hybrid_class_name == "Spellblade" and player.weapon and player.weapon.element != Element.PHYSICAL:
                bonus = int(dmg * 0.2)
                dmg += bonus
                slowprint(f"  ⚔️✨ Spellblade bonus: +{bonus} elemental damage!")

            # Shadowknight chance
            if player.hybrid_class_name == "Shadowknight" and random.random() < 0.3:
                target['poison'] = target.get('poison', 0) + 2
                target['stunned'] = 1
                slowprint("  ⚔️🌑 Shadowknight: Poison + Stun!")

            # Hexblade curse
            if player.hybrid_class_name == "Hexblade" and random.random() < 0.4:
                target['cursed'] = True
                slowprint("  🌑 Hexblade curse applied!")

            target['hp'] -= dmg
            player.total_damage_dealt += dmg
            player.ultimate_charge += 5
            slowprint(f"  💥 {dmg} damage to {target['name']}!")

            # Life Drain skill bonus
            lifedrain_bonus = get_skill_bonus(player, "Life Drain")
            if lifedrain_bonus > 0:
                heal = int(dmg * (lifedrain_bonus / 100))
                player.heal(heal)
                slowprint(f"  💚 Life Drain: +{heal} HP!")

            # Ravager lifesteal
            if player.hybrid_class_name == "Ravager" and is_crit:
                heal = int(dmg * 0.3)
                player.heal(heal)
                slowprint(f"  🩸 Ravager lifesteal: +{heal} HP!")

            # Battle Trance - HP on kill
            if target['hp'] <= 0:
                trance_bonus = get_skill_bonus(player, "Battle Trance")
                if trance_bonus > 0:
                    player.heal(trance_bonus)
                    slowprint(f"  ⚔️ Battle Trance: +{trance_bonus} HP!")

            # Check for legendary weapon effects
            if player.weapon and player.weapon.is_legendary:
                if "Heals" in player.weapon.legendary_effect and target['hp'] <= 0:
                    heal_amt = int(player.compute_max_hp() * 0.1)
                    player.heal(heal_amt)
                    slowprint(f"   ⚔️ {player.weapon.name} heals {heal_amt} HP!")

            # Reaper harvest check
            if player.hybrid_class_name == "Reaper" and target['hp'] <= 0:
                player.berserk_mode = True
                slowprint("  💀 REAPER HARVEST! Berserk mode extended!")

        elif choice == "2":
            use_ability(player, alive_enemies)

        elif choice == "3":
            use_item(player)

        if all(e['hp'] <= 0 for e in enemies):
            break

        # Enemy turn (only fires if enemies did NOT already go first this turn)
        if not enemy_goes_first:
            for enemy in enemies:
                if enemy['hp'] > 0:
                    if enemy['stunned'] > 0:
                        enemy['stunned'] -= 1
                        slowprint(f"😵 {enemy['name']} is stunned!")
                        continue

                    if check_parry(player) or 'perfect_parry' in player.active_buffs:
                        slowprint(f"  🛡️ PERFECT PARRY! Countered {enemy['name']}!")
                        counter_dmg = player.compute_damage()
                        if 'perfect_parry' in player.active_buffs:
                            counter_dmg = int(counter_dmg * 1.5)
                        enemy['hp'] -= counter_dmg
                        slowprint(f"   ⚔️ Counter: {counter_dmg} damage!")
                        continue

                    dmg = enemy.get('atk', 10)

                    # Hexblade curse effect
                    if enemy.get('cursed'):
                        dmg = int(dmg * 0.7)
                        slowprint("  🌑 Curse weakens attack!")

                    dmg = max(0, dmg - player.compute_defense())
                    player.hp -= dmg
                    if dmg > 0:
                        slowprint(f"💢 {enemy['name']} hits for {dmg}!")

        # Status effects
        for enemy in enemies:
            if enemy.get('poison', 0) > 0:
                enemy['hp'] -= 5
                enemy['poison'] -= 1
                slowprint(f"  ☠️ {enemy['name']} takes poison damage!")
            if enemy.get('burning', 0) > 0:
                enemy['hp'] -= 7
                enemy['burning'] -= 1
                slowprint(f"  🔥 {enemy['name']} takes burn damage!")

        # Cooldowns
        for key in player.cooldown_timers:
            if player.cooldown_timers[key] > 0:
                reduction = 1.0
                # Swift Strike skill bonus
                swift_bonus = get_skill_bonus(player, "Swift Strike")
                if swift_bonus > 0:
                    reduction = 1.0 + (swift_bonus / 100)
                player.cooldown_timers[key] -= reduction

        # Buffs
        for buff in list(player.active_buffs.keys()):
            player.active_buffs[buff] -= 1
            if player.active_buffs[buff] <= 0:
                if buff == 'bear_form':
                    player.defense -= 10
                del player.active_buffs[buff]

        # Rejuvenation healing
        if 'rejuvenation' in player.active_buffs:
            player.heal(15)
            slowprint("  🌿 Rejuvenation heals 15 HP!")

    if player.hp > 0:
        slowprint("\n🎉 VICTORY!")

        total_gold = 0
        total_xp = 0

        for enemy in enemies:
            player.kills[enemy['name']] = player.kills.get(enemy['name'], 0) + 1

            gold = random.randint(20, 50) * (2 if enemy.get('boss') else 1)
            total_gold += gold
            total_xp += 50 if enemy.get('boss') else 20

            if enemy.get('boss'):
                player.bosses_defeated += 1

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
    slowprint(f"⚔️ Stance: {player.stance.value}")

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
    slowprint("\n✨ Abilities:")
    for i, ability in enumerate(abilities, 1):
        cd = player.cooldown_timers.get(ability, 0)
        status = f"CD: {cd}" if cd > 0 else "✓ Ready"
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
    slowprint("        ✨ NOW WITH HYBRID CLASSES! ✨")
    slowprint("="*60)

    name = input("\nHero name: ").strip() or "Hero"

    slowprint("\nChoose class:")
    slowprint("=" * 60)
    slowprint("1) Warrior - Tank with high HP and defense")
    slowprint("2) Mage - High magic damage, elemental master")
    slowprint("3) Rogue - Fast attacks, high crit chance")
    slowprint("4) Berserker - High risk, high reward damage")
    slowprint("5) Assassin - Poison master, stealth attacks")
    slowprint("6) Paladin - Holy warrior, healing and defense")
    slowprint("7) Necromancer - Dark magic, summon undead")
    slowprint("8) Monk - Martial arts, chi energy")
    slowprint("9) Ranger - Nature magic, beast companion")
    slowprint("10) Druid - Shapeshifter, nature spells")
    slowprint("11) Samurai - Honorable warrior, counter attacks")
    slowprint("12) Warlock - Demon pacts, cursed magic")
    slowprint("=" * 60)

    choice = input("> ").strip()
    player = Player(name=name)

    if choice == "1":
        player.class_name = "Warrior"
        player.max_hp += 30
        player.hp = player.max_hp
        player.base_damage += 3
        player.defense += 2
    elif choice == "2":
        player.class_name = "Mage"
        player.base_damage += 12
        player.max_hp -= 10
    elif choice == "3":
        player.class_name = "Rogue"
        player.base_damage += 5
        player.max_hp -= 5
    elif choice == "4":
        player.class_name = "Berserker"
        player.base_damage += 8
        player.max_hp += 10
    elif choice == "5":
        player.class_name = "Assassin"
        player.base_damage += 6
        player.max_hp -= 10
    elif choice == "6":
        player.class_name = "Paladin"
        player.max_hp += 25
        player.base_damage += 4
        player.defense += 3
    elif choice == "7":
        player.class_name = "Necromancer"
        player.base_damage += 10
        player.max_hp -= 5
    elif choice == "8":
        player.class_name = "Monk"
        player.base_damage += 7
        player.defense += 2
        player.max_hp += 5
    elif choice == "9":
        player.class_name = "Ranger"
        player.base_damage += 6
        player.max_hp += 10
    elif choice == "10":
        player.class_name = "Druid"
        player.base_damage += 5
        player.max_hp += 15
        player.defense += 1
    elif choice == "11":
        player.class_name = "Samurai"
        player.base_damage += 8
        player.max_hp += 15
        player.defense += 2
    elif choice == "12":
        player.class_name = "Warlock"
        player.base_damage += 11
        player.max_hp -= 5

    player.weapon = WEAPONS["Rusty Sword"]
    player.init_class_abilities()
    init_achievements(player)
    init_bounties(player)

    player.consumables["Health Potion"] = 3

    slowprint(f"\n✨ {name} the {player.class_name} is ready!")
    slowprint("\n💡 TIP: Visit the Multiclass Trainer in town to unlock hybrid classes!")
    return player

def prestige_menu(player):
    """Menu for prestiging and viewing prestige benefits"""
    slowprint(f"\n╔{'═'*60}╗")
    slowprint(f"║{'PRESTIGE SYSTEM':^60}║")
    slowprint(f"╠{'═'*60}╣")
    slowprint(f"║ Current Prestige Level: {player.prestige_level:<39}║")
    slowprint(f"║ Current Character Level: {player.level}/30{'':<36}║")
    slowprint(f"╠{'═'*60}╣")

    if player.prestige_level > 0:
        slowprint(f"║{'CURRENT PRESTIGE BONUSES':^60}║")
        slowprint(f"║ 💪 Damage: +{player.prestige_bonuses.get('permanent_damage', 0):<48}║")
        slowprint(f"║ ❤️  Max HP: +{player.prestige_bonuses.get('permanent_hp', 0):<49}║")
        slowprint(f"║ 🛡️  Defense: +{player.prestige_bonuses.get('permanent_defense', 0):<47}║")
        slowprint(f"║ ⚡ Crit Chance: +{player.prestige_bonuses.get('crit_bonus', 0)}%{'':<43}║")
        slowprint(f"╠{'═'*60}╣")

    slowprint(f"║{'PRESTIGE BENEFITS':^60}║")
    slowprint(f"║ • Gain permanent stat bonuses{'':<31}║")
    slowprint(f"║ • Keep your hybrid class{'':<36}║")
    slowprint(f"║ • Keep half your skill levels{'':<31}║")
    slowprint(f"║ • Keep all achievements{'':<36}║")
    slowprint(f"║ • Reset to level 1 with boosted growth{'':<23}║")
    slowprint(f"╠{'═'*60}╣")

    if player.level >= 30:
        slowprint(f"║ 1) ⭐ PRESTIGE NOW! ⭐{'':<37}║")
        slowprint(f"║    Gain: +5 dmg, +20 HP, +2 def, +2% crit{'':<19}║")
    else:
        needed = 30 - player.level
        slowprint(f"║ Prestige available at level 30 ({needed} levels to go){'':<15}║")

    slowprint(f"║ 2) Back to Town{'':<45}║")
    slowprint(f"╚{'═'*60}╝")

    choice = input("> ").strip()

    if choice == "1" and player.level >= 30:
        slowprint("\n⚠️  WARNING: You will reset to level 1!")
        confirm = input("Type 'PRESTIGE' to confirm: ").strip()
        if confirm == "PRESTIGE":
            player.prestige()
        else:
            slowprint("Prestige cancelled.")
        input("Press Enter...")

def main():
    player = character_creation()
    battle_count = 0

    regular_enemies = [
        # Basic enemies
        {"name": "Goblin", "hp": 50, "max_hp": 50, "atk": 8, "element": Element.PHYSICAL},
        {"name": "Wolf", "hp": 45, "max_hp": 45, "atk": 12, "element": Element.PHYSICAL},
        {"name": "Skeleton", "hp": 60, "max_hp": 60, "atk": 7, "element": Element.DARK},
        {"name": "Ogre", "hp": 80, "max_hp": 80, "atk": 15, "element": Element.PHYSICAL},

        # Elemental enemies
        {"name": "Fire Elemental", "hp": 55, "max_hp": 55, "atk": 14, "element": Element.FIRE,
         "weakness": Element.ICE, "resistance": Element.FIRE},
        {"name": "Ice Wraith", "hp": 58, "max_hp": 58, "atk": 13, "element": Element.ICE,
         "weakness": Element.FIRE, "resistance": Element.ICE},
        {"name": "Storm Spirit", "hp": 52, "max_hp": 52, "atk": 16, "element": Element.LIGHTNING,
         "weakness": Element.PHYSICAL, "resistance": Element.LIGHTNING},
        {"name": "Shadow Beast", "hp": 65, "max_hp": 65, "atk": 11, "element": Element.DARK,
         "weakness": Element.HOLY, "resistance": Element.DARK},

        # Undead
        {"name": "Zombie", "hp": 70, "max_hp": 70, "atk": 9, "element": Element.DARK,
         "weakness": Element.HOLY, "resistance": Element.POISON},
        {"name": "Ghoul", "hp": 62, "max_hp": 62, "atk": 13, "element": Element.DARK,
         "weakness": Element.HOLY, "resistance": Element.DARK},
        {"name": "Wraith", "hp": 48, "max_hp": 48, "atk": 15, "element": Element.DARK,
         "weakness": Element.HOLY},
        {"name": "Death Knight", "hp": 85, "max_hp": 85, "atk": 17, "element": Element.DARK,
         "weakness": Element.HOLY, "resistance": Element.PHYSICAL},

        # Beasts
        {"name": "Dire Wolf", "hp": 65, "max_hp": 65, "atk": 14, "element": Element.PHYSICAL},
        {"name": "Giant Spider", "hp": 55, "max_hp": 55, "atk": 11, "element": Element.POISON},
        {"name": "Grizzly Bear", "hp": 90, "max_hp": 90, "atk": 16, "element": Element.PHYSICAL},
        {"name": "Wyvern", "hp": 75, "max_hp": 75, "atk": 18, "element": Element.FIRE},

        # Demons
        {"name": "Imp", "hp": 40, "max_hp": 40, "atk": 10, "element": Element.FIRE},
        {"name": "Hellhound", "hp": 68, "max_hp": 68, "atk": 15, "element": Element.FIRE,
         "resistance": Element.FIRE},
        {"name": "Demon Warrior", "hp": 82, "max_hp": 82, "atk": 19, "element": Element.DARK},

        # Constructs
        {"name": "Golem", "hp": 95, "max_hp": 95, "atk": 13, "element": Element.PHYSICAL,
         "resistance": Element.PHYSICAL},
        {"name": "Gargoyle", "hp": 72, "max_hp": 72, "atk": 14, "element": Element.PHYSICAL},

        # Magic users
        {"name": "Dark Mage", "hp": 50, "max_hp": 50, "atk": 20, "element": Element.DARK},
        {"name": "Cultist", "hp": 45, "max_hp": 45, "atk": 12, "element": Element.DARK},
        {"name": "Warlock", "hp": 58, "max_hp": 58, "atk": 18, "element": Element.DARK},
    ]

    bosses = [
        # Original bosses
        {"name": "Dragon", "hp": 200, "max_hp": 200, "atk": 25, "boss": True, "element": Element.FIRE,
         "weakness": Element.ICE, "resistance": Element.FIRE},
        {"name": "Lich King", "hp": 180, "max_hp": 180, "atk": 22, "boss": True, "element": Element.DARK,
         "weakness": Element.HOLY, "resistance": Element.DARK},

        # New bosses
        {"name": "Frost Titan", "hp": 220, "max_hp": 220, "atk": 28, "boss": True, "element": Element.ICE,
         "weakness": Element.FIRE, "resistance": Element.ICE},
        {"name": "Storm Lord", "hp": 190, "max_hp": 190, "atk": 30, "boss": True, "element": Element.LIGHTNING,
         "weakness": Element.PHYSICAL, "resistance": Element.LIGHTNING},
        {"name": "Demon Prince", "hp": 210, "max_hp": 210, "atk": 27, "boss": True, "element": Element.DARK,
         "weakness": Element.HOLY, "resistance": Element.FIRE},
        {"name": "Void Leviathan", "hp": 250, "max_hp": 250, "atk": 32, "boss": True, "element": Element.DARK,
         "weakness": Element.HOLY, "resistance": Element.DARK},
        {"name": "Phoenix King", "hp": 195, "max_hp": 195, "atk": 29, "boss": True, "element": Element.FIRE,
         "weakness": Element.ICE, "resistance": Element.FIRE},
        {"name": "Ancient Hydra", "hp": 240, "max_hp": 240, "atk": 26, "boss": True, "element": Element.POISON,
         "weakness": Element.FIRE, "resistance": Element.POISON},
        {"name": "Celestial Guardian", "hp": 205, "max_hp": 205, "atk": 24, "boss": True, "element": Element.HOLY,
         "weakness": Element.DARK, "resistance": Element.HOLY},
        {"name": "Shadow Dragon", "hp": 230, "max_hp": 230, "atk": 31, "boss": True, "element": Element.DARK,
         "weakness": Element.HOLY, "resistance": Element.DARK},
        {"name": "Kraken", "hp": 215, "max_hp": 215, "atk": 28, "boss": True, "element": Element.ICE,
         "weakness": Element.LIGHTNING, "resistance": Element.ICE},
        {"name": "Golem King", "hp": 260, "max_hp": 260, "atk": 23, "boss": True, "element": Element.PHYSICAL,
         "weakness": Element.LIGHTNING, "resistance": Element.PHYSICAL},
        {"name": "Necromancer Lord", "hp": 185, "max_hp": 185, "atk": 26, "boss": True, "element": Element.DARK,
         "weakness": Element.HOLY, "resistance": Element.DARK},
        {"name": "Crimson Behemoth", "hp": 270, "max_hp": 270, "atk": 30, "boss": True, "element": Element.FIRE,
         "weakness": Element.ICE, "resistance": Element.FIRE},
        {"name": "Arch Demon", "hp": 235, "max_hp": 235, "atk": 33, "boss": True, "element": Element.DARK,
         "weakness": Element.HOLY, "resistance": Element.FIRE},
        {"name": "Elder Wyrm", "hp": 245, "max_hp": 245, "atk": 29, "boss": True, "element": Element.POISON,
         "weakness": Element.HOLY, "resistance": Element.POISON},

        # Ultra bosses (rare)
        {"name": "Primordial Chaos", "hp": 300, "max_hp": 300, "atk": 35, "boss": True, "element": Element.DARK,
         "weakness": Element.HOLY},
        {"name": "World Eater", "hp": 320, "max_hp": 320, "atk": 38, "boss": True, "element": Element.PHYSICAL},
        {"name": "Death Itself", "hp": 280, "max_hp": 280, "atk": 40, "boss": True, "element": Element.DARK,
         "weakness": Element.HOLY, "resistance": Element.DARK},
    ]

    while player.hp > 0:
        battle_count += 1
        weather = get_current_weather()

        slowprint("\n╔═══════════ TOWN ════════════╗")
        slowprint("  1) Next Battle")
        slowprint("  2) Blacksmith")
        slowprint("  3) Potion Shop")
        slowprint("  4) Weapon Shop")
        slowprint("  5) Gambling Den")
        slowprint("  6) Bounty Board")
        slowprint("  7) Recruit Companion")
        slowprint("  8) Skill Tree 🌟")
        slowprint("  9) Hostel (Full heal)")
        slowprint(" 10) Multiclass Trainer ✨")
        slowprint(" 11) Prestige System ⭐")
        slowprint("╚═════════════════════════════╝")

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
        elif choice == "10":
            multiclass_trainer(player)
            continue
        elif choice == "11":
            prestige_menu(player)
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
            if player.hybrid_class_name:
                slowprint(f"Class: {player.hybrid_class_name}")
            slowprint(f"Total Kills: {sum(player.kills.values())}")
            slowprint(f"Gold Earned: {player.gold}")
            break

if __name__ == "__main__":
    main()
