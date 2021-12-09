#!/usr/bin/env python3

import csv
import sys
from decimal import Decimal

line = []
with open(sys.argv[1]) as f:
    r = csv.reader(f)
    next(r, None) # skip header

    for l in r:
        date = l[6]
        pair = l[0].replace('_', '-')
        side = 'Buy' if l[1] == 'bid' else 'Sell'
        amount = l[3]
        total = Decimal(l[2]) * Decimal(l[3])
        fee = l[4]
        feecur = pair.split('-')[0] if l[1] == 'bid' else pair.split('-')[1]
        line.append([date, pair, side, str(amount), total, fee, feecur, '', ''])

header = ['Koinly Date','Pair','Side','Amount','Total','Fee Amount','Fee Currency','Order ID','Trade ID']

with open('out.csv', 'w') as out:
    w = csv.writer(out)
    w.writerow(header)
    w.writerows(line)