#!/usr/bin/env python
#coding:utf-8

import sys

if len(sys.argv) != 2:
	print 'Usage: %s FILE' % sys.argv[0]
	exit(1)

with open(sys.argv[1],'r') as infile:
	w, n = [int(e) for e in infile.readline().split()]
	print 'Capacity: %d, total elements: %d' % (w,n)
	e = tuple([tuple([int(e) for e in line.split()]) for line in infile.readlines()])


class Node:
	def __init__(self, x):
		self.x=x
		self.v=None
		self.l=None
		self.r=None


L = [{} for _ in xrange(n)]
L[n-1][w] = Node(w)
print '<--'
for i in xrange(n-2,-1,-1):
	L[i] = {}
	for N in L[i+1].itervalues():
		if N.x not in L[i]:
			L[i][N.x] = Node(N.x)
		N.l = L[i][N.x]
		if N.x > e[i+1][1]:
			x_new = N.x - e[i+1][1]
			if x_new not in L[i]:
				L[i][x_new] = Node(x_new)
			N.r = L[i][x_new]
	#print 'Level %d: size %d' % (i, len(L[i]))
	print i

print '-->'
for i in xrange(n):
	for N in L[i].itervalues():
		if N.l is None:
			t1 = 0
		else:
			t1 = N.l.v
		if N.r is None:
			t2 = 0
		else:
			t2 = N.r.v + e[i][0]
		N.v = max(t1,t2)
	print i

print 'Ans:', L[n-1][w].v
