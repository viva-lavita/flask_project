from collections import Counter
from typing import List


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


# print(fake_bin('8123456789'))


# def likes(names):
#     len_names = len(names)
#     if len_names < 2:
#         return '{} likes this'.format(['no one', *names][len_names])
#     if len_names == 2:
#         return '{} and {} like this'.format(*names)
#     if len_names == 3:
#         return '{}, {} and {} like this'.format(*names)
#     return '{}, {} and {} others like this'.format(*names[0: 2], len_names - 2)


def likes(names):
    match names:
        case []: return 'no one likes this'
        case [a]: return f'{a} likes this'
        case [a, b]: return f'{a} and {b} like this'
        case [a, b, c]: return f'{a}, {b} and {c} like this'
        case [a, b, *rest]: return f'{a}, {b} and {len(rest)} others like this'


def unique_in_order(sequence):
    return [el for idx, el in enumerate(sequence)
            if idx == 0 or el != sequence[idx - 1]]


print(unique_in_order("AAAABBBCCDAABBB"))


def find_it(seq):
    return [k for k, v in Counter(seq).items() if v % 2][0]

# print(find_it([1, 1, 2, -2, 5, 2, 4, 4, -1, -2, 5]))


# def high(x):
#     d = {word: sum([(ord(char) - 96) for char in word]) for word in x.split()}
#     return max(d, key=d.get)

def high(x):
    return max(x.split(), key=lambda k: sum(ord(c) - 96 for c in k))


# print(high('what time are we climbing up the volcano'))

def to_jaden_case(string):
    return ' '.join(map(str.capitalize, string.split()))

from collections import Counter

def duplicate_count(text):
    return sum(text.count(c) > 1 for c in set(text.lower()))


# print(duplicate_count("abcdeaa"))

# from functools import reduce
# def row_sum_odd_numbers(n):
#     start = 1
#     step = 0
#     for i in range(1, n):
#         step += 2
#         start = start + step
#     return reduce(lambda x, y: x + y, range(start, start+(n*2), 2))

def row_sum_odd_numbers(n):
    """ А всего то n ** 3"""
    start = 1
    step = 0
    for i in range(1, n):
        step += 2
        start += step
    return sum(range(start, start + (n * 2), 2))


# print(row_sum_odd_numbers(5))

def alphabet_position(text):
    # return ''.join(ord(char) - 96 for char in text.split())
    return ' '.join(str(ord(char) - 96) for char in text.lower() if char.isalpha())
    # return [char for char in text.lower() if char.isalpha()]

print(alphabet_position("The sunset sets at twelve o' clock."))
