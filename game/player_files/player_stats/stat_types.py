from dataclasses import dataclass, field
from player_files.player_stats.stat_base_classes import PlayerStat, SubStats, StatClasses
from typing import ClassVar

@dataclass
class StrengthStats(PlayerStat):
    """
    Represents the Strength stat category of a player, including its substats and tier classification.

    Attributes:
        main_name (str): The name of this primary stat category, e.g., 'Strength'.
        tier (str): Classification tier of this stat, used for scaling or progression systems.
        substat_display_names (list[str]): Static list of display names for UI representation of substats.

        core_strength (SubStats): Substat tracking core muscle development.
        upper_body_strength (SubStats): Substat tracking upper body strength (arms, chest, shoulders).
        grip_strength (SubStats): Substat tracking hand and grip endurance/power.
        lower_body_strength (SubStats): Substat tracking leg and lower body development.

        damage (int): Strength influences how much damage a user does
    """

    main_name: ClassVar[str] =  "Strength"
    tier: str = ""
    substat_display_names: ClassVar[list[str]] = [
            "Core Strength",
            "Upper body Strength",
            "Grip Strength",
            "Lower body Strength",
        ] # Used to show readable names in the UI (kept separate from internal attribute names)
    
    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    core_strength: SubStats = field(default_factory=lambda:SubStats(name="Core Strength", main_stat=StatClasses.STRENGTH)) 
    upper_body_strength: SubStats = field(default_factory=lambda:SubStats(name="Upper Body Strength", main_stat=StatClasses.STRENGTH))
    grip_strength: SubStats = field(default_factory=lambda:SubStats(name="Grip Strength", main_stat=StatClasses.STRENGTH))
    lower_body_strength: SubStats = field(default_factory=lambda:SubStats(name="Lower Body Strength", main_stat=StatClasses.STRENGTH))

    damage: int = 5

    def compute_damage(self):
        self.compute_player_physical_stats("damage", 5, 15, 100)


@dataclass
class SpeedStats(PlayerStat):
    """ 
    Represents the Speed stat category of a player, including its substats and tier classification.

    Attributes:
        main_name (str): The name of this primary stat category, e.g., 'Speed'.
        tier (str): Classification tier of this stat, used for scaling or progression systems.
        substat_display_names (list[str]): Static list of display names for UI representation of substats.

        reaction_time (SubStats): Substat tracking how quickly a player can perceive and respond to events.
        velocity (SubStats): Substat tracking the top speed in movement.
        acceleration (SubStats): Substat tracking the amount of time it takesin going from 0 to a 100 in terms of speed
        agility (SubStats): Substat tracking how fluidly and efficiently a player can dodge, maneuver, and change direction.
    """

    main_name: ClassVar[str] = "Speed"
    tier: str = ""
    substat_display_names: ClassVar[list[str]] = [
        "Reaction time",
        "Velocity",
        "Acceleration",
        "Agility",
    ] # Used to show readable names in the UI (kept separate from internal attribute names)

    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    reaction_time: SubStats = field(default_factory=lambda:SubStats(name="Reaction Time", main_stat=StatClasses.SPEED))
    velocity: SubStats = field(default_factory=lambda:SubStats(name="Velocity", main_stat=StatClasses.SPEED))
    acceleration: SubStats = field(default_factory=lambda:SubStats(name="Acceleration", main_stat=StatClasses.SPEED))
    agility: SubStats = field(default_factory=lambda:SubStats(name="Agility", main_stat=StatClasses.SPEED))

    accuracy: int = 100
    evasiveness: int = 100

    def compute_accuracy(self):
        return self.compute_player_physical_stats("accuracy", 5, 15, 100)
    
    def compute_evasiveness(self):
        return self.compute_player_physical_stats("evasiveness", 5, 15, 100)


