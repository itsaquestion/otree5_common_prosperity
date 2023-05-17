import itertools
import random
import pandas as pd

from otree.api import *

doc = """
一致同意博弈
"""


class C(BaseConstants):
    NAME_IN_URL = 'agreement'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    ED_LIST = [200, 100]

    M = 2

    # 2个角色
    # LUCKY_ROLE = 'Lucky Role'
    # UNLUCKY_ROLE = 'Unlucky Role'

    # endowment
    ED = dict(high=200,
              low=100)

    # productivity
    PROD = [1, 2, 3]

    # transfer
    TRANS = dict(higer=0.7,
                 high=0.5,
                 low=0.25,
                 lower=0.10)

    # 参数表
    PARAMS_DF = pd.read_csv('agreement/params.csv').astype(int, errors='ignore')


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    """
    创建session时，乱序，并分配endowment
    """
    p1: Player
    p2: Player
    p: Player
    g: Group

    # 是否乱序看需要
    # subsession.group_randomly()

    tips = itertools.cycle([True, False])

    # 生成一个大列表，按轮次抽取某一行作为参数，或者随机选择一行
    params = C.PARAMS_DF.query(f"round == {subsession.round_number}").iloc[0].to_dict()

    print(f"{params=}")
    for g in subsession.get_groups():
        g.set_prod(params)

    for g in subsession.get_groups():

        # 每个组随机分配是否提示
        # 采用循环模式

        # 如果在配置中指定了show_tips与否，则按配置
        # 否则，则循环分配tip
        if 'show_tips' in subsession.session.config:
            g.tip = subsession.session.config['show_tips']
        else:
            g.tip = next(tips)


class Group(BaseGroup):
    # params = dict()

    plan = models.StringField()
    # X,Y
    endow = models.IntegerField()

    # delta x
    trans = models.FloatField()
    tip = models.BooleanField()

    alpha_x = models.IntegerField()
    beta_y = models.IntegerField()

    # X' Y'
    x2 = models.IntegerField()
    y2 = models.IntegerField()

    alpha_x2 = models.IntegerField()
    beta_y2 = models.IntegerField()

    offer = models.IntegerField()

    def set_prod(self, params):
        """Randomly extract two different values from `C.PROD`
        and set two `player.prod` respectively.
        """
        p1, p2 = self.get_players()

        self.endow = params['x']
        p1.endow = params['x']
        p2.endow = params['y']

        p1.partner_endow = p2.endow
        p2.partner_endow = p1.endow

        p1.prod = params['alpha']
        p2.prod = params['beta']

        p1.partner_prod = p2.prod
        p2.partner_prod = p1.prod

        self.alpha_x = params['alpha_x']
        self.beta_y = params['beta_y']

        self.trans = params['delta_x']

        self.x2 = params['x2']
        self.y2 = params['y2']

        self.alpha_x2 = params['alpha_x2']
        self.beta_y2 = params['beta_y2']

    def calc_player_prop(self):
        """Set player's properties"""
        pass


class Player(BasePlayer):
    # endowment = group.endowment
    endow = models.IntegerField()
    partner_endow = models.IntegerField()

    # productivity
    prod = models.IntegerField()
    partner_prod = models.IntegerField()

    # transfer
    trans = models.FloatField()

    # allocation
    alloc = models.FloatField()

    choice = models.StringField(
        choices=['A', 'B'],
        widget=widgets.RadioSelect,
        label='你的选择是？'
    )

    partner_choice = models.StringField()

    offer = models.IntegerField(label='')


class Intro(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(test=C.PARAMS_DF.to_html(classes='table table-bordered table-hover table-condensed', index=False))


class Agreement(Page):
    """一致同意页面"""
    form_model = 'player'
    form_fields = ['choice']

    @staticmethod
    def vars_for_template(player: Player):
        pass


def set_payoff(group: Group):
    """
    生产方式：
    1. A计划保持财富不变
    2. B计划，双方财富都交给Lucky_Role，乘以系数，由Lucky_Role持有，对方财富为0
    """
    p1, p2 = group.get_players()
    if group.plan == 'B':
        p1.endow = group.alpha_x2
        p2.endow = group.beta_y2
    else:
        p1.endow = group.alpha_x
        p2.endow = group.beta_y


def production(group: Group):
    """
    根据双方的选择
    1. 获得应该采用的Plan
    2. 必要的信息放到

    """
    p1: Player
    p2: Player
    p: Player

    # 记录双方的选择
    p1, p2 = group.get_players()
    p1.partner_choice = p2.choice
    p2.partner_choice = p1.choice

    # 计算plan
    if any([p.choice == 'A' for p in group.get_players()]):
        group.plan = 'A'
    else:
        group.plan = 'B'

    # 如果是方案A，则技术=1，产出等于禀赋

    # 如果是方案B，则：
    # 假定低ed的人，把全部财富给高ed的人
    # 最终产品就是两者的禀赋之和，乘以系数M

    # TODO: 这里等于假定，禀赋高的人，同时乘数也大

    set_payoff(group)

    for p in group.get_players():
        p.partner_endow = p.get_others_in_group()[0].endow

        p.participant.vars['endow'] = p.endow
        p.participant.vars['partner_endow'] = p.partner_endow
        p.participant.vars['choice'] = p.choice
        p.participant.vars['partner_choice'] = p.partner_choice
        p.participant.vars['plan'] = group.plan


class AgreementResultsWaitPage(WaitPage):
    after_all_players_arrive = production


class AgreementResults(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(plan=player.group.plan)


def offer_max(player):
    return max(player.endow, player.partner_endow)


class Offer(Page):
    form_model = 'player'
    form_fields = ['offer']

    @staticmethod
    def is_displayed(player: Player):
        # return player.endow > player.partner_endow
        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        partner = player.get_others_in_group()[0]
        player.payoff = player.endow - player.offer
        partner.payoff = partner.endow + player.offer



        # player.group.transfer = player.offer


class OfferResultsWaitPage(WaitPage):
    pass


class OfferResult(Page):
    pass


page_sequence = [Intro, Agreement, AgreementResultsWaitPage, AgreementResults, Offer, OfferResultsWaitPage, OfferResult]
