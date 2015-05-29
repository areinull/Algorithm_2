#!/usr/bin/env python
# coding:utf-8

import sys

if len(sys.argv) != 2:
	print 'source file required'
	exit(1)

with open(sys.argv[1],'r') as src:
	v_cnt, e_cnt = src.readline().split()
	print 'V size:', v_cnt, 'E size:', e_cnt
	V = set(xrange(1,1+int(v_cnt)))
	E = [(int(x),int(y),int(l)) for x,y,l in [line.split() for line in src.readlines()]]

X = set((1,))
T = []
while not X == V:
	best = (None,None,sys.maxint)
	for e in E:
		if (e[0] in X and e[1] not in X or e[0] not in X and e[1] in X) and e[2] < best[2]:
			best = e
	assert best[0] is not None
	X.add(best[0])
	X.add(best[1])
	T.append(best)

ans = sum([x[2] for x in T])
print ans
			
