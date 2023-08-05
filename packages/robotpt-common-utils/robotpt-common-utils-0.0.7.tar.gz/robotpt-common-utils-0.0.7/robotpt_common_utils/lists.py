def is_iterable(obj, is_strings_iterable=False):
    if type(obj) is str and not is_strings_iterable:
        return False
    try:
        _ = (e for e in obj)
    except TypeError:
        return False
    else:
        return True


def make_sure_is_iterable(obj):
    if is_iterable(obj):
        return obj
    else:
        return [obj]


def append_to_list(list_, objs, check_fns=[]):
    objs = make_sure_is_iterable(objs)
    check_fns = make_sure_is_iterable(check_fns)

    for obj in objs:
        for check in check_fns:
            if check(obj) == False:
                raise ValueError("Invalid object to add")
        list_.append(obj)

    return list_


def is_all_list_elements_pass_tests(obj, *tests):
    obj = make_sure_is_iterable(obj)
    for o in obj:
        if is_object_pass_tests(o, *tests) is False:
            return False

    return True


def is_object_pass_tests(obj, *tests):
    tests = make_sure_is_iterable(tests)

    for t in tests:
        if callable(t) is False:
            raise ValueError(f"'{t}' is not callable")

    for t in tests:
        if t(obj) is False:
            return False

    return True


def append_type_to_list(list_, objs, type_):
    return append_to_list(
        list_,
        objs,
        lambda obj: type(obj) is type_
    )


def remove_repeats(list_, is_remove_from_front=True):

    if is_remove_from_front:
        out = _remove_repeats(list_)
    else:
        list_.reverse()
        out = _remove_repeats(list_)
        out.reverse()
    return out


def _remove_repeats(list_):
    list_ = make_sure_is_iterable(list_)
    seen = set()
    return [x for x in list_ if not (x in seen or seen.add(x))]

