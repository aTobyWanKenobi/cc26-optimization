from opt_sottocampi.constraints.base import BaseConstraint

class CapacityConstraint(BaseConstraint):
    def __init__(self, capacity_distribution: dict):
        self.capacity_distribution = capacity_distribution

    def apply(self, model, variables, data):
        total_participants = sum(unit.total_participants for unit in data['units'])
        for sottocampo in data['sottocampi']:
            target = self.capacity_distribution[sottocampo.name] * total_participants
            actual = sum(
                variables[unit.name, sottocampo.name] * unit.total_participants
                for unit in data['units']
            )
            model += (actual <= target + 2, f"UpperBound_{sottocampo.name}")
            model += (actual >= target - 2, f"LowerBound_{sottocampo.name}")