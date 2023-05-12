from unequal_conflict import *


class C(C):
    NAME_IN_URL = 'unequal_conflict_joy'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    REWARD = 0


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


def set_payoffs_and_upload(group: Group):
    set_payoffs(group)

    for player in group.get_players():
        player.participant.vars['joy_bid'] = player.bid
        player.participant.vars['joy_is_winner'] = player.is_winner
        player.participant.vars['joy_payoff'] = player.payoff


class WaitForPartner(WaitPage):
    after_all_players_arrive = set_payoffs_and_upload


class Bid(Page):
    form_model = 'player'
    form_fields = ['bid']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['joy_bid'] = player.bid
        player.participant.vars['joy_is_winner'] = player.is_winner
        player.participant.vars['joy_payoff'] = player.payoff


page_sequence = [
    Bid,
    WaitForPartner
]
