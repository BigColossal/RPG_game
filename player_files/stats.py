from dataclasses import dataclass, field, fields
from typing import ClassVar


@dataclass
class SubStats: 
    """ 
    Object for storing and updating substat data 
    """

    name: str = ""
    level: int = 1
    exp: int = 0
    training_zone: str = ""
    exp_to_next_level: int = 10

    def add_exp(self, exp):
        """
        Adds exp to the existing exp attribute
        
        Parameters:
        exp (int): total exp to be added to this object
        """

        self.exp += exp

    def check_and_level_up(self):
        """
        Calculates the exp required for leveling up
        If current exp meets this criteria, increments level and removes exp from the current amount

        If substat can still be leveled up with remaining exp, continue in the loop until it can no longer

        Returns:
        leveled_up (boolean): for if player leveled up or not
        """
        leveled_up = False
        while True:
            if self.exp >= self.exp_to_next_level:
                self.exp -= self.exp_to_next_level
                self.exp_to_next_level = self.compute_exp_requirement()
                self.level += 1
                leveled_up = True
            else:
                break

        return leveled_up

    def compute_exp_requirement(self):
        """
        Computes the exp requirement for a given level
        Formula uses different values for levels 1-99 and levels 100+

        Exp requirements rise faster after level 100

        Parameters:
        level (int)

        Returns:
        Calculated integer exp requirement for the given argument value

        """

        b = (self.level - 1) // 100
        i = (self.level - 1) % 100
        if b == 0:
            start_exp = 10
            end_exp = 50000
        else:
            start_exp = 50000 * (250 ** (b - 1))
            end_exp = 50000 * (250 ** b)
        return start_exp + ((i / 99) ** 2) * (end_exp - start_exp) 



class PlayerStat:
    def __init__(self):
        self.main_level = 1
        self.substats = [f.name for f in fields(self) if f.type == SubStats]
        self.substat_amount = len(self.substats)

        self.main_level_req = self.main_level * self.substat_amount
        self.total_substat_levels = 0

    @staticmethod
    def update_total_substat_level(method):
        def wrapper(self, *args, **kwargs):
            leveled_up = method(self, *args, **kwargs)
            if leveled_up:
                self.total_substat_levels += 1
            return leveled_up
        return wrapper

    @update_total_substat_level
    def train(self, substat_name, exp):
        """
        User selects a substat to train, and then the game will add exp to its current amount the substat has
        Then checks for if that substat can level up

        Parameters:
        substat_name (str): The name of the substat user is training
        exp (int): The amount of exp to be added
        """
        if substat_name in self.substats:
            substat_obj = getattr(self, substat_name)

            substat_obj.add_exp(exp)
            return substat_obj.check_and_level_up()


    def main_level_up(self):
        if self.total_substat_levels >= self.main_level_req:
            self.main_level += 1
            self.main_level_req += self.substat_amount

# Objects for storing all data on stats, this includes its level and the data on its substats

@dataclass
class StrengthStats(PlayerStat):
    """ 
    Object for storing data on player strength and their individual substats
    """

    main_name: str =  "Strength"
    substat_names: ClassVar[list[str]] = [
            "Core Strength",
            "Upper body Strength",
            "Grip Strength",
            "Lower body Strength",
        ] # Used for UI display
    
    core_strength: SubStats = field(default_factory=lambda:SubStats(name="Core Strength")) 
    upper_body_strength: SubStats = field(default_factory=lambda:SubStats(name="Upper Body Strength"))
    grip_strength: SubStats = field(default_factory=lambda:SubStats(name="Grip Strength"))
    lower_body_strength: SubStats = field(default_factory=lambda:SubStats(name="Lower Body Strength"))
    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    # Each substat has levels, exp, and a training zone

    def __post_init__(self):
        super().__init__()
    # Might have more things soon ??

@dataclass
class SpeedStats(PlayerStat):
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

    reaction_time: SubStats = field(default_factory=lambda:SubStats(name="Reaction Time"))
    velocity: SubStats = field(default_factory=lambda:SubStats(name="Velocity"))
    acceleration: SubStats = field(default_factory=lambda:SubStats(name="Acceleration"))
    agility: SubStats = field(default_factory=lambda:SubStats(name="Agility"))
    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    # Each substat has levels, exp, and a training zone

    def __post_init__(self):
        super().__init__()
    # Might have more things soon ??


@dataclass
class DurabilityStats(PlayerStat):
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

    lung_capacity: SubStats = field(default_factory=lambda:SubStats(name="Lung Capacity"))
    stamina: SubStats = field(default_factory=lambda:SubStats(name="Stamina"))
    regeneration: SubStats = field(default_factory=lambda:SubStats(name="Regeneration"))
    toughness: SubStats = field(default_factory=lambda:SubStats(name="Toughness"))
    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    # Each substat has levels, exp, and a training zone

    def __post_init__(self):
        super().__init__()
    # Might have more things soon ??

@dataclass
class IntelligenceStats(PlayerStat): 
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

    knowledge: SubStats = field(default_factory=lambda:SubStats(name="Knowledge"))
    logic: SubStats = field(default_factory=lambda:SubStats(name="Logic"))
    strategy: SubStats = field(default_factory=lambda:SubStats(name="Strategy"))
    problem_solving: SubStats = field(default_factory=lambda:SubStats(name="Problem Solving"))
    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    # Each substat has levels, exp, and a training zone

    def __post_init__(self):
        super().__init__()
    # Might have more things soon ??

@dataclass
class MagicStats(PlayerStat):
    """ 
    Object for storing data on player magic and their individual substats
    """

    magic: int = 1
    substat_names: ClassVar[list[str]] = [
        "Mana Control",
        "Spell Power",
        "Magic Resistance",
    ] # Used for UI display

    mana_control: SubStats = field(default_factory=lambda:SubStats(name="Mana Control"))
    spell_power: SubStats = field(default_factory=lambda:SubStats(name="Spell Power"))
    magic_resistance: SubStats = field(default_factory=lambda:SubStats(name="Magic Resistance"))
    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    # Each substat has levels, exp, and a training zone

    def __post_init__(self):
        super().__init__()
    # Might have more things soon ??