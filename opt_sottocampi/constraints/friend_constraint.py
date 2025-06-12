from opt_sottocampi.constraints.base import BaseConstraint

class FriendUnitConstraint(BaseConstraint):
    
    def __init__(self, min_num_friends: int):
        self.min_num_friends = min_num_friends

    def apply(self, model, var_assignements, var_zone_in_sc, data):
        for sc in data['sottocampi']:
            for u in data['units']:
                same_zone_others = [v for v in data['units'] if v.zone == u.zone and v != u]
                model += (
                    self.min_num_friends*var_assignements[u.name, sc.name] <= sum(var_assignements[v.name, sc.name] for v in same_zone_others),
                    f"friend_unit_{u.name}_{sc.name}"
                )
