#!/usr/bin/env python
#coding:utf-8

import sys

if len(sys.argv) != 2:
	print 'Usage: %s FILE' % sys.argv[0]
	exit(1)

data = []
with open(sys.argv[1],'r') as fd:
	total,elsize = [int(e) for e in fd.readline().split()]
	print 'Total: %d, element size: %d' % (total, elsize)
	for line in fd.readlines():
		data.append(tuple([int(e) for e in line.split()]))

res=0
exclude=set()
for i in xrange(total-1):
	if i in exclude:
		continue
	res+=1
	for j in xrange(i+1, total):
		s=0
		for k in xrange(elsize):
			if data[i][k] != data[j][k]:
				s+=1
		if s <= 2:
			exclude.add(j)

print 'Result:',res
