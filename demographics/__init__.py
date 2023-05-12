from otree.api import *

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'demographics'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    EDU_LEVELS = [
        [1, '小学及以下'],
        [2, '初中'],
        [3, '高中'],
        [4, '大学及以上']
    ]

    FAM_INCOME_LEVELS = [
        [1, '5万以下'],
        [2, '5万-10万'],
        [3, '10万-25万'],
        [4, '25万-50万'],
        [5, '50万-100万'],
        [6, '100万及以上']

    ]

    ETHNICITY = [
        '汉族',
        '满族',
        '蒙古族',
        '回族',
        '藏族',
        '维吾尔族',
        '苗族',
        '彝族',
        '壮族',
        '布依族',
        '侗族',
        '瑶族',
        '白族',
        '土家族',
        '哈尼族',
        '哈萨克族',
        '傣族',
        '黎族',
        '傈僳族',
        '佤族',
        '畲族',
        '高山族',
        '拉祜族',
        '水族',
        '东乡族',
        '纳西族',
        '景颇族',
        '柯尔克孜族',
        '土族',
        '达斡尔族',
        '仫佬族',
        '羌族',
        '布朗族',
        '撒拉族',
        '毛南族',
        '仡佬族',
        '锡伯族',
        '阿昌族',
        '普米族',
        '朝鲜族',
        '塔吉克族',
        '怒族',
        '乌孜别克族',
        '俄罗斯族',
        '鄂温克族',
        '德昂族',
        '保安族',
        '裕固族',
        '京族',
        '塔塔尔族',
        '独龙族',
        '鄂伦春族',
        '赫哲族',
        '门巴族',
        '珞巴族',
        '基诺族'

    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gender = models.IntegerField(choices=[
        [1, '男'],
        [2, '女']
    ], widget=widgets.RadioSelectHorizontal, label='你的性别：')

    birth_year = models.IntegerField(min=1990, max=2020, label='出生年')
    birth_month = models.IntegerField(min=1, max=12, label='出生月')

    ethnicity = models.StringField(choices=C.ETHNICITY, label="你的民族：")

    party_member = models.BooleanField(choices=[[True, '是'], [False, '否']],
                                       widget=widgets.RadioSelectHorizontal,
                                       label='你是党员吗？')

    school = models.StringField(label='你就读的学院为：')

    grade = models.StringField(label='你就读的年级为：',
                               choices=['大一',
                                        '大二',
                                        '大三',
                                        '大四',
                                        '研一',
                                        '研二'],
                               widget=widgets.RadioSelectHorizontal)

    height = models.FloatField(label='你的身高', min=0, max=200)

    weight = models.FloatField(label='你的体重', min=0, max=200)

    monthly_expense = models.IntegerField(label='你每个月的生活费平均有：', min=0)

    big_brothers = models.IntegerField(min=0, max=99)
    big_sisters = models.IntegerField(min=0, max=99)
    little_brothers = models.IntegerField(min=0, max=99)
    little_sisters = models.IntegerField(min=0, max=99)

    mother_edu = models.IntegerField(
        label='你母亲的最高学历是：',
        choices=C.EDU_LEVELS,
        widget=widgets.RadioSelectHorizontal
    )

    father_edu = models.IntegerField(
        label='你父亲的最高学历是：',
        choices=C.EDU_LEVELS,
        widget=widgets.RadioSelectHorizontal
    )

    fam_income = models.IntegerField(
        label='你的家庭年总收入大概是什么范围？',
        choices=C.FAM_INCOME_LEVELS,
        widget=widgets.RadioSelectHorizontal
    )

    hukou = models.IntegerField(
        label='你的户籍类型是？',
        choices=[
            [1, '农业户籍'],
            [2, '城镇户籍（非农户籍）'],
        ],
        widget=widgets.RadioSelectHorizontal
    )

    birth_prov = models.StringField(
        label='你出生的省份（自治区、直辖市）'
    )


# PAGES
class Survey(Page):
    form_model = Player
    form_fields = [
        'gender',
        'birth_year',
        'birth_month',
        'ethnicity',
        'party_member',
        'school',
        'grade',
        'height',
        "weight",
        'monthly_expense',
        'big_brothers',
        'big_sisters',
        'little_brothers',
        'little_sisters',
        'mother_edu',
        'father_edu',
        'fam_income',
        'hukou',
        'birth_prov'

    ]


page_sequence = [Survey]
