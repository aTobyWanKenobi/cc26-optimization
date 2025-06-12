import yaml
from pathlib import Path
from opt_sottocampi.models.unit import Unit
from opt_sottocampi.models.sottocampo import Sottocampo
from opt_sottocampi.constraints.unit_balance_constraints import BalanceUnitsPerSottocampoConstraint
from opt_sottocampi.constraints.forest_constraint import ForestConstraint
from opt_sottocampi.constraints.zone_constraint import ZoneDiversityConstraint, MaxZoneUnitsPerSottocampoConstraint
from opt_sottocampi.constraints.friend_constraint import FriendUnitConstraint
from opt_sottocampi.solver.optimizer import run_optimization

def load_config(path: str):
    with open(path, 'r') as f:
        raw = yaml.safe_load(f)

    units = [Unit(**unit_data) for unit_data in raw['units']]
    sottocampi = [Sottocampo(**sc_data) for sc_data in raw['sottocampi']]
    return {"units": units, "sottocampi": sottocampi}

def main():
    data = load_config("opt_sottocampi/data/input.yaml")

    constraints = [
        FriendUnitConstraint(min_num_friends=0),
        BalanceUnitsPerSottocampoConstraint(allowed_delta=2),
        ForestConstraint(tolerance=5),
        ZoneDiversityConstraint(min_zones_per_sc=3, max_zones_per_sc=4),
        MaxZoneUnitsPerSottocampoConstraint(max_zone_units_per_sc=10)
    ]
    result = run_optimization(data, constraints, time_limit=5)

    print("\nAssignment Result:")
    tot_partecipanti = sum(unit.total_participants for unit in data["units"])
    print(f"\tTotale partecipanti: {tot_partecipanti}\n")
        
    for sc in data['sottocampi']:
        tot_unita = 0
        tot_sottocampo = 0
        tot_foresta = 0
        dist_zone = {}
        print(sc)
        print(f"Lista unità:")
        for unit_name, (unit, sottocampo) in result.items():
            if sottocampo.name == sc.name:
                print(unit)
                tot_unita += 1
                tot_sottocampo += unit.total_participants
                tot_foresta += unit.forest_requirement
                dist_zone[unit.zone.value] = dist_zone.get(unit.zone.value, 0) + 1
        print(f"Totale unità sottocampo: {tot_unita}/{len(data['units'])}")
        print(f"Totale partecipanti sottocampo: {tot_sottocampo}/{tot_partecipanti} ({100*tot_sottocampo/tot_partecipanti:.1f}%)")
        print(f"Gettoni bosco usati: {tot_foresta}/{sc.forest_slots}")
        print(f"Distribuzione zone: {dist_zone}")
        print()
        

if __name__ == "__main__":
    main()
