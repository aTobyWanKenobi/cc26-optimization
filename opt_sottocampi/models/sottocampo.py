from pydantic import BaseModel

class Sottocampo(BaseModel):
    name: str
    forest_slots: int
    capacity: float
    
    def __str__(self):
        return f"Sottocampo {self.name} ({100*self.capacity}% della capacità | {self.forest_slots} gettoni bosco)"