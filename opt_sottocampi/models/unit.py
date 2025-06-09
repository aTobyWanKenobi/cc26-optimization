from pydantic import BaseModel, model_validator
from enum import Enum
from typing import List, Set

class Zone(str, Enum):
    BEL = 'BEL'
    LOC = 'LOC'
    LUG = 'LUG'
    MEN = 'MEN'

class Reparto(BaseModel):
    name: str
    zone: Zone
    participants: int
    forest_req: int

class Unit(BaseModel):
    name: str
    reparti: List[Reparto]

    @property
    def total_participants(self) -> int:
        return sum(r.participants for r in self.reparti)

    @property
    def forest_requirement(self) -> int:
        return sum(r.forest_req for r in self.reparti)

    @property
    def zone(self) -> Zone:
        return self.reparti[0].zone

    @model_validator(mode='after')
    def validate_same_zone(self) -> 'Unit':
        if self.reparti:
            first_zone = self.reparti[0].zone
            for r in self.reparti:
                if r.zone != first_zone:
                    raise ValueError(f"All reparti in a unit must belong to the same zone. Found {r.zone} != {first_zone}")
        return self