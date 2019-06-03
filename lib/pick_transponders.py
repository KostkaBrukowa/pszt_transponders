from typing import Set, List, Tuple


def pick_transponders(bitrate: float, path_length: float, transponders, weakest_band):
    '''
    Pick transponders only based on demand. Doesn't take into account 
    frequencies and bands.
    Assumes that transponders are sorted by bitrate ascending
    '''
    available_transponders = [
        t for t in transponders if t.power_budget > path_length * weakest_band.loss_per_km]

    if len(available_transponders) == 0:
        return []

    biggest_transponder = available_transponders[-1]
    biggest_transponders_number = int(
        bitrate // biggest_transponder.bitrate)
    picked_transponders = [biggest_transponder] * biggest_transponders_number

    rest_bitrate = bitrate % biggest_transponder.bitrate
    if rest_bitrate == 0:
        return picked_transponders

    for transponder in available_transponders:
        if transponder.bitrate >= rest_bitrate:
            picked_transponders.append(transponder)
            break

    return picked_transponders