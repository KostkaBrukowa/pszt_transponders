from typing import Set, List, Tuple
from models.models import Transponder, Demand


def pick_transponders(demand: Demand, transponders: List[Transponder]) -> List[Transponder]:
    '''
    Pick transponders only based on demand. Doesn't take into account 
    frequencies and bands.
    Assumes that transponders are sorted by bitrate ascending
    '''
    biggest_transponder = transponders[-1]
    biggest_transponders_number = int(demand.bitrate / biggest_transponder.bitrate)
    picked_transponders = [biggest_transponder] * biggest_transponders_number

    rest_bitrate = demand.bitrate % biggest_transponder.bitrate
    if rest_bitrate == 0:
        return picked_transponders

    for transponder in transponders:
        if transponder.bitrate >= rest_bitrate:
            picked_transponders.append(transponder)
            break

    return picked_transponders

    # current_bitrate = 0
    # picked_transponders: List[Transponder] = []
    # while current_bitrate < demand.bitrate:
    #     old_bitrate = current_bitrate
    #     for transponder in transponders:
    #         if transponder.bitrate >= demand.bitrate - current_bitrate:
    #             picked_transponders.append(transponder)
    #             current_bitrate += transponder.bitrate
    #             break

    #     if(old_bitrate == current_bitrate):
    #         picked_transponders.append(transponders[-1])
    #         current_bitrate += transponders[-1].bitrate

    return picked_transponders
