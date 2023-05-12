from otree.api import Currency as c, currency_range, expect, Bot
from . import *

import random


class PlayerBot(Bot):

    def play_round(self):
        x = random.randint(0, 40)
        yield Offer, dict(self_receive=x, other_receive=50 - x)
