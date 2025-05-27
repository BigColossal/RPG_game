from UI_files.base_ui import BaseUI
from tools import error_handling

class TrainingUI(BaseUI):

    def __init__(self):
        super().__init__()
        self.screen_start_up()

    def screen_start_up(self):
        self.insert_text("test", "Testing the game UI", (0, 0))

    def insert_text(self, name, text, pos):
        x, y = pos[0] + 1, pos[1] + 1

        if x < 0 or y < 0: # check negative case
            error_handling.check_index_err(x, y, name)

        text_len = len(text)
        if text_len != 0:
            end_x = x + (text_len - 1)
            char_index = 0
            for i in range(x, end_x + 1):
                try:
                    self.UI[y] = self.UI[y][:i] + text[char_index] + self.UI[y][i + 1:]
                    char_index += 1
                except Exception:
                    error_handling.check_index_err(x, y, name)

        
        self.text_object_names.append(name)