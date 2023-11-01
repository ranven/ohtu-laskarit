from enum import Enum
import unittest
from statistics_service import StatisticsService
from player import Player


class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]


class SortBy(Enum):
    POINTS = 1
    GOALS = 2
    ASSISTS = 3


class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(PlayerReaderStub())

    def test_top_points_works(self):
        top_list = self.stats.top(4, SortBy.POINTS)
        self.assertEqual(top_list[0].name, "Gretzky")
        self.assertEqual(top_list[4].name, "Semenko")

    def test_top_goals_works(self):
        top_list = self.stats.top(4, SortBy.GOALS)
        self.assertEqual(top_list[0].name, "Lemieux")
        self.assertEqual(top_list[4].name, "Semenko")

    def test_top_assists_works(self):
        top_list = self.stats.top(4, SortBy.ASSISTS)
        self.assertEqual(top_list[0].name, "Gretzky")
        self.assertEqual(top_list[4].name, "Semenko")

    def test_team_works(self):
        team = self.stats.team("EDM")
        self.assertEqual(len(team), 3)

    def test_player_search_works(self):
        player = self.stats.search("Kurri")
        self.assertEqual(player.name, "Kurri")

    def test_player_search_no_result_works(self):
        player = self.stats.search("Jesus")
        self.assertEqual(player, None)
