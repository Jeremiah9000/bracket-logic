import copy

brackets = {'rounded': ('(', ')'),
            'pointed': ('<', '>'),
            'squared': ('[', ']'),
            'curly': ('{', '}')}

math_expression = ['([<x+y>+3]-1)', '([<x+y>+3)-1]', '[<>()]', '[<(>)]', '[(a*b+<7-c>+9]', '[{(h*i+3)-12]/4*x+2}',
                   '[ab(c/d<e-f+(7*6)>)+2]']


def bracket_logic(expression):
    valid = True
    patterns = {'round': [], 'point': [], 'square': [], 'curly': []}
    round_indexes_open = [i for i, ltr in enumerate(expression) if ltr == '(']
    round_indexes_close = [i for i, ltr in enumerate(expression) if ltr == ')']
    round_indexes_all = round_indexes_open + round_indexes_close
    round_indexes_all.sort()
    for index in round_indexes_all:
        if index in round_indexes_open:
            patterns['round'].append(1)
        if index in round_indexes_close:
            patterns['round'].append(-1)
    point_indexes_open = [i for i, ltr in enumerate(expression) if ltr == '<']
    point_indexes_close = [i for i, ltr in enumerate(expression) if ltr == '>']
    point_indexes_all = point_indexes_open + point_indexes_close
    point_indexes_all.sort()
    for index in point_indexes_all:
        if index in point_indexes_open:
            patterns['point'].append(1)
        if index in point_indexes_close:
            patterns['point'].append(-1)
    square_indexes_open = [i for i, ltr in enumerate(expression) if ltr == '[']
    square_indexes_close = [i for i, ltr in enumerate(expression) if ltr == ']']
    square_indexes_all = square_indexes_open + square_indexes_close
    square_indexes_all.sort()
    for index in square_indexes_all:
        if index in square_indexes_open:
            patterns['square'].append(1)
        if index in square_indexes_close:
            patterns['square'].append(-1)
    curly_indexes_open = [i for i, ltr in enumerate(expression) if ltr == '{']
    curly_indexes_close = [i for i, ltr in enumerate(expression) if ltr == '}']
    curly_indexes_all = curly_indexes_open + curly_indexes_close
    curly_indexes_all.sort()
    for index in curly_indexes_all:
        if index in curly_indexes_open:
            patterns['curly'].append(1)
        if index in curly_indexes_close:
            patterns['curly'].append(-1)
    opens = [round_indexes_open, point_indexes_open, square_indexes_open, curly_indexes_open]
    closes = [round_indexes_close, point_indexes_close, square_indexes_close, curly_indexes_close]
    for beg, end in zip(opens, closes):
        if len(beg) != len(end):
            return False
    for value in patterns.values():
        balance = 0
        for direction in value:
            balance += direction
            if balance < 0:
                return False
        if balance != 0:
            return False
    index_and_direction = copy.deepcopy(patterns)
    for key in index_and_direction.keys():
        index_and_direction[key].clear()
    for name, indexes, directions in zip([key for key in patterns.keys()],
                                         [round_indexes_all, point_indexes_all, square_indexes_all, curly_indexes_all],
                                         [patterns['round'], patterns['point'], patterns['square'], patterns['curly']]):
        for index, direction in zip(indexes, directions):
            index_and_direction[name].append((index, direction))
    index_direction_tracer = copy.deepcopy(index_and_direction)
    for value in index_direction_tracer.values():
        value.clear()
    for key, value in index_and_direction.items():
        balance = 0
        for pair in value:
            if pair[1] == 1:
                balance += pair[1]
                index_direction_tracer[key].append((pair[0], 'open', balance))
            if pair[1] == -1:
                index_direction_tracer[key].append((pair[0], 'close', balance))
                balance += pair[1]
    bracket_segments_index = copy.deepcopy(index_direction_tracer)
    for value in bracket_segments_index.values():
        value.clear()
    for key, value in index_direction_tracer.items():
        for triplet in value:
            if triplet[1] == 'open':
                for item in index_direction_tracer[key]:
                    if item[0] != triplet[0]:
                        if item[2] == triplet[2]:
                            bracket_segments_index[key].append((triplet[0], item[0]))
    bracket_segments = copy.deepcopy(bracket_segments_index)
    for value in bracket_segments.values():
        value.clear()
    for key, value in bracket_segments_index.items():
        for beg, end in value:
            bracket_segments[key].append(expression[beg + 1:end])
    all_segments = []
    for value in bracket_segments.values():
        for item in value:
            all_segments.append(item)
    for item in all_segments:
        if item.count('(') != item.count(')'):
            valid = False
        if item.count('<') != item.count('>'):
            valid = False
        if item.count('[') != item.count(']'):
            valid = False
        if item.count('{') != item.count('}'):
            valid = False
    return valid


for expr in math_expression:
    print(expr, "is valid expression?", bracket_logic(expr))
