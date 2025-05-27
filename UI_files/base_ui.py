class BaseUI():
    def __init__(self):
        self.UI_width = 100
        self.UI_height = 25
        self.UI = [". " * int(self.UI_width / 2) for i in range(self.UI_height)]
        self.add_border()
        self.text_object_names = []

    def render_UI(self):
        for line in self.UI:
            print(line)

    def print_text_objects(self):
        print(self.text_object_names)

    def add_border(self):
        self.UI[0] = "-" * (self.UI_width - 1)
        self.UI[self.UI_height - 1] = "-" * (self.UI_width - 1)
        for i in range(1, self.UI_height - 1):
            self.UI[i] = "|" + self.UI[i][0:]
            self.UI[i] = self.UI[i][:self.UI_width - 2] + "|"

        self.add_char("*", (0, 0))
        self.add_char("*", (self.UI_width - 2, 0))
        self.add_char("*", (0, self.UI_height - 1))
        self.add_char("*", (self.UI_width - 2, self.UI_height - 1))


    def add_char(self, char, pos):
        x, y = pos[0], pos[1]
        self.UI[y] = self.UI[y][:x] + char + self.UI[y][x + 1:]