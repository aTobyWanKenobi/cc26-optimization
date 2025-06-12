from .base import BaseConstraint
from opt_sottocampi.models.unit import Zone

class ZoneDiversityConstraint(BaseConstraint):
    def __init__(self, min_zones_per_sc: int, max_zones_per_sc: int):
        self.min_zones_per_sc = min_zones_per_sc
        self.max_zones_per_sc = max_zones_per_sc

    def apply(self, model, var_assignements, var_zone_in_sc, data):
        for sc in data['sottocampi']:
            zone_count = sum(var_zone_in_sc[zone, sc.name] for zone in Zone)
            
            model += (
                zone_count >= self.min_zones_per_sc,
                f"min_zone_{sc.name}"
            )
            
            model += (
                zone_count <= self.max_zones_per_sc,
                f"max_zone_{sc.name}"
            )
            
            
class MaxZoneUnitsPerSottocampoConstraint(BaseConstraint):
    
    def __init__(self, max_zone_units_per_sc: int):
        self.max_zone_units_per_sc = max_zone_units_per_sc

    def apply(self, model, var_assignments, var_zone_in_sc, data):
        for zone in Zone:
            for sc in data['sottocampi']:
                units_in_zone = [u for u in data['units'] if u.zone == zone]

                model += (
                    sum(var_assignments[u.name, sc.name] for u in units_in_zone) <= self.max_zone_units_per_sc,
                    f"max_units_{zone}_{sc.name}"
                )