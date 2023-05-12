import string
from otree.api import *

doc = """
unequal conflict
"""


class C(BaseConstants):
    NAME_IN_URL = 'preface'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    pass


class Player(BasePlayer):
    pass


class Group(BaseGroup):
    pass


class Intro(Page):
    pass


class Understand(Page):
    pass


class Preface(Page):
    pass


page_sequence = [
    Preface]
