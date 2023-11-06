class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.nationality = dict['nationality']
        self.assists = dict['assists']
        self.goals = dict['goals']
        self.penalties = dict['penalties']
        self.team = dict['team']
        self.games = dict['games']
        self.total = self.assists + self.goals
    
    def __str__(self):
        return(f"{self.name:20} {self.team:5} {self.goals:2} + {self.assists:2} = {self.total:2}")
