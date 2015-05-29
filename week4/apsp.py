#!/usr/bin/env python
#coding:utf-8

import sys

if len(sys.argv) != 2:
	print 'Usage: %s FILE' % sys.argv[0]
	exit(1)

class Edge:
	def __init__(self, tail, head, weight):
		self.t = tail
		self.h = head
		self.w = weight

E = []
V = {}

with open(sys.argv[1],'r') as infile:
	v_cnt, e_cnt = [int(e) for e in infile.readline().split()]
	print 'Total V %d, total E %d' % (v_cnt, e_cnt)
	for line in infile.readlines():
		t,h,w = map(int, line.split())
		t -= 1
		h -= 1
		e = Edge(t,h,w)
		E.append(e)
		if t not in V:
			V[t] = []
		V[t].append(e)

assert len(E) == e_cnt
assert len(V) == v_cnt

print 'Init A'
A_cur = [[sys.maxint for _2 in xrange(v_cnt)] for _1 in xrange(v_cnt)]
A_prev = [[sys.maxint for _2 in xrange(v_cnt)] for _1 in xrange(v_cnt)]
for i in xrange(v_cnt):
	for j in xrange(v_cnt):
		if i == j:
			A_cur[i][j] = 0
		else:
			for e in V[i]:
				if e.h == j:
					A_cur[i][j] = e.w
					break
print 'Fill A'
for k in xrange(1,v_cnt):
	A_prev, A_cur = A_cur, A_prev
	for i in xrange(v_cnt):
		for j in xrange(v_cnt):
			A_cur[i][j] = min(A_prev[i][j], A_prev[i][k]+A_prev[k][j])

print 'Find answer'
cur_min = sys.maxint
for i in xrange(v_cnt):
	for j in xrange(v_cnt):
		if i == j:
			if A_cur[i][j] < 0:
				print 'Found negative cycle', i
				exit(0)
		else:
			cur_min = min(cur_min, A_cur[i][j])

print 'Answer:', cur_min
