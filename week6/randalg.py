#!/usr/bin/env python
#coding:utf-8

import sys
import random
import math

if len(sys.argv) != 2:
	print 'Usage: %s FILE' % sys.argv[0]
	exit(1)

class Clause:
	@staticmethod
	def getFn(x, y):
		if x >=0 and y >= 0:
			return lambda a,b: a or b
		elif x < 0 and y >= 0:
			return lambda a,b: not a or b
		elif x >= 0 and y < 0:
			return lambda a,b: a or not b
		else:
			return lambda a,b: not a or not b

	@staticmethod
	def checkAll(C,A):
		for i,c in enumerate(C):
			if not c.check(A):
				return False, i
		return True, None

	def __init__(self, x, y):
		self.x = abs(x)
		self.y = abs(y)
		self.fn = self.getFn(x,y)

	def check(self, A):
		return self.fn(A[self.x],A[self.y])

C = []
with open(sys.argv[1],'r') as infile:
	N = int(infile.readline())
	print 'Total:', N
	
	for line in infile:
		x,y = [int(e) for e in line.split()]
		C.append(Clause(x,y))

assert len(C) == N

res = False
totalLoop = int(math.ceil(math.log(N,2)))
totalInner = 2*N*N
for i in xrange(totalLoop):
	print 'Outer loop %d of %d' % (i+1, totalLoop)
	if res: break
	A = [random.choice((True,False)) for _ in xrange(N+1)]
	prevProg = -1
	for j in xrange(totalInner):
		progress = int(j*100./totalInner)
		if progress != prevProg and progress % 10 == 0:
			print '%d %%' % int(progress)
			prevProg = progress
		random.shuffle(C)
		isSat, k = Clause.checkAll(C,A)
		if isSat:
			res = True
			break
		m = random.choice((C[k].x,C[k].y))
		A[m] = not A[m]

print 'Answer:', res