@dataclass
class DurabilityStats(PlayerStat):
    """ 
    Represents the Durability stat category of a player, including its substats and tier classification.

    Attributes:
        main_name (str): The name of this primary stat category, e.g., 'Durability'.
        tier (str): Classification tier of this stat, used for scaling or progression systems.
        substat_display_names (list[str]): Static list of display names for UI representation of substats.

        lung_capacity (SubStats): Substat tracking how long the lungs can hold oxygen without extra intake
        stamina (SubStats): Substat tracking how much energy the body can expend before becoming exhausted
        regeneration (SubStats): Substat tracking how quick the rate of healing from wounds is
        toughness (SubStats): Substat tracking how tough the body's skin is
    """

    main_name: ClassVar[str] = "Durability"
    tier: str = ""
    substat_stat_names: ClassVar[list[str]] = [
        "Lung capacity",
        "Stamina",
        "Regeneration",
        "Toughness",
    ] # Used to show readable names in the UI (kept separate from internal attribute names)

    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    lung_capacity: SubStats = field(default_factory=lambda:SubStats(name="Lung Capacity", main_stat=StatClasses.DURABILITY))
    stamina: SubStats = field(default_factory=lambda:SubStats(name="Stamina", main_stat=StatClasses.DURABILITY))
    regeneration: SubStats = field(default_factory=lambda:SubStats(name="Regeneration", main_stat=StatClasses.DURABILITY))
    toughness: SubStats = field(default_factory=lambda:SubStats(name="Toughness", main_stat=StatClasses.DURABILITY))

    player_health: int = 100
    player_stamina: int = 100
    player_regen: int = 5

    def compute_health(self) -> int:
        return self.compute_player_physical_stats("player_health", 15, 50, 300)

    def compute_stamina(self) -> int:
        return self.compute_player_physical_stats("player_stamina", 5, 10, 75)
    
    def compute_regen(self) -> int:
        return self.compute_player_physical_stats("player_regen", 1, 5, 50)




@dataclass
class IntelligenceStats(PlayerStat): 
    """ 
    Represents the Intelligence stat category of a player, including its substats and tier classification.

    Attributes:
        main_name (str): The name of this primary stat category, e.g., 'Intelligence'.
        tier (str): Classification tier of this stat, used for scaling or progression systems.
        substat_display_names (list[str]): Static list of display names for UI representation of substats.

        knowledge (SubStats): Substat tracking how much overall knowledge is known
        logic (SubStats): Substat tracking the brain's ability to analyze and reason
        strategy (SubStats): Substat tracking the ability to plan, adapt, and make long-term decisions effectively in complex situations.
        problem_solving (SubStats): Substat tracking the ability to solve issues with the most optimal solutions

        player_leadership (int): Leadership over empire
    """

    main_name: ClassVar[str] = "Intelligence"
    tier: str = ""
    substat_stat_names: ClassVar[list[str]] = [
        "Knowledge",
        "Logic",
        "Strategy",
        "Problem Solving",
    ] # Used to show readable names in the UI (kept separate from internal attribute names)

    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    knowledge: SubStats = field(default_factory=lambda:SubStats(name="Knowledge", main_stat=StatClasses.INTELLIGENCE))
    logic: SubStats = field(default_factory=lambda:SubStats(name="Logic", main_stat=StatClasses.INTELLIGENCE))
    strategy: SubStats = field(default_factory=lambda:SubStats(name="Strategy", main_stat=StatClasses.INTELLIGENCE))
    problem_solving: SubStats = field(default_factory=lambda:SubStats(name="Problem Solving", main_stat=StatClasses.INTELLIGENCE))

    player_leadership: int = 50

    def compute_leadership(self) -> int:
        return self.compute_player_physical_stats("player_leadership", 10, 35, 175)


@dataclass
class MagicStats(PlayerStat):
    """ 
    Represents the Magic stat category of a player, including its substats and tier classification.

    Attributes:
        main_name (str): The name of this primary stat category, e.g., 'Magic'.
        tier (str): Classification tier of this stat, used for scaling or progression systems.
        substat_display_names (list[str]): Static list of display names for UI representation of substats.

        mana_control (SubStats): Substat tracking the capacity and efficient usage of mana
        spell_power (SubStats): Substat tracking how powerful cast spells are
        magic_resistance (SubStats): Substat tracking how well the body reacts to opposing magic spells

        mana (int): Amount of mana capacity
    """

    main_name: ClassVar[str] = "Magic"
    tier: str = ""
    substat_stat_names: ClassVar[list[str]] = [
        "Mana Control",
        "Spell Power",
        "Magic Resistance",
    ] # Used to show readable names in the UI (kept separate from internal attribute names)

    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    mana_control: SubStats = field(default_factory=lambda:SubStats(name="Mana Control", main_stat=StatClasses.MAGIC))
    spell_power: SubStats = field(default_factory=lambda:SubStats(name="Spell Power", main_stat=StatClasses.MAGIC))
    magic_resistance: SubStats = field(default_factory=lambda:SubStats(name="Magic Resistance", main_stat=StatClasses.MAGIC))

    mana: int = 100
    
    def compute_mana(self):
        return self.compute_player_physical_stats("mana", 10, 25, 125)