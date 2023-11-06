import requests
import operator
from player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2022-23/players"
    response = requests.get(url).json()

    players = []

    for player_dict in response:
        player = Player(player_dict)
        if player.nationality == "FIN":
            players.append(player)
    new_players = sorted(players, key=operator.attrgetter("total"), reverse=True)
            
    print("Players from FIN")
    for player in new_players:
        print(player)

if __name__ == "__main__":
    main()