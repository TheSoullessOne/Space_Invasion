from text_box import TextBox


class GameStats:
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.high_score_active = False
        self.get_initials = False
        self.game_over = False
        self.high_score = 0
        self.level = 1
        self.initials = ''

        self.get_high_score()

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0

    def get_high_score(self):
        f = open("high_score.txt", "r")
        score = f.readline()
        score_int = score.split(' ')
        self.high_score = int(score_int[0])
        f.close()

    def set_high_score(self):
        with open('high_score.txt') as f:
            high_scores_list = []
            score = f.readline()
            while score:
                score_list = score.split(' ')
                score_tuple = (int(score_list[0]), score_list[1])
                high_scores_list.append(score_tuple)
                score = f.readline()
                if score == "\n":
                    break

        higher = False
        for score, init in high_scores_list:
            if self.score > score:
                higher = True
                high_scores_list.append((self.score, self.initials + '\n'))
                break
        f.close()
        if not higher and len(high_scores_list) < 10:
            high_scores_list.append((self.score, self.initials + '\n'))

        high_scores_list.sort(reverse=True)
        if len(high_scores_list) == 11:
            del high_scores_list[10]

        with open('high_score.txt', 'w+') as f:
            for score, init in high_scores_list:
                f.write(str(score) + ' ' + init)
        f.close()

    def show_high_scores(self, ai_settings, screen, stats):
        with open('high_score.txt') as f:
            high_scores_list = []
            score = f.readline()
            while score:
                score_list = score.split(' ')
                score_tuple = (int(score_list[0]), score_list[1])
                high_scores_list.append(score_tuple)
                score = f.readline()
                if score == "\n":
                    break
        f.close()

        high_score_text = TextBox(ai_settings, screen, stats)
        high_score_text.update_text("HIGH SCORES!")
        high_score_text.text_rect.top = screen.get_rect().top + 50
        high_score_text.text_rect.centerx = screen.get_rect().centerx
        high_score_text.update_font('arial', 80)
        high_score_text.draw(screen)

        count = 0
        text_list = []
        for score, init in high_scores_list:
            text_render = TextBox(ai_settings, screen, stats)
            text_render.update_text(str(score) + '  ' + init.rstrip())
            text_render.text_rect.top = 200 + count * 50
            text_render.text_rect.centerx = screen.get_rect().centerx
            text_list.append(text_render)
            count += 1

        for i in text_list:
            i.draw(screen)

    def set_initials(self, string):
        self.initials = string
