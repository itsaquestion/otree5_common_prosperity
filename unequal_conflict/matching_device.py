import random


def unlist(x):
    return [i for sublist in x for i in sublist]


def is_unique(x):
    return len(set(x)) == len(x)


def get_matches():
    """
    生成随机匹配matrix

    匹配组合见matching.jpg.

    pairs是一个两层的List，外层是组别，内层是参与人ID
    以第二行为例  [[5, 6], [9, 10]],
    5，6禀赋相同，9，10禀赋相同

    匹配过程：shuffle([5,6]), shuffle([9,10])

    [5,6] -> shuffle()
    [9,10] -> shuffle()
    -> zip()

    可得
    [[第一组的某个，第二组的某个],[第一组的另一个，第二组的另一个]]

    -> append到result -> unlist

    """
    pairs = [
        [[1, 2], [3, 4]],
        [[5, 6], [9, 10]],
        [[7, 8], [17, 18]],
        [[11, 12], [13, 14]],
        [[15, 16], [19, 20]],
        [[21, 22], [23, 24]]
    ]

    result = []

    for i in range(len(pairs)):
        a_pair = pairs[i]
        [random.shuffle(pl) for pl in a_pair]
        """
        a_pair = [[1, 2], [3, 4]]
        """
        result.append(list(zip(a_pair[0], a_pair[1])))

    return unlist(result)


if __name__ == "__main__":
    print(get_matches())
    print(get_matches())


