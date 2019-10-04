class GameStats:
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.high_score_active = False
        self.high_score = 0
        self.level = 1

        self.get_high_score()

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0

    def get_high_score(self):
        f = open("high_score.txt", "r")
        self.high_score = int(f.read())
        f.close()

    def set_high_score(self):
        f = open("high_score.txt", "w+")
        f.write(str(self.high_score))
        f.close()
