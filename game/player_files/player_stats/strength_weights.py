from enum import Enum

class CoreStrength(Enum):
    1 = "2 lb" # below average (level 1)
    2 = "8 lb" # below average (level 10)
    3 = "25 lb" # average (level 20)
    4 = "50 lb" # average (level 30)
    5 = "80 lb" # average (level 40)
    6 = "140 lb" # athlete (level 50)
    7 = "200 lb" # athlete (level 60)
    8 = "275 lb" # athlete (level 70)
    9 = "350 lb" # athlete (level 80)
    10 = "425 lb" # athlete (level 90)
    11 = "500 lb" # peak human (level 100)
    12 = "625 lb" # peak human (level 110)
    13 = "775 lb" # peak human (level 120)
    14 = "950 lb" # peak human (level 130)
    15 = "1100 lb" # peak human (level 140)
    16 = "1325 lb" # peak human (level 150)
    17 = "1625 lb" # peak huamn (level 160)
    18 = "1900 lb" # peak human (level 170)
    19 = "2300 lb" # super human (level 180)
    20 = "4500 lb" # super human (level 190)
    21 = "20 tons" # super human (level 200)


class UpperBody(Enum):
    pass

class Grip(Enum):
    pass

class LowerBody(Enum):
    pass