from pydantic import BaseModel

class Sottocampo(BaseModel):
    name: str
    forest_slots: int