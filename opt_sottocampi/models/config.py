from pydantic import BaseModel
from typing import List, Dict
from opt_sottocampi.models.unit import Unit
from opt_sottocampi.models.sottocampo import Sottocampo

class CampConfig(BaseModel):
    units: List[Unit]
    sottocampi: Dict[str, Sottocampo]