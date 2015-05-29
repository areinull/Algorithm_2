#!/usr/bin/env python
#coding:utf-8

import sys

if len(sys.argv) != 2:
	print 'Usage: %s FILE' % sys.argv[0]
	exit(1)

Nodes=[]
with open(sys.argv[1], 'r') as infile:
	N = int(infile.readline())
	print 'Total nodes:', N
	Nodes = tuple([tuple([float(x) for x in line.split()]) for line in infile.readlines()])

def dist(i,j):
	return ((Nodes[i][0]-Nodes[j][0])**2.0 + (Nodes[i][1]-Nodes[j][1])**2.0)**0.5


A = {}
prev_level = []
cur_level = [frozenset((0,))]
A[cur_level[0]] = {0: 0.0}

for m in xrange(2, N+1):
	print 'S size', m
	for s_old in prev_level:
		del A[s_old]
	prev_level = cur_level
	cur_level = []
	for new_p in xrange(1,N):
		for s_old in prev_level:
			s_new = frozenset(s_old | frozenset((new_p,)))
			if s_new not in A:
				A[s_new] = {0: float('inf')}
				cur_level.append(s_new)
				
				for j in s_new:
					if j == 0: continue
					curmin = float('inf')
					for k in s_new:
						if k == j: continue
						curmin = min(curmin, A[s_new-frozenset((j,))][k] + dist(k, j))
					A[s_new][j] = curmin

#assert cur_level == [frozenset(range(N))]
curmin = float('inf')
for j in xrange(1,N):
	curmin = min(curmin, A[cur_level[0]][j] + dist(j, 0))

print 'Result:', curmin
