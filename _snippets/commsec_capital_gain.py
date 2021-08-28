import os
from collections import defaultdict
from tika import parser
from datetime import datetime, timedelta

def invert_date(dt):  # '01/02/2020' -> '2020-02-01'
    d,m,y = dt.split('/')
    return f'{y}-{m}-{d}'

def cgt_discount(bdt, sdt, price_diff):
    # TODO
    #if price_diff < 0:  # no need to discount loss  ???
    #    return 1
    bdt = datetime.strptime(bdt, '%Y-%m-%d')
    sdt = datetime.strptime(sdt, '%Y-%m-%d')
    return 1 if (sdt - bdt) < timedelta(days=366) else 0.5

def date_to_financial_year(dt):  # '01/08/2020' -> '2021'
    y, m, d = dt.split('-')
    m = int(m)
    if m < 7:
        return y
    else:
        return str(int(y) + 1)

def get_units_price(line):
    units, price = line.split(' ')
    units = int(units.replace(',', ''))
    price = float(price)
    return units, price

def extract(fname):  # extract transaction from contract file
    raw = parser.from_file(fname)
    lines = raw['content'].split('\n')
    # name
    idx = lines.index('55539463 0468818969')
    share = lines[idx + 2]
    # units, price
    idx = lines.index('UNITS AT PRICE')
    if len(lines[idx + 2].split(' ')) == 2:
        up = []
        while 'PAYMENT METHOD' not in lines[idx + 2]:
            up.append(get_units_price(lines[idx + 2]))
            idx += 2
    else:
        up = []
        while 'AVERAGE PRICE' not in lines[idx - 2]:
            up.append(get_units_price(lines[idx - 2]))
            idx -= 2
    # date
    if 'TOTAL COST:' in lines:
        idx = lines.index('TOTAL COST:')
    else:
        idx = lines.index('SETTLEMENT DATE:')
    date = lines[idx + 2]
    date = invert_date(date)
    # sold or bought
    sold = 'WE HAVE SOLD THE FOLLOWING SECURITIES FOR YOU' in lines
    bought = 'WE HAVE BOUGHT THE FOLLOWING SECURITIES FOR YOU' in lines
    assert(sold ^ bought)
    if sold:
      tp = 'S'
    if bought:
      tp = 'B'
    return [(date, share, tp, up1[0], up1[1]) for up1 in up]

data = defaultdict(list)
for root, subdirs, files in os.walk('./'):  # process all contract files
    for fname in files:
        if fname.startswith('Contract '):
            if not root.endswith('/'):
                root += '/'
            res = extract(root + fname)
            for date, share, tp, unit, price in res:
                if root != './':  # we assume contracts are placed in directory with asset name (or just lay in the root)
                    print(root[2:], share)
                    assert (root[2:-1] == share)
                data[share]+=[(date, tp, unit, price)]

for sh in data:
    data[sh].sort(key=lambda v:v[0])

capital_gain = defaultdict(lambda: defaultdict(lambda: 0))
current_shares = {}

# share = 'AGG'
def process(share):  # calculate capital gain for share
    bought = list(filter(lambda r: r[1] == 'B', data[share]))
    sold = list(filter(lambda r: r[1] == 'S', data[share]))
    while sold:
        # https://www.ato.gov.au/Forms/Guide-to-capital-gains-tax-2021/?page=30
        # Alternatively, you may wish to use a ‘first in, first out’ basis where you treat the first shares
        # or units you bought as being the first you disposed of.
        bdt, _, b, bp = bought[0]
        date, _, s, sp = sold[0]
        price_diff = sp - bp
        financial_year = date_to_financial_year(date)
        discount = cgt_discount(bdt, date, price_diff)
        if s == b:
            print(s*price_diff, financial_year, discount, bought[0], sold[0])
            capital_gain[financial_year][share] += s*price_diff*discount
            bought = bought[1:]
            sold = sold[1:]
        elif s > b:
            print(b*price_diff, financial_year, discount, bought[0], sold[0])
            capital_gain[financial_year][share] += b*price_diff*discount
            bought = bought[1:]
            date, tp, unit, price = sold[0]
            sold[0] = (date, tp, s-b, price)
        elif b > s:
            print(s*price_diff, financial_year, discount, bought[0], sold[0])
            capital_gain[financial_year][share] += s*price_diff*discount
            sold = sold[1:]
            date, tp, unit, price = bought[0]
            bought[0] = (date, tp, b - s, price)
        else:
            assert False
    current_shares[share] = sum([b[2] for b in bought]), sum([b[2]*b[3] for b in bought])
    print(share, 'empty' if not bought else sum([b[2] for b in bought]))

for share in data:
    print(share)
    process(share)

# drop 0s from "current_shares"
for sh in list(current_shares.keys()):
    if not current_shares[sh][0]:
        del current_shares[sh]

# print results

print('\nCapital gain per year&share:')
for y in sorted(capital_gain.keys()):
    for sh in capital_gain[y]:
        print(y, sh, capital_gain[y][sh])
    print('\n')

print('\nCapital gain per year:')
for y in sorted(capital_gain.keys()):
    print(y, sum(capital_gain[y].values()))

print('\n\ncurrent shares')
for sh in current_shares:
    print(sh, current_shares[sh][0])
print('\n\ninitial cost', sum([current_shares[sh][1] for sh in current_shares.keys()]))