from dataclasses import dataclass, field
from typing import ClassVar
from functools import lru_cache

@dataclass
class SubStats: 
    """ 
    Object for storing and updating substat data 
    """

    level: int = 1
    exp: int = 0
    training_zone: str = ""
    name: str = ""

    def add_exp(self, exp):
        """
        Adds exp to the existing exp attribute
        Checks if exp has reached past level requirement
        
        Parameters:
        exp (int): total exp to be added to this object
        """

        self.exp += exp
        self.check_and_level_up()

    def check_and_level_up(self):
        """
        Calculates the exp required for leveling up
        If current exp meets this criteria, increments level and removes exp from the current amount

        If substat can still be leveled up with remaining exp, continue in the loop until it can no longer
        """
        while True:
            exp_req = self.compute_exp_requirement(self.level)
            if self.exp >= exp_req:
                self.exp -= exp_req
                self.level += 1
            else:
                break

    @staticmethod # allows for the absence of "self" in parameters
    @lru_cache(maxsize=None) # save computational space for duplicated argument values
    def compute_exp_requirement(level):
        """
        Computes the exp requirement for a given level
        Formula uses different values for levels 1-99 and levels 100+

        Exp requirements rise faster after level 100

        Parameters:
        level (int)

        Returns:
        Calculated integer exp requirement for the given argument value

        """

        b = (level - 1) // 100
        i = (level - 1) % 100
        if b == 0:
            start_exp = 10
            end_exp = 50000
        else:
            start_exp = 50000 * (250 ** (b - 1))
            end_exp = 50000 * (250 ** b)
        return start_exp + ((i / 99) ** 2) * (end_exp - start_exp) 



# Objects for storing all data on stats, this includes its level and the data on its substats

@dataclass
class StrengthStats():
    """ 
    Object for storing data on player strength and their individual substats
    """

    strength: int =  1 # base level
    substat_names: ClassVar[list[str]] = [
            "Core Strength",
            "Upper body",
            "Grip",
            "Lower body",
        ] # Used for UI display
    
    core_strength: SubStats = field(default_factory=SubStats(name="Core Strength")) 
    upper_body_strength: SubStats = field(default_factory=SubStats(name="Upper Body Strength"))
    grip_strength: SubStats = field(default_factory=SubStats(name="Grip Strength"))
    lower_body_strength: SubStats = field(default_factory=SubStats(name="Lower Body Strength"))
    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    # Each substat has levels, exp, and a training zone

    
    # Might have more things soon ??

@dataclass
class SpeedStats():
    """ 
    Object for storing data on player speed and their individual substats
    """

    speed: int = 1 # base level
    substat_names: ClassVar[list[str]] = [
        "Reaction time",
        "Velocity",
        "Acceleration",
        "Agility",
    ] # Used for UI display

    reaction_time: SubStats = field(default_factory=SubStats(name="Reaction Time"))
    velocity: SubStats = field(default_factory=SubStats(name="Velocity"))
    acceleration: SubStats = field(default_factory=SubStats(name="Acceleration"))
    agility: SubStats = field(default_factory=SubStats(name="Agility"))
    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    # Each substat has levels, exp, and a training zone

    # Might have more things soon ??


@dataclass
class DurabilityStats():
    """ 
    Object for storing data on player durability and their individual substats
    """

    durability: int = 1 # base level
    substat_names: ClassVar[list[str]] = [
        "Lung capacity",
        "Stamina",
        "Regeneration",
        "Toughness",
    ] # Used for UI display

    lung_capacity: SubStats = field(default_factory=SubStats(name="Lung Capacity"))
    stamina: SubStats = field(default_factory=SubStats(name="Stamina"))
    regeneration: SubStats = field(default_factory=SubStats(name="Regeneration"))
    toughness: SubStats = field(default_factory=SubStats(name="Toughness"))
    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    # Each substat has levels, exp, and a training zone

    # Might have more things soon ??

@dataclass
class IntelligenceStats(): 
    """ 
    Object for storing data on player intelligence and their individual substats
    """

    intelligence: int = 1
    substat_names: ClassVar[list[str]] = [
        "Knowledge",
        "Logic",
        "Strategy",
        "Problem Solving",
    ] # Used for UI display

    knowledge: SubStats = field(default_factory=SubStats(name="Knowledge"))
    logic: SubStats = field(default_factory=SubStats(name="Logic"))
    strategy: SubStats = field(default_factory=SubStats(name="Strategy"))
    problem_solving: SubStats = field(default_factory=SubStats(name="Problem Solving"))
    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    # Each substat has levels, exp, and a training zone

    # Might have more things soon ??

@dataclass
class MagicStats():
    """ 
    Object for storing data on player magic and their individual substats
    """

    magic: int = 1
    substat_names: ClassVar[list[str]] = [
        "Mana Control",
        "Spell Power",
        "Magic Resistance",
    ] # Used for UI display

    mana_control: SubStats = field(default_factory=SubStats(name="Mana Control"))
    spell_power: SubStats = field(default_factory=SubStats(name="Spell Power"))
    magic_resistance: SubStats = field(default_factory=SubStats(name="Magic Resistance"))
    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    # Each substat has levels, exp, and a training zone

    # Might have more things soon ??