from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Attachment:
    id: str
    name: str
    url: str

@dataclass
class Card:
    id: str
    name: str
    list_id: str
    desc: Optional[str] = ""
    attachments: Optional[List[Attachment]] = None

