import re


def clear_list(l: list):
    l = [x.strip() for x in l if x != "\t"]
    l = [x for x in l if x != " "]
    l = [x for x in l if x != "\n"]
    return list(filter(None, l))

def clear_join(l: list) -> str:
    l = clear_list(l)
    l_str = " ".join(l)
    return re.sub(' +', ' ', l_str)