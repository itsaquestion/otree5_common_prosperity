from otree.api import *

doc = """
One player decides how to divide a certain amount between himself and the other
player.
See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.
"""


class C(BaseConstants):
    NAME_IN_URL = 'dictator'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    transfer = models.IntegerField()


def offer_max(player):
    return player.wealth


class Player(BasePlayer):
    wealth = models.IntegerField()
    partner_wealth = models.IntegerField()

    offer = models.IntegerField(
        doc="""Amount dictator decided to keep for himself""",
        min=0,
        label="我会向另一位参与人支付",
        initial=0
    )


# PAGES
class Intro(Page):

    @staticmethod
    def is_displayed(player: Player):
        player.wealth = player.participant.vars['wealth']
        player.partner_wealth = player.participant.vars['partner_wealth']
        return True


class Offer(Page):
    form_model = 'player'
    form_fields = ['offer']

    @staticmethod
    def is_displayed(player: Player):
        return player.wealth > player.partner_wealth

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        partner = player.get_others_in_group()[0]
        player.payoff = player.wealth - player.offer
        partner.payoff = partner.wealth + player.offer
        player.group.transfer = player.offer


class ResultsWaitPage(WaitPage):
    # after_all_players_arrive = set_payoffs
    pass


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(transfer=player.group.transfer)


page_sequence = [Intro, Offer, ResultsWaitPage, Results]
