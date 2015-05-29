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

A = [[0 for x in xrange(w+1)] for i in xrange(n)]

for i in xrange(1,n):
	for x in xrange(w+1):
		if e[i][1] > x:
			A[i][x] = A[i-1][x]
		else:
			A[i][x] = max(A[i-1][x], A[i-1][x-e[i][1]]+e[i][0])

print 'Ans:', A[n-1][w]
