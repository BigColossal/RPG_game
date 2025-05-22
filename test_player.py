from player_files.player import Player
import time
from tools.help_tools import clear_screen

user = Player("Jeremy")

for i in range(50):
    print(f"level: {user.level} exp: {round(user.exp)}")
    user.add_exp("exp", 5)
    user.check_exp_for_up("level", "exp")
    time.sleep(0.5)
    clear_screen()

