import math
import statistics
import random

def get_variance(combs=(48,52,720,1096,3744,16440), payouts=(40,30,6,3,1,-1), m=1):
    if combs[0] >= 1: #combs is list of combo totals
        combs=[int(round(i/m)) for i in combs]
    else: # combs is list of probabilites, m should be >= 1/min(combs)
        combs = [int(round(i*m)) for i in combs]
    y = []
    print(combs)
    print(payouts)
    
    for i,j in zip(combs, payouts):
        y += [j]*i
    print(len(y))
    return statistics.variance(y)


def get_ev(combs=(48,52,720,1096,3744,16440), payouts=(-40,-30,-6,-3,-1,1)):
    y = 0
    for i,j in zip(combs, payouts):
        y += i*j
    if combs[0] < 1:
        return y
    else:
        return y / sum(combs)

def kelley(b, w, p):
    """
    b = ratio of bet amount to bankroll
    w = list of win amounts on a "to one" basis
    p = list of probabilies of outcomes
    returns expected bankroll growth after one bet 
    """

    n = min(len(w), len(p))
    
    x = 1
    if p[0] > 1:
        s = sum(p)
        p = [i/s for i in p]
    for i in range(n):
        y = math.pow(1+b*w[i], p[i])
        x *= y
    return x - 1

def get_kelley_bet(combs=(48,52,720,1096,3744,16440), payouts=(-40,-30,-6,-3,-1,1), m=100000):
    """
    given a list of payouts on a "to one" basis, and corresponding list either combination totals or probabilites
    returns the optimal fraction within precision of 1/m of a bankroll to bet according to kelley, and expected bankroll growth after 1 bet
    in other words, given values for w and p returns the value for b which maximizes kelley(b, w, p), and expected bankroll growth after one bet
    
    """
    
    s = sum(combs)
##    n = len(payouts)
    w = payouts
    if combs[0] >= 1:
        p = [i/s for i in combs]
    else:
        p = combs
    r = 0
    bet = 0
    for i in range(2, m+1):
        b = 1 / i
        try:
            x = kelley(b, w, p)
            if x > r:
                r = x
                bet = b, i
        except ValueError:
            continue
    return bet, r

#buster
buster_payouts = (-2,-2,-4,-16,-50,-200,1)
buster_probs = 0.1730318431697958, 0.08939180973343368, 0.020472550873558974, 0.0026376021859951643, 0.000214444168179472, 1.1945253825662186e-05, 0.7142398046152112

buster_combs = [17303, 8939, 2047, 264, 21, 1, 71424]

#perfect pair (digit is deck num):
pp_probs_2 = 0.038834951456310676, 0.019417475728155338, 0.009708737864077669, 0.9320388349514563
pp_probs_5 = 0.03861003861003861, 0.019305019305019305, 0.015444015444015444, 0.9266409266409267
pp_combs_8 = [3328, 1664, 1456, 79872]
pp_payouts = (-6, -12, -25, 1)

# 3 card poker bonus bet:
six_card_combs = 188, 1656, 14664, 165984, 205792, 361620, 732160, 18876456
six_card_payouts = -1000, -200, -100, -20, -15, -10, -7, 1 # -1000, -500

pairplus_combs=(48,52,720,1096,3744,16440)
pairplus_payouts=(-40,-30,-6,-3,-1,1)

uth = 4324, 37260, 224848, 3473184, 4047644, 6180020, 6461620, 113355660
uth_p = -50, -40, -30, -8, -7, -4, -3, 1

def sim_growth(trials=1000, trial_len=10000, combs=(48,52,720,1096,3744,16440), payouts=(-40,-30,-6,-3,-1,1), bet_frac=1/147):
    br = 1
    y = [0]
    for i in combs:
        y.append(y[-1]+i)
    s = sum(combs) - 1
    br_total = 0
    t = 0

    for trial in range(trials):
        br = 1
        for i in range(trial_len):
            n = random.randint(0, s)
            bet = br * bet_frac
            for j in range(len(y)):
                if n < y[j]:
                    r = payouts[j-1]
                    br += r * bet
                    break
            if br == 2:
                t += i
                break
            if br <= 0:
                print(br)
                break
        br_total += br
    return t / trials, br_total / trials


def kelley_multiply(trials=1000, combs=(48,52,720,1096,3744,16440), payouts=(-40,-30,-6,-3,-1,1), bet_frac=1/147, m=2):
    # returns average number of trials to multiply roll by m
    br = 1
    y = [0]
    for i in combs:
        y.append(y[-1]+i)
    s = sum(combs) - 1
    br_total = 0
    t = 0

    for trial in range(trials):
        br = 1
        i = 0
        while 1:
            i += 1
            n = random.randint(0, s)
            bet = br * bet_frac
            for j in range(len(y)):
                if n < y[j]:
                    r = payouts[j-1]
                    br += r * bet
##                    print(br)
                    break
            if br >= m:
                print(i)
                t += i
                break
            if br <= 0:
                print(br)
                break
        br_total += br
    return t / trials

