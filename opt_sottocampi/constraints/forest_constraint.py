from opt_sottocampi.constraints.base import BaseConstraint

class ForestConstraint(BaseConstraint):
    def apply(self, model, variables, data):
        for sottocampo in data['sottocampi']:
            model += (
                sum(
                    variables[unit.name, sottocampo.name] * unit.forest_requirement
                    for unit in data['units']
                ) <= sottocampo.forest_slots,
                f"ForestSlots_{sottocampo.name}"
            )