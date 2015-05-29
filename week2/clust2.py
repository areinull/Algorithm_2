#!/usr/bin/env python
# coding:utf-8

import sys

if len(sys.argv) != 2:
	print 'Usage: %s FILE' % sys.argv[0]
	exit(1)

class Edge:
	def __init__(self, v1, v2, cost):
		self.v1=v1
		self.v2=v2
		self.cost=cost

	def __str__(self):
		return '%d <-> %d (%d)' % (self.v1,self.v2,cost)

class V:
	def __init__(self, v):
		self.v=v
		self.lead=self
		self.size=1


class CC:
	def __init__(self, v):
		self.V=set((v,))
		self.lead=v.lead
	def __str__(self):
		return 'Lead: {}, '.format(self.lead.v) + ','.join([str(e.v) for e in self.V])

	@staticmethod
	def merge(CC1, CC2):
		if CC1.lead.size > CC2.lead.size:
			CC_b = CC1
			CC_s = CC2
		else:
			CC_b = CC2
			CC_s = CC1
		CC_b.V |= CC_s.V
		CC_b.lead.size += CC_s.lead.size
		for v in CC_s.V:
			v.lead = CC_b.lead
		return CC_b

	@staticmethod
	def closest(CC_list, E):
		assert len(CC_list) >= 2
		best_e=None
		for e in E:
			if e.v1.lead == e.v2.lead:
				continue
			if best_e is not None and e.cost >= best_e.cost:
				continue
			best_e = e
		assert best_e is not None
		CC1=None
		CC2=None
		for CC in CC_list:
			if CC1 is not None and CC2 is not None:
				break
			if CC1 is None and best_e.v1 in CC.V:
				CC1 = CC
			if CC2 is None and best_e.v2 in CC.V:
				CC2 = CC
		assert CC1 is not None
		assert CC2 is not None
		assert CC1 != CC2
		return CC1,CC2,best_e.cost

E=[]
with open(sys.argv[1], 'r') as fd:
	v_cnt = int(fd.readline())
	CC_list = [CC(V(v)) for v in range(1,v_cnt+1)]
	for line in fd.readlines():
		v1,v2,cost = [int(e) for e in line.split()]
		E.append(Edge(CC_list[v1-1].lead,CC_list[v2-1].lead,cost))


while len(CC_list) > 1:
	CC1,CC2,bec = CC.closest(CC_list,E)
	print bec
	if bec > 1:
		break
	CC_list.remove(CC1)
	CC_list.remove(CC2)
	CC_new = CC.merge(CC1,CC2)
	CC_list.append(CC_new)
print '\n'.join([str(e) for e in CC_list])
