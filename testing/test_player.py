from player_files.player import Player
from player_files.player_stats.stat_base_classes import StrengthStats
import time
from tools.help_tools import clear_screen

test = Player("jeremy", strength=StrengthStats(main_level=0))

for i in range(1000):
    test.strength.main_level += 1
    print(test.strength.compute_damage())
    print("\n")