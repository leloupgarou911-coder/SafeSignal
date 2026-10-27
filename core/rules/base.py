from dataclasses import dataclass
from typing import Pattern
@dataclass(frozen=True)
class Rule:
 id:str
 category:str
 pattern:Pattern[str]
 title:dict
 explanation:dict
 advice:dict
 severity:str="medium"
