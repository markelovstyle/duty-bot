import re
from typing import Union

from pymorphy2 import MorphAnalyzer

from .display import *

m = MorphAnalyzer()


def get_case(
    num: Union[float, int],
    word: str,
    case: str = "nomn",
    include: bool = True
) -> str:
    inflected = m.parse(word)[0].inflect({case})[0]
    p = m.parse(inflected)[0]
    agree = p.make_agree_with_number(int(num)).word
    if include:
        return "{} {}".format(num, agree)

    return agree


def display_time(seconds: int, case: str = "nomn", cut: bool = False) -> str:
    result = []
    for name, count in list(display_intervals.items()):
        value = int(seconds // count)
        if not value:
            continue
        seconds -= value * count
        if value == 1 and cut:
            result.append(name)
        else:
            result.append(get_case(value, name, case))
    return ' '.join(result[:3])


def parse_interval(text: str) -> int:
    """ Парсинг ключевых слов (день, час, мин, сек ...)
    в секунды.
    :param text: -> string
    :return: unix (total seconds)
    """
    unix = 0
    tags = re.findall(r'(\d+)[. ](день|дн|час|мин|сек|мес|г)', text)
    for k, v in tags:
        if not k:
            continue
        unix += int(k) * display_intervals[v]
    return unix