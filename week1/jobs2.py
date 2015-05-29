#!/usr/bin/env python
# coding:utf-8

import sys

if len(sys.argv) != 2:
	print 'source file required'
	exit(1)

with open(sys.argv[1],'r') as src:
	cnt = int(src.readline())
	print 'Jobs total:', cnt
	jobs = [(int(w),int(l),float(w)/float(l)) for w,l in [line.split() for line in src.readlines()]]

schedule=[]
while len(jobs) > 0:
	best = jobs[0]
	best_idx = 0
	for i in xrange(1,len(jobs)):
		if jobs[i][2] > best[2] or (jobs[i][2] == best[2] and jobs[i][0] > best[0]):
			best = jobs[i]
			best_idx = i
	schedule.append(best)
	del jobs[best_idx]

ans = 0
cur_time = 0
for j in schedule:
	cur_time += j[1]
	ans += j[0]*cur_time
print ans
