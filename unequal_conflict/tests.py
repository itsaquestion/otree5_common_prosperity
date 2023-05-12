from otree.api import Currency as c, currency_range, expect, Bot
from . import *

import random


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield Intro

        yield Bid, dict(bid=random.randint(10, 90))

        yield Result
