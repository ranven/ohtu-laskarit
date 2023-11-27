
game_status = ["Love", "Fifteen", "Thirty", "Forty"]


class TennisGame:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.score1 = 0
        self.score2 = 0

    def won_point(self, player_name):
        if player_name == self.player1:
            self.score1 = self.score1 + 1
        else:
            self.score2 = self.score2 + 1

    def get_score(self):
        if self.score1 == self.score2:
            return self.tie()

        elif self.score1 >= 4 or self.score2 >= 4:
            difference = self.score1 - self.score2

            if difference > 1 or difference < -1:
                return self.win(difference)
            else:
                return self.advantage(difference)
        else:
            return f"{game_status[self.score1]}-{game_status[self.score2]}"

    def win(self, difference):
        if difference >= 2:
            return "Win for player1"
        else:
            return "Win for player2"

    def advantage(self, difference):
        if difference == 1:
            return "Advantage player1"
        elif difference == -1:
            return "Advantage player2"

    def tie(self):
        if self.score1 > 3:
            return "Deuce"
        else:
            return f"{game_status[self.score1]}-All"
