from collections import defaultdict


s = 'kjfjfhfjsnfsdcnfhuiefhsjdn'

d = {}

for c in s:
    if c not in d:
        d[c] = 0
    d[c] += 1


print(d)

d = {}
for c in s:
    d.setdefault(c, 0)
    d[c] += 1



d = defaultdict(int)

for c in s:
    d[c] += 1

print(d)
