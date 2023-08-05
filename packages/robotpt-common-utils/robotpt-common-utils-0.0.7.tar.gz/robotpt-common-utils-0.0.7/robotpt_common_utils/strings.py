import random
import string
from robotpt_common_utils import lists
import re


def random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, length))


def wildcard_search_in_list(pattern, list_, wildcard_symbol='*'):
    list_ = lists.make_sure_is_iterable(list_)
    idxs = []
    for idx in range(len(list_)):
        if is_wildcard_match(
                pattern, list_[idx],
                wildcard_symbol=wildcard_symbol
        ):
            idxs.append(idx)
    return [list_[i] for i in idxs]


def is_wildcard_match(pattern, str_, wildcard_symbol='*'):
    for special_char in ['^', '$', '.', '+', '?', '{', '}', '/', '\\',
                         '|', '[', ']', '(', ')', ':', '<', '>', '*']:
        if special_char in pattern and special_char is not wildcard_symbol:
            raise ValueError("May conflict with REGEX parsing and do weird things")
    regex_glob_star = ".*"
    pattern = str.replace(pattern, wildcard_symbol, regex_glob_star)
    pattern = '^' + pattern + '$'
    matches = re.search(pattern, str_)
    return matches is not None
