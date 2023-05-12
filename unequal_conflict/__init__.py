import random

from otree.api import *

from unequal_conflict.matching_device import get_matches
from unequal_conflict.tullock import *
from utils import set_endowment

doc = """
unequal conflict
"""


class C(BaseConstants):
    NAME_IN_URL = 'unequal_conflict'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 20

    ENDOWMENT = [90, 180, 540]

    REWARD = 180

    PAY_ROUNDS_NUM = 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    endowment = models.CurrencyField()

    tag = models.StringField()  # 匹配用的ABCD标签

    reward = models.CurrencyField(default=C.REWARD)

    partner_id = models.IntegerField()

    partner_endowment = models.CurrencyField()

    bid = models.CurrencyField(min=0, label="你的出价是：（代币，请填整数）")

    partner_bid = models.CurrencyField()

    is_winner = models.BooleanField()

    # pay_rounds = []


def creating_session(subsession: Subsession):
    p: Player

    set_endowment(subsession)

    subsession.set_group_matrix(get_matches())

    for p in subsession.get_players():
        p.is_winner = False

        p.endowment = p.participant.wealth
        p.tag = p.participant.tag

    for p in subsession.get_players():
        p.partner_id = p.get_others_in_group()[0].id_in_subsession

    for p in subsession.get_players():
        p.partner_endowment = p.get_others_in_group()[0].endowment
        p.participant.vars['p_endowment'] = p.partner_endowment


def bid_max(player: Player):
    """
    bid的上限
    """
    return player.endowment


def set_payoffs(group: Group):
    p1, p2 = group.get_players()

    p1.partner_bid = p2.bid
    p2.partner_bid = p1.bid

    # 如果x和y为otree的currency类型，相除只能得到整形，必须先转为浮点
    if random.random() < tullock(float(p1.bid), float(p2.bid)):
        p1.is_winner = True
    else:
        p2.is_winner = True

    p: Player
    for p in group.get_players():
        p.payoff = p.endowment - p.bid + (p.reward if p.is_winner else 0)


class WaitForPartner(WaitPage):
    after_all_players_arrive = set_payoffs


class Result(Page):
    pass


class FinalWaitPage(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        if player.round_number == C.NUM_ROUNDS:

            pay_rounds = random.sample(range(1, C.NUM_ROUNDS + 1), min(C.PAY_ROUNDS_NUM, C.NUM_ROUNDS))
            pay_rounds.sort()
            player.participant.vars['uc_pay_rounds'] = pay_rounds

            # player.participant.payoff = 0
            total_payoff = 0
            for i in pay_rounds:
                total_payoff += player.in_round(i).payoff

            player.participant.vars['uc_payoff'] = total_payoff / len(pay_rounds)

        return player.round_number == C.NUM_ROUNDS


class FinalResult(Page):
    """
    存档
    """
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return dict(pay_rounds=player.participant.vars['pay_rounds'],
                    total_payoff=player.participant.payoff)


class Bid(Page):
    form_model = 'player'
    form_fields = ['bid']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(a=1)


class Intro(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


page_sequence = [
    Intro,
    Bid,
    WaitForPartner,
    Result,
    FinalWaitPage
    #    FinalResult
]
