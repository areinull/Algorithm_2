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
		self.x_ = x
		self.y_ = y
		self.fn = self.getFn(x,y)

	def __str__(self):
		return 'Clause: ' + str(self.x_) + ' '  + str(self.y_)

	def check(self, A):
		return self.fn(A[self.x],A[self.y])

def preprocess(C):
	while True:
		print 'C size:', len(C)
		cc = {}
		used = set()
		for i,c in enumerate(C):
			if c.x not in used:
				if -c.x_ in cc:
					del cc[-c.x_]
					used.add(c.x)
				else:
					if c.x_ not in cc:
						cc[c.x_] = []
					cc[c.x_].append(i)
			if c.y not in used:
				if -c.y_ in cc:
					del cc[-c.y_]
					used.add(c.y)
				else:
					if c.y_ not in cc:
						cc[c.y_] = []
					cc[c.y_].append(i)
		if len(cc) == 0:
			return C
		for k in cc:
			for i in cc[k]:
				C[i] = None
		C = [e for e in C if e is not None]
						

C = []
with open(sys.argv[1],'r') as infile:
	N = int(infile.readline())
	print 'Total:', N
	
	for line in infile:
		x,y = [int(e) for e in line.split()]
		C.append(Clause(x,y))

assert len(C) == N

C = preprocess(C)

if len(C) == 0:
	res = True
else:
	res = False
totalLoop = int(math.ceil(math.log(N,2)))
totalInner = 2*N

for i in xrange(totalLoop):
	if res: break
	print 'Outer loop %d of %d' % (i+1, totalLoop)
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
