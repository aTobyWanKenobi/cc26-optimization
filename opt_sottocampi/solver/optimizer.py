from opt_sottocampi.constraints.capacity_constraint import CapacityConstraint
from pulp import LpProblem, LpVariable, LpBinary, LpMinimize, lpSum, LpStatus, PULP_CBC_CMD

def run_optimization(data, constraints, capacity_distribution, time_limit):
    model = LpProblem("Scout_Camp_Assignment", LpMinimize)

    print(capacity_distribution)
    print()

    units = data['units']
    print(units)
    print()

    sottocampi = data['sottocampi']
    print(sottocampi)
    print()
    
    # Decision variables: unit i assigned to sottocampo j
    variables = {
        (unit.name, sc.name): LpVariable(f"{unit.name}_{sc.name}", cat=LpBinary)
        for unit in units for sc in sottocampi
    }
    print(variables)
    print()

    # Each unit must go to exactly one sottocampo
    for unit in units:
        model += lpSum(variables[unit.name, sc.name] for sc in sottocampi) == 1, f"Assign_{unit.name}"

    # Apply constraints
    for constraint in constraints:
        constraint.apply(model, variables, data)
    
    print(constraints)
    print()

    # Objective: minimize absolute imbalance from target distribution
    imbalance_vars = []
    total_participants = sum(unit.total_participants for unit in units)
    print(f"Total participants: {total_participants}")

    for sc in sottocampi:
        assigned = lpSum(variables[unit.name, sc.name] * unit.total_participants for unit in units)
        target = capacity_distribution[sc.name] * total_participants

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
        unit.name: (unit, next(sc for sc in sottocampi if variables[unit.name, sc.name].varValue == 1))
        for unit in units
    }
    return result