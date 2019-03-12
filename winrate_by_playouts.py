#!/usr/bin/env python3

from collections import defaultdict, Counter
import math
from scipy import stats

DATA = "data/elo_by_speed.csv"

with open(DATA) as f:
    data = [[int(i) if len(i) < 4 else i for i in line.split(",")] for line in f.readlines()]

print("Games:", sum(r[3] for r in data))
print("\tRapid:", sum(r[3] for r in data if r[2] == "rapid"))
print("\tFast:", sum(r[3] for r in data if r[2] == "fast"))
print("\tSlow:", sum(r[3] for r in data if r[2] == "slow"))
print()
print("Rows:", len(data))
print("Models:", len(set(r[0] for r in data)))

# Row is [black, white, speed, games, black_wins]
games = defaultdict(int)
wins = defaultdict(int)

for r in data:
    if r[0] > r[1]:
        r[0], r[1] = r[1], r[0]
        r[4] = r[3] - r[4]

    games[tuple(r[:3])] += r[3]
    wins[tuple(r[:3])] += r[4]

for speed in ["rapid", "fast", "slow"]:
    print (speed, "pairings:", len(set(tuple(r[:2]) for r in data if r[2] == speed)))
print()

diff_counter = Counter()
for r in data:
    diff_counter[(r[2], abs(int(r[0]) - int(r[1])))] += r[3]
for (speed, diff), count in sorted(diff_counter.items()):
    print (speed, diff, "pairings:", count)

def elo(key):
    if not (key in wins and key in games):
        return None

    winrate = wins[key] / games[key]
    winrate = min(0.99, max(0.01, winrate))
    return -400 * math.log10(1 / winrate - 1)

def plot_and_save(diffs, name, a, b):
    import matplotlib
    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    plt.clf()

    _ = plt.hist(x=diffs, bins=50)

    plt.yscale("log")

    plt.xlabel("Elo diff {} vs {} playouts".format(a, b))
    plt.ylabel("Frequency")
    plt.title("Elo difference at various playouts")

    png = "pictures/elo_diff_histogram_{}.png".format(name)
    plt.savefig(png)
    print("eog", png)
    s = stats.describe(diffs)
    print("\tn={}, min={:.1f}, max={:.1f}, mean={:.1f}, stddev={:.1f}".format(
        s.nobs, s.minmax[0], s.minmax[1], s.mean, s.variance ** 0.5))


diff = []
diff2 = []
diff3 = []
for key in sorted(games.keys()):
    a, b = key[:2]

    if key[2] != "slow":
        continue

    rapid_key = key[:2] + ("rapid",)
    fast_key = key[:2] + ("fast",)
    slow_key = key[:2] + ("slow",)

    rapid_elo = elo(rapid_key)
    fast_elo = elo(fast_key)
    slow_elo = elo(slow_key)
    if slow_elo and fast_elo:
        diff.append(slow_elo - fast_elo)
    if slow_elo and rapid_elo:
        diff2.append(slow_elo - rapid_elo)
    if fast_elo and rapid_elo:
        diff3.append(fast_elo - rapid_elo)

#    print ("{},{}: {:.4g} {:.4g} {:.4g}".format(a, b, slow_elo, fast_elo, slow_elo - fast_elo))

print()
plot_and_save(diff, "slow_fast", 800, 200)
plot_and_save(diff2, "slow_rapid", 800, 50)
plot_and_save(diff3, "fast_rapid", 200, 50)
