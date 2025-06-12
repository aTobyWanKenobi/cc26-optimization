from opt_sottocampi.constraints.base import BaseConstraint

class BalanceUnitsPerSottocampoConstraint(BaseConstraint):
    
    def __init__(self, allowed_delta: int):
        self.allowed_delta = allowed_delta
    
    def apply(self, model, var_assignements, var_zone_in_sc, data):
        # Precompute total units in each sottocampo
        unit_count = {
            sc.name: sum(var_assignements[u.name, sc.name] for u in data['units'])
            for sc in data['sottocampi']
        }

        # For all pairs (A, B), constrain |count_A - count_B| <= 1
        for i in range(len(data['sottocampi'])):
            for j in range(i + 1, len(data['sottocampi'])):
                sc_a = data['sottocampi'][i].name
                sc_b = data['sottocampi'][j].name
                count_a = unit_count[sc_a]
                count_b = unit_count[sc_b]

                model += (count_a - count_b <= self.allowed_delta, f"balance_up_{sc_a}_{sc_b}")
                model += (count_b - count_a <= self.allowed_delta, f"balance_down_{sc_a}_{sc_b}")