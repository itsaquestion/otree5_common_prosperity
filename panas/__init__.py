from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'panas'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    LOTTERIES = [
        [20, 20],
        [16, 28],
        [12, 36],
        [8, 44],
        [4, 52],
        [-2, 58]
    ]



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass



def make_q(label):
    return models.IntegerField(label=label, choices=[1, 2, 3, 4, 5], widget=widgets.RadioSelect)


class Player(BasePlayer):
    interested = make_q('感兴趣的')
    distressed = make_q('心烦的')
    excited = make_q('精神活力高的')
    upset = make_q('心神不宁的')
    strong = make_q('劲头足的')
    guilty = make_q('内疚的')
    scared = make_q('恐惧的')
    hostile = make_q('敌意的')
    enthusiastic = make_q('热情的')
    proud = make_q('自豪的')
    irritable = make_q('易怒的')
    alert = make_q('警觉性高的')
    ashamed = make_q('害羞的')
    inspired = make_q('备受鼓舞的')
    nervous = make_q('紧张的')
    determined = make_q('意志坚定的')
    attentive = make_q('注意力集中的')
    jittery = make_q('坐立不安的')
    active = make_q('有活力的')
    afraid = make_q('害怕的')


# PAGES
class Survey(Page):
    form_model = Player
    form_fields = [
        'interested',
        'distressed',
        'excited',
        'upset',
        'strong',
        'guilty',
        'scared',
        'hostile',
        'enthusiastic',
        'proud',
        'irritable',
        'alert',
        'ashamed',
        'inspired',
        'nervous',
        'determined',
        'attentive',
        'jittery',
        'active',
        'afraid',
    ]


page_sequence = [Survey]
