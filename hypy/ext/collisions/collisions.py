from typing import Set
from ...abc import HypyIterable


def player_collisions(party1: HypyIterable, party2: HypyIterable) -> Set[str]:
    """Returns collisions of people between 2 Objects"""
    parties = []
    for i in [party1, party2]:
        parties.append([x.no_dashes for x in i.iter_uuids()])
    return set(set(parties[0]).intersection(parties[1]))
