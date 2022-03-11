import random


def root_available_factions(riverfolk=False, underworld=False, marauder=False):

    reach = {
        "Marquise de Cat": 10,
        "Eyrie Dynasties": 7,
        "Vagabond": 5,
        "Woodland Alliance": 3,
    }

    if riverfolk:
        reach.update({
            "Riverfolk Company": 5,
            "Lizard Cult": 2,
            "2nd Vagabond": 2,
        })
    if underworld:
        reach.update({
            "Underground Duchy": 8,
            "Corvid Conspiracy": 3,
        })
    if marauder:
        reach.update({
            "Lord of the Hundreds": 9,
            "Keepers in Iron": 8,
        })

    return reach


def root_assign_faction(reach, players):
    available_factions = reach.copy()
    reach_sums = {
        2: 17, 3: 18, 4: 21, 5: 25, 6: 28,
    }
    num_of_players = len(players)
    print(num_of_players)
    reach_left = reach_sums[num_of_players]
    print(f"reach {reach_left}")
    assigned_factions = {}

    random.shuffle(players)
    for player in players:
        faction = random.choice(list(available_factions.keys()))
        if faction == "2nd Vagabond" and "Vagabond" in available_factions.keys():
            faction = 'Vagabond'
        print(faction)
        reach_left -= available_factions[faction]
        del available_factions[faction]
        assigned_factions[player] = faction
    print(f'reach_left: {reach_left}')
    if reach_left > 0:
        assigned_factions = root_assign_faction(reach, players)
    print(assigned_factions)
    return assigned_factions


class RootScripts:
    pass