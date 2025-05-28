from UI_files.player_training_ui import TrainingUI
from tools.help_tools import clear_screen
from player_files import player

user = player.Player("Jeremy")

test = TrainingUI(user)
clear_screen()
test.render_UI()