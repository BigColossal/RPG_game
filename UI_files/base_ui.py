class BaseUI():
    def __init__(self):
        self.UI = [[". " * 50] for i in range(25)]

    def __repr__(self):
        for line in self.UI:
            print(line[0])

base = BaseUI()

print(base)