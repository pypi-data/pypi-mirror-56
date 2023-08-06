from typing import Dict, Union


def merge(a: dict, b: dict) -> dict:
    """Deep merge of 2 dict objects.

    Take the values in dict "b" and merge them
    into dict "a". If a key exists in both inputs
    the value from "b" will be used.
    """
    queue = list()
    ret = dict()
    queue.append((ret, a, b))
    while len(queue) > 0:
        root, left, right = queue.pop()
        for rk, rv in right.items():
            if rk not in left:
                root[rk] = rv
            elif isinstance(rv, list) and isinstance(left[rk], list):
                root[rk] = left[rk] + rv
            elif isinstance(rv, dict) and isinstance(left[rk], dict):
                root[rk] = {}
                queue.append((root[rk], left[rk], rv))
            else:
                root[rk] = rv
        for lk, lv in left.items():
            if lk not in right:
                root[lk] = lv
    return ret


def explode(items: Dict[str, Union[str, int, bool, list]], delimiter: str = ':') -> dict:
    """Explode a flat map into a nested map.

    Explode a flat map such as { "a:b:c", "val" } into
    a nested map such as { "a": { "b": { "c": "val" } } }
    """
    val = dict()
    for k, v in items.items():
        r = val
        parts = k.split(delimiter)
        for i in range(len(parts)):
            k_part = parts[i]
            if i == len(parts) - 1:
                if v is not None:
                    r[k_part] = v
            elif k_part not in r:
                r[k_part] = {}
                r = r[k_part]
            elif isinstance(r[k_part], dict):
                r = r[k_part]
    return val
