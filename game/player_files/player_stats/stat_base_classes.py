from dataclasses import dataclass, field, fields
from typing import ClassVar
from enum import Enum
from tools.number_utils import round_to_3_leading_digits

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


class StatClasses(Enum):
    """
    Enum representing different stat categories used to classify a character's capabilities.

    Attributes:
        STRENGTH: Represents physical power, typically used to lift or strike objects.
        SPEED: Represents movement velocity or reaction time.
        DURABILITY: Represents resistance to damage or physical stress.
        INTELLIGENCE: Represents mental capacity and problem-solving ability.
        MAGIC: Represents magical prowess or control over supernatural forces.
    """
    STRENGTH = "Strength"
    SPEED = "Speed"
    DURABILITY = "Durability"
    INTELLIGENCE = "Intelligence"
    MAGIC = "Magic"

    def capability_measure_helper(self):
        """
        Returns the unit of measurement associated with the stat type.

        Returns:
            str: A string representing the unit of measurement:
                - "Lb" for STRENGTH (Pounds of force)
                - "Kmph" for SPEED (Kilometers per hour)
                - "Lbf" for DURABILITY (Pound-force)
                - "IQ" for INTELLIGENCE (Intelligence Quotient)
                - "MU" for MAGIC (Mana Units)
        """

        return {
            StatClasses.STRENGTH: "Lb", # Pounds - measures physical force
            StatClasses.SPEED: "Kmph", # Kilometers per hour - measures speed
            StatClasses.DURABILITY: "Lbf", # Pound-force - resistance to damage
            StatClasses.INTELLIGENCE: "IQ", # Intelligence Quotient
            StatClasses.MAGIC: "MU", # Mana Units - magical energy
        }[self]


@dataclass
class SubStats: 
    """
    Represents a substat that can be trained and leveled up over time.

    Attributes:
    main_stat (StatClasses): Enum for the 5 different main stats (e.g., Strength, Intelligence)
    capability_multi (int): Multiplier for how much the substat level affects the substat's capability in terms of either Kmph, Lbs, IQ, etc.
    measurement (str): The way for measuring the capability of a substat.
    name (str): The name of the substat (e.g., Core Strength, Agility).
    level (int): The current level of the substat. Defaults to 1.
    exp (int): The current experience points accumulated. Defaults to 0.
    training_zone (str): The name of the training zone where this substat can be improved.
    exp_to_next_level (int): The experience required to reach the next level. Defaults to 10.
    """

    main_stat: StatClasses
    name: str
    capability_multi: int = 1
    measurement: str = field(init=False)
    capability: str = field(init=False)

    level: int = 1
    exp: int = 0
    training_zone: str = ""
    exp_to_next_level: int = 10

    def __post_init__(self):
        self.measurement = self.main_stat.capability_measure_helper()
    
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

    def compute_capability(self) -> int:
        """
        Calculates how strong/fast/smart etc the substat is, and then stores it

        Multiplies the current level of the substat by how much multi it has.
        all substats have different multis depending on what they are (e.g, upper body 5.5, lower body 7.5)

        """
        self.capability = self.level * self.capability_multi + " " + self.measurement



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

    def compute_player_physical_stats(self, physical_name: str, option1: int, option2: int, option3: int):
        """
        Computes a physical stat value for the player based on their level and growth options.

        This method dynamically adjusts a specific physical stat (e.g., strength, speed) based on 
        the player's main level. The stat increase is calculated using a tiered system:
            - Levels < 50 use option1 as the multiplier.
            - Levels 50-99 use option2.
            - Levels 100+ use option3 with a scaling boost beyond level 100.

        The result is slightly boosted (multiplied by 1.1) before applying the level-based increase,
        then rounded to three leading digits.

        Args:
            physical_name (str): The name of the physical stat attribute to modify (e.g., "strength").
            option1 (int): Growth factor for levels below 50.
            option2 (int): Growth factor for levels between 50 and 99.
            option3 (int): Base growth factor for levels 100 and above, with scaling applied.

        Returns:
            int: The newly computed physical stat, rounded to 3 leading digits.
        """
        if self.main_level < 50:
            increase_factor = (self.main_level / 5) * option1
        elif self.main_level < 100:
            increase_factor = (self.main_level / 5) * option2
        elif self.main_level >= 100:
            # Scales more aggressively after level 100
            increase_factor = (self.main_level / 5) * (option3 * (((self.main_level - 100) / 75) + 1))
        
        # Retrieve the original stat value using the provided attribute name
        chosen_physical_stat = getattr(self, physical_name)

        # Apply a base 10% boost and add the increase factor
        chosen_physical_stat = round_to_3_leading_digits(int(chosen_physical_stat * 1.1) + increase_factor)

        return chosen_physical_stat