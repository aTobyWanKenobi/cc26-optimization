from .base import BaseConstraint
from opt_sottocampi.models.unit import Zone

class ZoneDiversityConstraint(BaseConstraint):
    def __init__(self, min_units_per_zone: int):
        self.min_units_per_zone = min_units_per_zone

    def apply(self, model, variables, data):
        for sottocampo in data['sottocampi']:
            for zone in Zone:
                model += (
                    sum(
                        variables[unit.name, sottocampo.name]
                        for unit in data['units']
                        if unit.zone == zone
                    ) >= self.min_units_per_zone,
                    f"MinZone_{zone}_{sottocampo.name}"
                )