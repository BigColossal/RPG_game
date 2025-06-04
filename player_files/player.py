import tools.error_handling as error_handling
from player_files.player_stats.stat_base_classes import StrengthStats, SpeedStats, DurabilityStats, IntelligenceStats, MagicStats
from player_files.player_inventory import PlayerInventory
from dataclasses import dataclass, field

@dataclass
class Player:
    name: str
    level: int = 1
    level_exp: int = 0

    player_class: str = ""

    cindrals: int = 0

    strength: StrengthStats = field(default_factory=lambda:StrengthStats())
    speed: SpeedStats = field(default_factory=lambda:SpeedStats())
    durability: DurabilityStats = field(default_factory=lambda:DurabilityStats())
    intelligence: IntelligenceStats = field(default_factory=lambda:IntelligenceStats())
    magic: MagicStats = field(default_factory=lambda:MagicStats())

    # Might be changed in the future
    swordsmanship: int = 1
    farming: int = 1
    fishing: int = 1
    mining: int = 1
    spells: list[str] = field(default_factory=list)

    inventory: PlayerInventory = field(default_factory=lambda:PlayerInventory())

    rebirths: int = 0
    reality_shards: int = 0
    training_bonus: int = 1

    