#!/usr/bin/env python
#coding:utf-8

import sys
import datetime

if len(sys.argv) != 2:
	print 'Usage: %s FILE' % sys.argv[0]
	exit(1)

stime = datetime.datetime.now()
print 'Start:', stime

Nodes=[]
with open(sys.argv[1], 'r') as infile:
	N = int(infile.readline())
	print 'Total nodes:', N
	Nodes = tuple([tuple([float(x) for x in line.split()]) for line in infile.readlines()])

def dist(x,y):
	return ((x[0]-y[0])**2.0 + (x[1]-y[1])**2.0)**0.5

input_time = datetime.datetime.now()
print 'Read input: step dur:', input_time - stime, 'from start:', input_time-stime

# generate subsets map
S_map = {}
cnt = 0
prev_init_sets = None
cur_init_sets = [frozenset((0,))]
S_map[frozenset((0,))] = cnt
cnt += 1

for k in xrange(1,N):
	prev_init_sets = cur_init_sets
	cur_init_sets = []
	for m in xrange(1,N):
		for S in prev_init_sets:
			S_new = frozenset(S | frozenset((m,)))
			if S_new not in S_map:
				S_map[S_new] = cnt
				cnt += 1
				cur_init_sets.append(S_new)

#print S_map
subsets_time = datetime.datetime.now()
print 'Generate subsets map: step dur:', subsets_time - input_time, 'from start:', subsets_time-stime


# init A array
A=[]
for s in xrange(len(S_map)):
	A.append([])
	for n in xrange(N):
		A[s].append(None)
for S in S_map:
	if S == frozenset((0,)):
		A[S_map[S]][0] = 0.0
	else:
		A[S_map[S]][0] = float('inf')
#print A
initA_time = datetime.datetime.now()
print 'Init A array: step dur:', initA_time - subsets_time, 'from start:', initA_time-stime


# fill up A array
for m in xrange(2, N+1):
	for S in S_map:
		if len(S) == m:
			for j in S:
				if j == 0: continue
				#print 'S:', S, 'j:', j
				curmin = None
				for k in S:
					if k == j: continue
					tmp = A[S_map[S-frozenset((j,))]][k] + dist(Nodes[k], Nodes[j])
					if curmin is None or tmp < curmin:
						curmin = tmp
				A[S_map[S]][j] = curmin

fillA_time = datetime.datetime.now()
print 'Fill A array: step dur:', fillA_time - initA_time, 'from start:', fillA_time-stime

# return answer
curmin = None
fulls_idx = S_map[frozenset(range(N))]
for j in xrange(1,N):
	tmp = A[fulls_idx][j] + dist(Nodes[j], Nodes[0])
	if curmin is None or tmp < curmin:
		curmin = tmp

ans_time = datetime.datetime.now()
print 'Get answer: step dur:', ans_time - fillA_time, 'from start:', ans_time-stime

print 'Result:', curmin
