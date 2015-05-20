import glob
from collections import Counter
import os

path = '/Users/andying/Sites/Trade/data/sz/'

c = Counter()
for fname in glob.glob(os.path.join(path, '*.csv')):
    fpath = os.path.join(path, fname)
    with open(fpath) as f:
        c.update({len(f.readlines()): 1})

for fname in glob.glob(os.path.join(path, '*.csv')):
    fpath = os.path.join(path, fname)
    with open(fpath) as f:
        if len(f.readlines()) >= 1100:
            continue
    os.remove(fpath)
