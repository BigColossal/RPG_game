from dataclasses import dataclass, field
from typing import Optional

@dataclass
class PlayerInventory:
    items: list[str] = field(default_factory=list)

    weapon: Optional[str] = None
    helmet: Optional[str] = None
    chestplate: Optional[str] = None
    leggings: Optional[str] = None
    belt: Optional[str] = None
    left_glove: Optional[str] = None
    right_glove: Optional[str] = None
    boots: Optional[str] = None
    accessories: list[str] = field(default_factory=list)