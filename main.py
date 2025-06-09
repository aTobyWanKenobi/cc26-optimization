import yaml
from pathlib import Path
from opt_sottocampi.models.unit import Unit
from opt_sottocampi.models.sottocampo import Sottocampo
from opt_sottocampi.constraints.capacity_constraint import CapacityConstraint
from opt_sottocampi.constraints.forest_constraint import ForestConstraint
from opt_sottocampi.constraints.zone_constraint import ZoneDiversityConstraint
from opt_sottocampi.solver.optimizer import run_optimization

def load_config(path: str):
    with open(path, 'r') as f:
        raw = yaml.safe_load(f)

    units = [Unit(**unit_data) for unit_data in raw['units']]
    sottocampi = [Sottocampo(**sc_data) for sc_data in raw['sottocampi']]
    return {"units": units, "sottocampi": sottocampi}

def main():
    data = load_config("opt_sottocampi/data/input.yaml")

    capacity_distribution = {
        "HDX": 0.25,
        "HSX": 0.25,
        "LDX": 0.25,
        "LSX": 0.25
    }

    constraints = [
        #CapacityConstraint(capacity_distribution),
        ForestConstraint(),
        ZoneDiversityConstraint(min_units_per_zone=1)
    ]
    
    result = run_optimization(data, constraints, capacity_distribution, 60)

    print("\nAssignment Result:")
    tot_partecipanti = sum(unit.total_participants for unit in data["units"])
    print(f"\tTotale partecipanti: {tot_partecipanti}\n")
        
    for sc in data['sottocampi']:
        tot_sottocampo = 0
        tot_foresta = 0
        dist_zone = {}
        print(f"Sottocampo {sc.name} - Capacità {100*capacity_distribution[sc.name]:.1f} % - Gettoni bosco = {sc.forest_slots/10}")
        print(f"Lista unità sottocampo {sc.name}")
        for unit_name, (unit, sottocampo) in result.items():
            if sottocampo.name == sc.name:
                print(f"\tUnit {unit.name} ({unit.total_participants}) → {sottocampo.name}")
                tot_sottocampo += unit.total_participants
                tot_foresta += unit.forest_requirement
                dist_zone[unit.zone] = dist_zone.get(unit.zone, 0) + 1
        print(f"Totale partecipanti sottocampo: {tot_sottocampo}/{tot_partecipanti} ({100*tot_sottocampo/tot_partecipanti:.1f}%)")
        print(f"Gettoni bosco usati: {tot_foresta/10}/{sc.forest_slots/10}")
        print(f"Distribuzione zone: {dist_zone}")
        print()
        

if __name__ == "__main__":
    main()
