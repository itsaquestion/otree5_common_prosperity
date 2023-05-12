import random

from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'eckel_risk'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    LOTTERIES = [
        [20, 20],
        [16, 28],
        [12, 36],
        [8, 44],
        [4, 52],
        [-2, 58]
    ]



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    lottery_choice = models.IntegerField(
        choices=list(range(1, 7)),
        widget=widgets.RadioSelectHorizontal
    )


# PAGES
class Lottery(Page):
    form_model = Player
    form_fields = ['lottery_choice']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        lottery = C.LOTTERIES[player.lottery_choice - 1]
        player.payoff = lottery[0] if random.random() < 0.5 else lottery[1]

        player.participant.vars['risk_choice'] = player.lottery_choice
        player.participant.vars['risk_payoff'] = player.payoff


page_sequence = [Lottery]
