import random
import os

from otree.api import *

from unequal_conflict import get_matches
from utils import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'dictator'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def creating_session(subsession: Subsession):
    p: Player

    set_endowment(subsession)

    subsession.set_group_matrix(get_matches())

    for p in subsession.get_players():
        # p.is_winner = False

        p.endowment = p.participant.wealth
        # p.tag = p.participant.tag
        p.chosen = False

    for p in subsession.get_players():
        p.partner_id = p.get_others_in_group()[0].id_in_subsession

    for p in subsession.get_players():
        p.partner_endowment = p.get_others_in_group()[0].endowment
        p.participant.vars['p_endowment'] = p.partner_endowment


class Player(BasePlayer):
    endowment = models.CurrencyField()
    partner_endowment = models.CurrencyField()
    partner_id = models.IntegerField()

    chosen = models.BooleanField(value=False)

    self_receive = models.CurrencyField(max=50)
    other_receive = models.CurrencyField(max=50)
    partner_offer = models.CurrencyField()


# PAGES
class Offer(Page):
    form_model = Player
    form_fields = [
        'self_receive',
        'other_receive'
    ]


def set_payoffs(group: Group):
    p1: Player = group.get_players()[0]
    p2: Player = group.get_players()[1]

    p1.partner_offer = p2.other_receive
    p2.partner_offer = p1.other_receive

    p1.chosen = False
    p2.chosen = False

    if random.random() < 0.5:
        p1.chosen = True
        p1.payoff = p1.self_receive
        p2.payoff = p1.other_receive
    else:
        p2.chosen = True
        p2.payoff = p2.self_receive
        p1.payoff = p2.other_receive

    p1vars = p1.participant.vars
    p2vars = p2.participant.vars

    p1vars['dg_self_receive'] = p1.self_receive
    p1vars['dg_partner_offer'] = p1.partner_offer
    p1vars['dg_payoff'] = p1.payoff
    p1vars['dg_chosen'] = p1.chosen

    dg_save_json(p1)

    p2vars['dg_self_receive'] = p2.self_receive
    p2vars['dg_partner_offer'] = p2.partner_offer
    p2vars['dg_payoff'] = p2.payoff
    p2vars['dg_chosen'] = p2.chosen

    dg_save_json(p2)


def dg_save_json(player: Player):
    p_dir = "participant_data"

    if not os.path.exists(p_dir):
        os.mkdir(p_dir)

    data = dict(dg_payoff=float(player.payoff),
                dg_chosen=player.chosen)

    save_to_json(data, os.path.join(p_dir, f'{player.participant.code}.json'))


class WaitForPartner(WaitPage):
    after_all_players_arrive = set_payoffs


page_sequence = [
    Offer,
    WaitForPartner
]
