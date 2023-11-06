import requests
import operator
from player import Player

class PlayerReader:
    def __init__(self, url):
        self.url = url
        self.players = self.get_players()

    def get_players(self):
        response = requests.get(self.url).json()
        players = [Player(player_dict) for player_dict in response]
        return players
            
class PlayerStats: 
    def __init__(self, players: PlayerReader):
        self.playerList = players.players
        
    def top_scorers_by_nationality(self, nationality):
        nat_list = [player for player in self.playerList if player.nationality == nationality]
        return sorted(nat_list, key=operator.attrgetter("total"), reverse=True)

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2022-23/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality("FIN")

    for player in players:
        print(player)

if __name__ == "__main__":
    main()