import random

from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'holt_risk'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    TITLE = '任务一'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_choice(i):
    lottery = models.StringField(
        choices=[
            ['A', f'{i * 10}%概率获得20代币，{100 - i * 10}%概率获得16代币'],
            ['B', f'{i * 10}%概率获得39.5代币，{100 - i * 10}%概率获得1代币']
        ],
        widget=widgets.RadioSelect,
        label=str(i)
    )
    return lottery


class Player(BasePlayer):
    lottery_1 = make_choice(1)
    lottery_2 = make_choice(2)
    lottery_3 = make_choice(3)
    lottery_4 = make_choice(4)
    lottery_5 = make_choice(5)
    lottery_6 = make_choice(6)
    lottery_7 = make_choice(7)
    lottery_8 = make_choice(8)
    lottery_9 = make_choice(9)
    lottery_10 = make_choice(10)


# PAGES
class Lottery(Page):
    form_model = Player
    form_fields = [f'lottery_{i}' for i in range(1, 11)]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        i = random.choice(list(range(1, 11)))
        choice = getattr(player, "lottery_" + str(i))
        profit = 0.0

        if choice == "A":
            profit = 20 if random.random() < i / 10 else 16
        else:
            profit = 39.5 if random.random() < i / 10 else 1

        player.participant.vars[C.NAME_IN_URL] = dict(i=i, choice=choice, profit=profit)


page_sequence = [Lottery]
