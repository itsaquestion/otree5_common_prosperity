import json
import string

from otree.api import BasePlayer
from otree.api import BaseSubsession


def get_pc_id(player: BasePlayer):
    """
    从player的电脑的标签中获得座位号
    PC_01 -> 1
    PC_15 -> 5
    """
    pc_label = player.participant.label
    return label_to_id(pc_label)


def label_to_id(pc_label: str):
    return int(pc_label.split('_')[-1])


def set_endowment(subsession: BaseSubsession):
    """
       分配endowment和分组用的tag

       player.id是按连入服务器顺序，和座位号不完全对应。对于多round，第二个round的player.id，会接上一个round，
       因此必然不从1开始。

       应使用player.id_in_subsession，每个round都从1开始，可正常分组。
    """

    EDM = [90, 180, 540]

    p: BasePlayer

    for p in subsession.get_players():
        """
        对于endowment：
        1-8 -> low
        9-16 -> mid
        17-24 -> high

        对于tag
        A: 1-2
        B: 3-4
        C: 5-6
        D: 7-8
        ... ...

        """

        p.participant.wealth = EDM[(p.id_in_subsession - 1) // 8]

        p.participant.tag = string.ascii_uppercase[(p.id_in_subsession - 1) // 2]


"""
读写json文件到dict，用于在apps间传递数据，避免一些潜在的bug
"""


def save_to_json(data, path):
    with open(path, 'w') as fp:
        json.dump(data, fp)


def read_json(path) -> dict:
    with open(path, 'r') as fp:
        data = json.load(fp)
    return data
