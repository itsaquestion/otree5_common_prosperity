import itertools
import random

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
    LUCKY_ROLE = 'Lucky Role'
    UNLUCKY_ROLE = 'Unlucky Role'


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

    for g in subsession.get_groups():

        # 每个组随机分配是否提示
        # 采用循环模式

        # 如果在配置中指定了show_tips与否，则按配置
        # 否则，则循环分配tip
        if 'show_tips' in subsession.session.config:
            g.tip = subsession.session.config['show_tips']
        else:
            g.tip = next(tips)

        # 每组参与人按角色分配初始财富

        for p in g.get_players():
            if p.role == C.LUCKY_ROLE:
                p.wealth = max(C.ED_LIST)
            else:
                p.wealth = min(C.ED_LIST)


class Group(BaseGroup):
    tip = models.BooleanField()
    plan = models.StringField()


class Player(BasePlayer):
    wealth = models.IntegerField()
    partner_wealth = models.IntegerField()

    choice = models.StringField(
        choices=['A', 'B'],
        widget=widgets.RadioSelect,
        label='你的选择是？'
    )

    partner_choice = models.StringField()


class Intro(Page):
    pass


class Agreement(Page):
    """一致同意页面"""
    form_model = 'player'
    form_fields = ['choice']


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

    if group.plan == 'B':
        output = (p1.wealth + p2.wealth) * C.M

        group.get_player_by_role(C.LUCKY_ROLE).wealth = output
        group.get_player_by_role(C.UNLUCKY_ROLE).wealth = 0

    for p in group.get_players():
        p.partner_wealth = p.get_others_in_group()[0].wealth

        p.participant.vars['wealth'] = p.wealth
        p.participant.vars['partner_wealth'] = p.partner_wealth
        p.participant.vars['choice'] = p.choice
        p.participant.vars['plan'] = group.plan


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = production


class Results(Page):
    form_model = 'player'
    form_fields = ['choice', 'partner_choice']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(plan=player.group.plan)


page_sequence = [Intro, Agreement, ResultsWaitPage, Results]
