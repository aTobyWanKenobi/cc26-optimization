from opt_sottocampi.constraints.base import BaseConstraint

class ForestConstraint(BaseConstraint):
    
    def __init__(self, tolerance: int):
        self.tolerance = tolerance
    
    
    def apply(self, model, var_assignements, var_zone_in_sc, data):
        for sottocampo in data['sottocampi']:
            if sottocampo.forest_slots == 0:
                accepted_capacity = 0
            else:
                accepted_capacity = sottocampo.forest_slots + self.tolerance
            model += (
                sum(
                    var_assignements[unit.name, sottocampo.name] * unit.forest_requirement
                    for unit in data['units']
                ) <= accepted_capacity,
                f"ForestSlots_{sottocampo.name}"
            )