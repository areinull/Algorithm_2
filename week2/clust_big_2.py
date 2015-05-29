#!/usr/bin/env python
#coding:utf-8

import sys

if len(sys.argv) != 2:
	print 'Usage: %s FILE' % sys.argv[0]
	exit(1)

raw_v=set()
with open(sys.argv[1],'r') as infile:
	total, elsize = [int(e) for e in infile.readline().split()]
	print 'Total:',total,' elsize:',elsize
	for line in infile:
		raw_v.add(int(''.join(line.split()), base=2))

print 'Unique:',len(raw_v)
print 'Input read'

V={}
for i,v in enumerate(raw_v):
	V[v]=i


dist=[]
for i in xrange(elsize):
	dist.append(2**i)
	for j in xrange(i+1, elsize):
		dist.append(2**i+2**j)
print 'dist calculated'

E=set()
for d in dist:
	for src in V:
		another = d ^ src
		if another in V and (V[another],V[src]) not in E:
			E.add((V[src],V[another]))

E=list(E)
print 'edges found'

V1={}
for v in xrange(len(raw_v)):
	V1[v]=set()

for e in E:
	V1[e[0]].add(e[1])
	V1[e[1]].add(e[0])

print 'graph generated'

V_all=set(range(len(raw_v)))
clust_cnt=0
#clust=[]
while len(V_all)>0:
	print 'clust_cnt:',clust_cnt
	q = [V_all.pop()]
	V_all.add(q[0])
	clust_cnt += 1
#	clust.append([])
	while len(q)>0:
		cur = q.pop()
#		print 'cur:',cur,
		if cur not in V_all:
#			print 'not in V_all'
			continue
#		else:
#			clust[-1].append(cur)
		V_all.remove(cur)
		q.extend(tuple(V1[cur]))
#		print

print 'Clusters:',clust_cnt
#print clust
