from pydantic import BaseModel, model_validator
from enum import Enum
from typing import List, Set

class Zone(str, Enum):
    BEL = 'BEL'
    LOC = 'LOC'
    LUG = 'LUG'
    MEN = 'MEN'
    
class Hike(str, Enum):
    CAPANNA = 'CAPANNA'
    TELI_REPARTO = 'TELI_REPARTO'
    TELI_PATTUGLIA = 'TELI_PATTUGLIA'
    GIORNO = 'GIORNO'

class Reparto(BaseModel):
    name: str
    zone: Zone
    participants: int
    forest_req: int
    hike: Hike
    
    def __str__(self):
        return f"[{self.zone.value}] {self.name} : {self.participants} partecipanti | {self.forest_req} bosco | in {self.hike.value}"

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
    
    @property
    def hike(self) -> Hike:
        if len({r.hike for r in self.reparti}) > 1:
            raise ValueError('Due reparti gemellati con escursioni diverse!')
        else:
            return self.reparti[0].hike

    @model_validator(mode='after')
    def validate_same_zone(self) -> 'Unit':
        if self.reparti:
            first_zone = self.reparti[0].zone
            for r in self.reparti:
                if r.zone != first_zone:
                    raise ValueError(f"All reparti in a unit must belong to the same zone. Found {r.zone} != {first_zone}")
        return self
    
    def __str__(self):
        return f"[{self.zone.value}] {self.name} : {self.total_participants} partecipanti | {self.forest_requirement} bosco | in {self.hike.value}"