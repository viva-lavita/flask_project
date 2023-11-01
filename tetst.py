from typing import List, Tuple


def get_index(office: List[str]) -> dict[int: List[int]]:
    cor = {}
    for y in range(len(office)):
        temp = []
        for x in range(len(office[y])):
            if office[y][x] == '.':
                temp.append((x))
        cor[y] = temp
    return cor


def locate_entrance(office: List[str]) -> dict[int: List[int]]:
    cor = get_index(office)
    if cor[0] != []:
        return cor[0][0], 0
    elif cor[len(cor)-1] != []:
        return cor[len(cor)-1][0], len(cor)-1

    for y in range(1, len(cor) - 1):
        for el in cor[y]:
            if (
                el >= len(office[y-1]) or
                el >= len(office[y+1]) or
                el == 0 or
                el == len(office[y]) - 1 or
                office[y][el-1] == ' ' or
                office[y][el+1] == ' ' or
                office[y-1][el] == ' ' or
                office[y+1][el] == ' '
            ):
                return el, y


def fake_bin(s):
    return s.translate(str.maketrans('0123456789', '0000011111'))


print(fake_bin('8123456789'))


def likes(names):
    len_names = len(names)
    if len_names < 2:
        return '{} likes this'.format(['no one', *names][len_names])
    if len_names == 2:
        return '{} and {} like this'.format(*names)
    if len_names == 3:
        return '{}, {} and {} like this'.format(*names)
    return '{}, {} and {} others like this'.format(*names[0: 2], len_names - 2)


print(likes([]))


def likes(names):
    match names:
        case []: return 'no one likes this'
        case [a]: return f'{a} likes this'
        case [a, b]: return f'{a} and {b} like this'
        case [a, b, c]: return f'{a}, {b} and {c} like this'
        case [a, b, *rest]: return f'{a}, {b} and {len(rest)} others like this'
