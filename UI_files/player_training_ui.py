from UI_files.base_ui import BaseUI
from tools import error_handling

class TrainingUI(BaseUI):

    def __init__(self, player):
        super().__init__(player.name)
        self.screen_start_up()
        self.stat_options = [
            "Strength",
            "Durability",
            "Speed",
            "Intelligence",
            "Magic",
        ]
        self.strength_sub_stats = [
            "Core Strength",
            "Upper body",
            "Grip",
            "Lower body",
        ]

    def screen_start_up(self):
        self.insert_text("Title Text", "Training", (44, 0), True)
        self.insert_text("Name text", self.username, (1, 0), True)
        self.insert_text("Level text", "Level: ", (1, 1), True)