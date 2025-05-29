from dataclasses import dataclass, field, fields
from typing import ClassVar

"""
Player Stats Module

This module defines a modular and extensible system for tracking and updating categorized statistical attributes. 
It includes:

- `PlayerStat`: A general-purpose class that groups related `SubStats`, handles leveling, and calculates aggregate data.
- Subclasses of `PlayerStat`: Represent specific stat categories such as Strength, Speed, Durability, Intelligence, and Magic, 
  each composed of relevant substats.
- `SubStats`: Individual measurable components that can gain experience, level up, and affect broader categories.


Features:
- Nonlinear experience and level progression formulas.
- Automatic propagation of substat changes to the main category.
- Clean separation of internal keys and display-friendly labels.
- Designed for flexibility, extension, and clarity in structured attribute systems.
"""


@dataclass
class SubStats: 
    """
    Represents a substat that can be trained and leveled up over time.

    Attributes:
    name (str): The name of the substat (e.g., Strength, Agility).
    level (int): The current level of the substat. Defaults to 1.
    exp (int): The current experience points accumulated. Defaults to 0.
    training_zone (str): The name of the training zone where this substat can be improved.
    exp_to_next_level (int): The experience required to reach the next level. Defaults to 10.
    """

    name: str = ""
    level: int = 1
    exp: int = 0
    training_zone: str = ""
    exp_to_next_level: int = 10

    def add_exp(self, exp: int) -> None:
        """
        Adds experience points to the current substat.

        Args:
            exp (int): The amount of experience to add.
        
        Notes:
            This method does not handle level-ups. It only increases the raw experience total.
        """

        self.exp += exp

    def check_and_level_up(self) -> bool:
        """
        Checks if the substat has enough experience to level up.

        This method repeatedly levels up the substat while the current experience
        exceeds the required threshold. Each level-up deducts the required experience,
        increases the level, and recalculates the new experience requirement.

        Returns:
            bool: True if at least one level-up occurred, False otherwise.
        """

        leveled_up = False # Tracks whether any level-up occurred

        while True:
            # Deduct required exp and level up
            if self.exp >= self.exp_to_next_level:
                self.exp -= self.exp_to_next_level
                self.exp_to_next_level = self.compute_exp_requirement() # Recalculate threshold for next level
                self.level += 1
                leveled_up = True
            else:
                break # Exit loop if there's not enough exp to level up

        return leveled_up

    def compute_exp_requirement(self) -> int:
        """
        Calculates the experience required to reach the next level.

        The formula scales non-linearly:
        - For levels 1-99, experience increases smoothly from 10 to 50,000.
        - After level 100, experience requirements rise exponentially by a factor of 250.

        Returns:
            int: The experience required to reach the next level.
        """

        # Use integer division to find the current 'block' of 100 levels
        b = (self.level - 1) // 100

        # Position within the current 100-level block
        i = (self.level - 1) % 100

        # Exp requirements grow slowly at first, then exponentially after level 100
        if b == 0:
            start_exp = 10
            end_exp = 50000
        else:
            # For higher levels, scale exponentially
            start_exp = 50000 * (250 ** (b - 1))
            end_exp = 50000 * (250 ** b)

        # Quadratic interpolation between start and end exp values
        exp_req = start_exp + ((i / 99) ** 2) * (end_exp - start_exp) 

        # Experience points are generally whole numbers
        return int(exp_req)


@dataclass
class PlayerStat:
    """
    Base class for tracking a player's overall stat category and its associated substats.

    This class handles the logic for:
    - Initializing and managing substats.
    - Calculating the number of substats and the requirement to level up the main stat.
    - Training substats by applying experience and checking for level-ups.
    - Tracking total substat levels and handling main level progression when requirements are met.

    Attributes:
        main_level (int): The player's current level for this stat category.
        total_substat_levels (int): Total levels gained across all substats.
        main_level_req (int): Total substat levels required to level up the main stat.
        substats (list[str]): List of attribute names representing each substat.
        substat_amount (int): Number of substats under this stat category.
    """

    main_level: int = 1
    total_substat_levels: int = 0
    main_level_req: int = 0

    # These are marked with 'init=False' so it's not expected as a parameter during object creation
    # it's set in __post_init__.
    substats: list[str] = field(init=False)
    substat_amount: int = field(init=False)

    def __post_init__(self):
        """
        Initializes derived values after dataclass fields are populated.

        - Gathers all attributes of type SubStats and stores their names in self.substats.
        - Calculates the number of substats.
        - Determines the experience requirement for the next main level.
        """

        # Checks each attribute in class and if it's type is a SubStats object, include it in the "self.substats" attribute
        self.substats = [
            f.name 
            for f in fields(self) 
            if isinstance(getattr(self, f.name, None), SubStats)]
        
        self.substat_amount = len(self.substats)

        # The main level (e.g., Durability) can increase if the total amount of levels
        self.main_level_req = self.main_level * self.substat_amount

    @staticmethod
    def update_total_substat_level(method):
        """
        Decorator for substat-leveling methods.

        Automatically increments the `total_substat_levels` attribute of the instance
        if the wrapped method returns `True`, indicating that a level-up occurred.

        Parameters:
        method (Callable): The method being decorated. It must return a boolean
                        indicating whether a level-up occurred.

        Returns:
        Callable: Wrapped method with additional logic for updating total substat levels.
        """

        def wrapper(self, *args, **kwargs):
            leveled_up = method(self, *args, **kwargs)
            if leveled_up:
                self.total_substat_levels += 1
            return leveled_up
        return wrapper

    @update_total_substat_level
    def train(self, substat_name: str, exp: int) -> bool:
        """
        Trains a specific substat by adding experience points and checking for level-up.

        This method locates the substat by name, adds the specified amount of experience, 
        and checks whether it qualifies for a level-up. If a level-up occurs, it returns True.

        Parameters:
        substat_name (str): The name of the substat to be trained.
        exp (int): The amount of experience points to add.

        Returns:
        bool: True if the substat leveled up; False otherwise.
        """

        if substat_name in self.substats:
            substat_obj = getattr(self, substat_name)
            substat_obj.add_exp(exp)
            return substat_obj.check_and_level_up()

    def try_main_level_up(self) -> bool:
        """
        Checks if the player's total substat levels meet or exceed the requirement for main level-up.
        If so, increments main level and updates the next level requirement.

        Returns:
        bool: True if the main level was increased, False otherwise.
        """
        if self.total_substat_levels >= self.main_level_req:
            self.main_level += 1
            self.main_level_req = self.main_level * self.substat_amount
            return True
        return False


