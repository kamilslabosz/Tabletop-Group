import random
import requests
from bs4 import BeautifulSoup

BGG_COLLECTION_URL = 'https://boardgamegeek.com'

# ------------------ROOT BOARDGAME------------------


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


def root_exclude_factions(reach_dict, factions_to_exclude):
    for key in factions_to_exclude:
        if factions_to_exclude[key]:
            reach_dict.pop(key, None)
            if key == "Vagabond (both)":
                reach_dict.pop('Vagabond')
                reach_dict.pop('2nd Vagabond', None)
    return reach_dict


def check_reach_vs_player_num(players, reach_dict):
    reach_sums = {
        2: 17, 3: 18, 4: 21, 5: 25, 6: 28,
    }
    num_players = int(players)

    if len(reach_dict) < num_players:
        reach_ok = False
    else:

        sorted_reach = sorted(reach_dict.values())
        reach = 0
        print(sorted_reach)
        for num in range(1, num_players+1):
            reach += sorted_reach[-num]
        print(reach)
        if reach < reach_sums[num_players]:
            reach_ok = False
        else:
            reach_ok = True

    return reach_ok


def root_assign_faction(reach, players):
    try:
        available_factions = reach.copy()
    except AttributeError:
        return False
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


# -------------------BOARDGAME COLLECTION--------------------------------------


def get_collection_from_bgg(user):
    response = requests.get(url=f"{BGG_COLLECTION_URL}/collection/user/{user}")

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find('table', 'collection_table')
    all_tr = soup.find_all('tr')
    # slicing redundant tables
    games_list = all_tr[16:]
    game_collection = {}
    for game in games_list:
        link_html = game.findNext('a', class_='primary')
        link = link_html.get('href')
        status_html = game.findNext('td', class_='collection_status').find('div', class_='owned')
        try:
            status = status_html.string
            response = requests.get(url=f"{BGG_COLLECTION_URL}{link}")
            soup = BeautifulSoup(response.text, "html.parser")
            name_html = soup.find('title')
            name = name_html.string.replace(' | Board Game | BoardGameGeek', '')
            link = f"{BGG_COLLECTION_URL}{link}"
            game_collection[link] = name
        except AttributeError:
            pass

    return game_collection




