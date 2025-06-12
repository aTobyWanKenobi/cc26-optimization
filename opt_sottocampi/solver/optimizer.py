from opt_sottocampi.models.unit import Zone
from pulp import LpProblem, LpVariable, LpBinary, LpMinimize, lpSum, LpStatus, PULP_CBC_CMD

def run_optimization(data, constraints, time_limit):
    model = LpProblem("Scout_Camp_Assignment", LpMinimize)

    units = data['units']
    sottocampi = data['sottocampi']

    # ----------
    # Decision variables: unit i assigned to sottocampo j
    var_assignements = {
        (unit.name, sc.name): LpVariable(f"{unit.name}_{sc.name}", cat=LpBinary)
        for unit in units for sc in sottocampi
    }
    
    # Each unit must go to exactly one sottocampo
    for unit in units:
        model += lpSum(var_assignements[unit.name, sc.name] for sc in sottocampi) == 1, f"Assign_{unit.name}"
    
    # ----------
    # Auxiliary binary variables: zone appears in sottocampo
    var_zone_in_sc = {}
    for zone in Zone:
        for sc in data['sottocampi']:
            var_zone_in_sc[zone, sc.name] = LpVariable(f"var_zone_in_sc_{zone}_{sc.name}", cat="Binary")

    # Link var_zone_in_sc to unit assignments
    for zone in Zone:
        for sc in data['sottocampi']:
            units_in_zone = [u for u in data['units'] if u.zone == zone]
            
            for u in units_in_zone:
                model += (
                    var_zone_in_sc[zone, sc.name] >= var_assignements[u.name, sc.name],
                    f"link_upper_{zone}_{sc.name}_{u.name}"
                )
                
            # Lower bound: if var_zone_in_sc == 1, at least one unit must be assigned
            model += (
                lpSum(var_assignements[u.name, sc.name] for u in units_in_zone) >= var_zone_in_sc[zone, sc.name],
                f"link_lower_{zone}_{sc.name}"
            )

    # ----------
    # Apply constraints
    for constraint in constraints:
        constraint.apply(model, var_assignements, var_zone_in_sc, data)

    # Objective: minimize absolute imbalance from target distribution
    imbalance_vars = []
    total_participants = sum(unit.total_participants for unit in units)
    print(f"Total participants: {total_participants}")

    for sc in sottocampi:
        assigned = lpSum(var_assignements[unit.name, sc.name] * unit.total_participants for unit in units)
        target = sc.capacity * total_participants

        # Create a variable for absolute deviation
        delta = LpVariable(f"imbalance_{sc.name}", lowBound=0)
        model += assigned - target <= delta, f"imbalance_upper_{sc.name}"
        model += target - assigned <= delta, f"imbalance_lower_{sc.name}"
        imbalance_vars.append(delta)

    model += lpSum(imbalance_vars), "MinimizeTotalImbalance"

    # Solve
    model.solve(PULP_CBC_CMD(msg=1, timeLimit=time_limit))
    print(f"Status: {LpStatus[model.status]}")

    result = {
        unit.name: (unit, next(sc for sc in sottocampi if var_assignements[unit.name, sc.name].varValue == 1))
        for unit in units
    }
    return result