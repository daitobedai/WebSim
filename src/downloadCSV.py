import requests
import os
from collections import *
import glob


tickers_file = 'stockId.txt'
with open(tickers_file) as f:
    tickers = [l.strip() for l in f.readlines()]

# path is where I save downloaded tickers
path = '/Users/andying/Sites/Trade/data/sz/'
# Yahoo API URL
url = "http://table.finance.yahoo.com/table.csv"
# Yahoo get parameters where date range 2011/01/01 - 2012/01/01
# although 2012/01/01 is an international holiday and won't be in the data
get_params = "s=%(t)s.sz&a=00&b=01&c=2011&d=05&e=20&f=2015&g=d&ignore=.csv"
url = '?'.join([url, get_params])
for t in tickers:
    r = requests.get(url % {'t': t})
    if r.status_code != 200:
        continue
    fname = os.path.join(path, '%(t)s_sz.csv' % {'t': t})
    with open(fname, 'w') as f:
        f.write(r.text)

c = Counter()
for fname in glob.glob(os.path.join(path, '*.csv')):
    fpath = os.path.join(path, fname)
    with open(fpath) as f:
        c.update({len(f.readlines()): 1})

print c.most_common()
