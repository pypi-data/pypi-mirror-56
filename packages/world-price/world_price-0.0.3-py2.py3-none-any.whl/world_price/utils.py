import statistics
from enum import Enum
from itertools import combinations


class SymbolFormatEnum(Enum):
    UPPER_UNDERSCORE = 1
    LOWER_UNDERSCORE = 2
    LOWER = 3
    UPPER_HYPHEN = 4


def symbol_format_conv(s, from_format: SymbolFormatEnum, to_format: SymbolFormatEnum):
    if (from_format is SymbolFormatEnum.UPPER_UNDERSCORE and
            to_format is SymbolFormatEnum.LOWER):
        return ''.join(s.split('_')).lower()
    elif from_format is SymbolFormatEnum.UPPER_UNDERSCORE and to_format is SymbolFormatEnum.UPPER_HYPHEN:
        return '-'.join(s.split('_'))
    elif (from_format is SymbolFormatEnum.LOWER and
          to_format in [SymbolFormatEnum.LOWER_UNDERSCORE, SymbolFormatEnum.UPPER_UNDERSCORE]):
        # it's unknown how many chars are there for quote currency
        # try all 3 possibilities
        base = None
        for cur_base in ['btc', 'eth', 'usdt']:
            if s.endswith(cur_base):
                base = cur_base
                break
        if base is not None:
            result = s[:len(s) - len(base)] + '_' + base
            return result if to_format is SymbolFormatEnum.LOWER_UNDERSCORE else result.upper()
        else:
            return s


class InvalidWorldPrice(Exception):
    pass


def validate_world_price(world_prices, tolerance):
    size = len(world_prices)
    # size is always gte 1
    if size == 1:  # only one price record, mark it as valid
        return world_prices[0]
    elif size == 2:  # two price record, the difference of them should no-more-than e.g. 5%
        diff = (world_prices[0] - world_prices[1]) / world_prices[1]
        if abs(diff) >= tolerance:
            raise InvalidWorldPrice
        else:
            return statistics.mean(world_prices)
    elif size == 3:  # try all possible combinations, choose the smallest diff situation
        sorting_list = []  # use list, for sorting
        for idx, situation in enumerate(combinations(world_prices, 2)):
            diff = (situation[0] - situation[1]) / situation[1]
            diff = abs(diff)
            sorting_list.append([situation, diff])
        sorting_list.sort(key=lambda item: item[1])
        # choose the smallest diff
        if sorting_list[0][1] >= tolerance:
            raise InvalidWorldPrice
        return statistics.mean(sorting_list[0][0])
    else:  # more than 3, common situation, which is complicated, skip for now
        raise ValueError("more than 3 price source, not implemented yet...")
