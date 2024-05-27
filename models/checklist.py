from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Checklist:
    id: str
    name: str
    card_id: str
    items: List[str]
