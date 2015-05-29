#!/usr/bin/env python
#coding:utf-8

def aprint(A):
	for row in A:
		print
		for e in row:
			print '%4f' % e,
	print

w = (0.05, 0.4, 0.08, 0.04, 0.1, 0.1, 0.23)

A = []
for i in xrange(len(w)):
	A.append([])
	for j in xrange(len(w)):
		A[i].append(0)


for s in xrange(len(w)):
	for i in xrange(len(w)-s):
		pk = sum(w[i:i+s+1])
		tmp = []
		for r in xrange(i,i+s+1):
			if i > r-1:
				a1 = 0
			else:
				a1 = A[i][r-1]
			if r+1 > i+s:
				a2 = 0
			else:
				a2 = A[r+1][i+s]
			tmp.append(a1+a2)
		A[i][i+s] = pk + min(tmp)
#		print 's: %d i: %d pk: %f tmp: %s' % (s,i,pk,str(tmp))
#		aprint(A)
aprint(A)
