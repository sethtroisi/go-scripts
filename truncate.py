#!/usr/bin/env python3

import sys
import os

# Takes a path and a moves number
path, moves = sys.argv[1:]
assert path.endswith('.sgf'), path
assert os.path.exists(path), path
moves = int(moves)

def delta_parens(d):
    return d.count('(') - d.count(')')

def move_count(d):
    return d.count(';B[') + d.count(';W[')

new_path = path[:-4] + '-' + str(moves) + '.sgf'
with open(path, 'r') as data, open(new_path, 'w') as result:
    count_moves = 0
    count_parens = 0
    for line in data.readlines():
        if count_moves + move_count(line) > moves:
            # keep chopping ;... off back
            while count_moves + move_count(line) > moves:
                line = line.rsplit(';', 1)[0]

            assert line.endswith(']')

        result.write(line)
        count_moves += move_count(line)
        assert count_moves <= moves
        count_parens += delta_parens(line)
        assert count_parens >= 0

        if count_moves == moves:
            result.write(')' * count_parens)
            result.write('\n')
            break
