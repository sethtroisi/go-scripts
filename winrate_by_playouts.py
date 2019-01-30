from collections import defaultdict
import math

DATA = "data/wins_fast_slow.csv"

with open(DATA) as f:
    data = [list(map(int, line.split(","))) for line in f.readlines()]

print("Rows:", len(data))

print("Models:", len(set(r[0] for r in data)))

# Row is [black, white, is_slow, games, black_wins]
games = defaultdict(int)
wins = defaultdict(int)

for r in data:
    if r[0] > r[1]:
        r[0], r[1] = r[1], r[0]
        r[4] = r[3] - r[4]

    games[tuple(r[:3])] += r[3]
    wins[tuple(r[:3])] += r[4]

print ("Pairings:", len(data), len(games))

def elo(key):
    winrate = wins[key] / games[key]
    winrate = min(0.99, max(0.01, winrate))
    return -400 * math.log10(1 / winrate - 1)


diff = []
for key in sorted(games.keys()):
    a, b = key[:2]

    if key[2] == True:
        continue

    slow_key = key[:2] + (False,)
    fast_key = key[:2] + (True,)

    slow_elo = elo(slow_key)
    fast_elo = elo(fast_key)
    diff.append(slow_elo - fast_elo)

    print ("{},{}: {:.4g} {:.4g} {:.4g}".format(a, b, slow_elo, fast_elo, slow_elo - fast_elo))

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

_ = plt.hist(x=diff, bins=50)

plt.yscale('log')

plt.grid(axis='y')
plt.xlabel('Elo diff 800 vs 200 playouts')
plt.ylabel('Frequency')
plt.title('Elo difference at various playouts')

plt.savefig('elo_diff_histogram.png')

