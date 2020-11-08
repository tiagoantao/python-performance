import numpy as np

import requests

PATTERN_FORMAT = 'http://www.conwaylife.com/patterns/{pattern}.cells'


def get_pattern_text(pattern_name):
    return requests.get(PATTERN_FORMAT.format(pattern=pattern_name)).text


def convert_pattern_to_array(pattern_text):
    max_width = 0
    my_pattern_list = []
    for line in pattern_text.split('\n')[:-1]:
        line = line.rstrip()
        if len(line) != 0 and line[0] == '!':
            continue
        my_line = []
        for char in line:
            my_line.append(1 if char == 'O' else 0)
        my_pattern_list.append(my_line)
        max_width = max(max_width, len(my_line))
    for line_number, line_pattern in enumerate(my_pattern_list):
        line_pattern.extend([0] * (max_width - len(line_pattern)))
    return np.array(my_pattern_list)


def recolor(matrix, new_color):
    return matrix[matrix == 1] == new_color


#my_pattern_text = get_pattern_text('pulsar')

#my_pattern = convert_pattern_to_array(my_pattern_text)