# Objects for storing all data on stats, this includes its level and the data on its substats


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
    """

    main_name: str =  "Strength"
    tier: str = ""
    substat_display_names: ClassVar[list[str]] = [
            "Core Strength",
            "Upper body Strength",
            "Grip Strength",
            "Lower body Strength",
        ] # Used to show readable names in the UI (kept separate from internal attribute names)
    
    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    core_strength: SubStats = field(default_factory=lambda:SubStats(name="Core Strength")) 
    upper_body_strength: SubStats = field(default_factory=lambda:SubStats(name="Upper Body Strength"))
    grip_strength: SubStats = field(default_factory=lambda:SubStats(name="Grip Strength"))
    lower_body_strength: SubStats = field(default_factory=lambda:SubStats(name="Lower Body Strength"))

    # Might have more things soon ??


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

    main_name: str = "Speed"
    tier: str = ""
    substat_display_names: ClassVar[list[str]] = [
        "Reaction time",
        "Velocity",
        "Acceleration",
        "Agility",
    ] # Used to show readable names in the UI (kept separate from internal attribute names)

    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    reaction_time: SubStats = field(default_factory=lambda:SubStats(name="Reaction Time"))
    velocity: SubStats = field(default_factory=lambda:SubStats(name="Velocity"))
    acceleration: SubStats = field(default_factory=lambda:SubStats(name="Acceleration"))
    agility: SubStats = field(default_factory=lambda:SubStats(name="Agility"))

    # Might have more things soon ??


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

    main_name: str = "Durability"
    tier: str = ""
    substat_stat_names: ClassVar[list[str]] = [
        "Lung capacity",
        "Stamina",
        "Regeneration",
        "Toughness",
    ] # Used to show readable names in the UI (kept separate from internal attribute names)

    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    lung_capacity: SubStats = field(default_factory=lambda:SubStats(name="Lung Capacity"))
    stamina: SubStats = field(default_factory=lambda:SubStats(name="Stamina"))
    regeneration: SubStats = field(default_factory=lambda:SubStats(name="Regeneration"))
    toughness: SubStats = field(default_factory=lambda:SubStats(name="Toughness"))

    # Might have more things soon ??


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
    """

    main_name: str = "Intelligence"
    tier: str = ""
    substat_stat_names: ClassVar[list[str]] = [
        "Knowledge",
        "Logic",
        "Strategy",
        "Problem Solving",
    ] # Used to show readable names in the UI (kept separate from internal attribute names)

    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    knowledge: SubStats = field(default_factory=lambda:SubStats(name="Knowledge"))
    logic: SubStats = field(default_factory=lambda:SubStats(name="Logic"))
    strategy: SubStats = field(default_factory=lambda:SubStats(name="Strategy"))
    problem_solving: SubStats = field(default_factory=lambda:SubStats(name="Problem Solving"))

    # Might have more things soon ??


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
    """

    main_name: str = "Magic"
    tier: str = ""
    substat_stat_names: ClassVar[list[str]] = [
        "Mana Control",
        "Spell Power",
        "Magic Resistance",
    ] # Used to show readable names in the UI (kept separate from internal attribute names)

    # field(default_factory=*****) is used to ensure that values dont share mutable defaults
    mana_control: SubStats = field(default_factory=lambda:SubStats(name="Mana Control"))
    spell_power: SubStats = field(default_factory=lambda:SubStats(name="Spell Power"))
    magic_resistance: SubStats = field(default_factory=lambda:SubStats(name="Magic Resistance"))

    # Might have more things soon ??