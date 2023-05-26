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
    pass

class Results(Page):

    @staticmethod
    def vars_for_template(player: Player):
        pass

page_sequence = [Results]
