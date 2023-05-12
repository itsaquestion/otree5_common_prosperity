import os
import random

from otree.api import *

from utils import read_json

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'results_payment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    risk_payoff = models.CurrencyField()
    joy_payoff = models.CurrencyField()
    uc_payoff = models.CurrencyField()
    uc_pay_rounds = models.StringField()
    dg_payoff = models.CurrencyField()
    dg_chosen = models.BooleanField()
    final_payoff = models.CurrencyField()
    final_payment_cny_plus_fee = models.CurrencyField()


def read_dg_data(player: Player):
    p_dir = "participant_data"

    data = read_json(os.path.join(p_dir, f'{player.participant.code}.json'))

    return data


class Results(Page):

    @staticmethod
    def vars_for_template(player: Player):
        p_vars = player.participant.vars

        player.risk_payoff = p_vars['risk_payoff']
        player.joy_payoff = p_vars['joy_payoff']
        player.uc_payoff = p_vars['uc_payoff']
        player.uc_pay_rounds = ', '.join([str(i) for i in p_vars['uc_pay_rounds']])

        # player.dg_chosen = p_vars['dg_chosen']
        # player.dg_payoff = p_vars['dg_payoff']

        dg_data = read_dg_data(player)

        player.dg_chosen = dg_data['dg_chosen']
        player.dg_payoff = dg_data['dg_payoff']

        payoff_list = [
            p_vars['risk_payoff'],
            p_vars['joy_payoff'],
            p_vars['uc_payoff'],
            player.dg_payoff
        ]

        # uc必选，risk和dg抽一个
        pay_tasks = [2, random.choice([0, 3])]
        pay_tasks.sort()

        pay_tasks_1 = [i + 1 for i in pay_tasks]

        player.participant.payoff = 0
        for i in pay_tasks:
            player.participant.payoff += payoff_list[i]

        player.final_payoff = player.participant.payoff

        player.final_payment_cny_plus_fee = player.participant.payoff_plus_participation_fee()

        return dict(dg_is_winner=player.dg_chosen,
                    dg_payoff=player.dg_payoff,
                    final_payment_cny=player.final_payment_cny_plus_fee,
                    pay_tasks_1=pay_tasks_1
                    )


page_sequence = [Results]
