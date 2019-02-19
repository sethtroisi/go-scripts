#!/usr/bin/env python3

import random
import math

def LL(x):
    return 1/(1+10**(-x/400))

def LLF(wins,losses, p0, p1):
    # from sethtrois@ https://github.com/gcp/leela-zero/issues/378#issuecomment-351639093
    winLog = math.log(p1 / p0)
    lossLog = math.log((1-p1) / (1-p0))

    alpha = beta = 0.05
    lower = math.log(beta / (1 - alpha))
    upper = math.log((1 - beta) / alpha)

    llf = wins * winLog + losses * lossLog
    #print (round(lower,3), round(upper,3), "\t", round(llf, 3))
    #print ("LLF:", round(llf, 5))
    return llf

def wiki(w, l, p0, p1):
    # from https://en.wikipedia.org/wiki/Likelihood-ratio_test
    # and  https://nowak.ece.wisc.edu/ece830/ece830_fall11_lecture9.pdf
    H1 = p1 ** w * (1-p1) ** l
    H0 = p0 ** w * (1-p0) ** l
    t1 = math.log(H1 / H0)

    H_combined = (p1 / p0) ** w * ((1-p1)/(1-p0)) ** l
    t = math.log(H_combined)
    return t

def LLR(W,L,p0,p1):
    # from https://github.com/gcp/leela-zero-server/blob/master/classes/utilities.js#L178
    N = W + L
    w = W / N
    l = L / N
    #s = w
    #m2 = w
    #variance = m2 - s ** 2
    #variance_s = variance / N
    #res = (p1 - p0) * (2.0 * s - p0 - p1) / variance_s / 2.0

    variance_s = (w * (1 - w)) / N
    res = (p1 - p0) * (2 * w - p0 - p1) / variance_s / 2
    #print ("LLR (var method):", round(res ,3))
    return res

def compareSPRT():
    alpha = beta = 0.05
    elo0 = 0
    elo1 = 35
    LA=math.log(beta/(1-alpha))
    LB=math.log((1-beta)/alpha)
    print ("LA, LB: {:.3f} {:.3f}".format(LA, LB))

    p0=LL(elo0)
    p1=LL(elo1)
    print ("P0, P1: {:.3f} {:.3f}".format(p0, p1))
    print ()

    N = 400
    for W in range(1, N):
        for L in range(1, N-W+1):
            # LZ
            LLR_  = LLR(W, L, p0, p1)

            # Seth's two attempts
            LLF_  = LLF(W,L, p0,p1)
            wiki_ = wiki(W,L, p0,p1)

            def result(a):
                return -1 if a < LB else (1 if a > LA else 0)

            lz_res = result(LLR_)
            test_res = result(LLF_)
            if lz_res != test_res:
                print ("W/L: {}-{}: {:.3f} vs {:.3f}".format(
                    W, L, LLR_, LLF_))


compareSPRT()


'''
def randomRatio(p):
    assert 0 <= p <= 1
    while True:
        yield random.random() < p

class Sprt:
    def __init__(self, elo0, elo1, test):
        self.test = test

        alpha = 0.05
        beta = 0.05
        self.lower = math.log(beta / (1 - alpha))
        self.upper = math.log((1 - beta) / alpha)

        self.p0=LL(elo0)
        self.p1=LL(elo1)

        self.wins = 1e-5
        self.losses = 1e-5

    def addResult(self, win):
        if win:
            self.wins += 1
        else:
            self.losses += 1

    def status(self):
        llr = self.test(self.wins, self.losses, self.p0, self.p1)
        if llr < self.lower:
            return -1
        if llr > self.upper:
            return 1
        return 0

def brute_test(n, elo0, elo1, test):
    good = 0
    bad = 0
    unfinished = 0
    gamesNeeded = 0

    for iteration in range(n):
#        true_elo = random.randint(-120, 120)
        true_elo = 5
        true_prob_win = LL(true_elo)
        correct_action = -1 if abs(elo0 - true_elo) < abs(elo1 - true_elo) else 1

        trial = Sprt(elo0, elo1, test)

        for i, r in enumerate(randomRatio(true_prob_win), 1):
            if i > 50000:
                unfinished += 1
                break

            trial.addResult(r)
            action = trial.status()
            if i < 20 or action == 0:
                continue

            gamesNeeded += i
            if action == correct_action:
                good += 1
            else:
                bad += 1
            break

    print ("accepted {} = {:.1f}%,  rejected {} = {:.1f}%".format(
        good, 100 * good / n, bad, 100 * bad / n))
    print ("\tunfinished {} = {:.1f}%".format(
        unfinished, 100 * unfinished / n))
    print ("\tevaled {} games, {:.1f} per trial".format(
        gamesNeeded, gamesNeeded / n))
    print ()


######

w = 920
l = 820
elo0 = 0
elo1 = 35

#SPRT(w, l, elo0, elo1)

brute_test(100, -1, 3, LLR)
brute_test(100, -1, 3, LLF)
'''
