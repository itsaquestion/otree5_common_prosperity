from os import environ

SESSION_CONFIGS = [
    dict(
        name='common_prosperity',
        app_sequence=['agreement'],
        num_demo_participants=2,
        show_tips=True
    ),
]

ROOMS = [
    {
        'name': 'pc_99',
        'display_name': 'Room 418',
        'participant_label_file': '_rooms/pc_99.txt'}
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.1, participation_fee=10.00, doc=""
)

PARTICIPANT_FIELDS = [
    'endowment'
    'tag'
]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'zh-hans'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'CNY'
USE_POINTS = True
POINTS_CUSTOM_NAME = ' '

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6559744369738'

BROWSER_COMMAND = r"C:\Program Files\Mozilla Firefox\firefox.exe"
