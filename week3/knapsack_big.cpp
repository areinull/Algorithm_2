#include <iostream>
#include <fstream>
#include <map>
#include <vector>

struct Element
{
	unsigned val;
	unsigned size;
};

struct Node
{
	unsigned x;
	unsigned v;
	Node *l;
	Node *r;
	Node(unsigned x_): x(x_), v(0), l(0), r(0) {}
};

int main(int argc, char *argv[])
{
	if (argc != 2)
	{
		std::cout << "Usage: " << argv[0] << " FILE" << std::endl;
		return 1;
	}

	std::ifstream ifs(argv[1]);
	unsigned w, n;
	ifs >> w >> n;
	std::cout << "Capacity: " << w << ", total elements: " << n << std::endl;

	Element *E = new Element[n];
	for (int i=0; i < n; ++i)
		ifs >> E[i].val >> E[i].size;

	typedef std::map<unsigned,Node*> level_t;
	typedef std::vector<level_t> list_t;

	list_t L(n);
	L[n-1].insert(std::make_pair(w,new Node(w)));

	std::cout << "<--" << std::endl;
	for (int i=n-2; i>=0; --i)
	{
		for (level_t::const_iterator N=L[i+1].begin(), end=L[i+1].end(); N != end; ++N)
		{
			if (!L[i].count(N->second->x))
				L[i].insert(std::make_pair(N->second->x, new Node(N->second->x)));
			N->second->l = L[i][N->second->x];
			if (N->second->x > E[i+1].size)
			{
				const unsigned x_new = N->second->x - E[i+1].size;
				if (!L[i].count(x_new))
					L[i].insert(std::make_pair(x_new, new Node(x_new)));
				N->second->r = L[i][x_new];
			}
		}
//		std::cout << i << std::endl;
	}

	std::cout << "-->" << std::endl;
	for (int i=0; i < n; ++i)
	{
		for (level_t::iterator N=L[i].begin(), end=L[i].end(); N != end; ++N)
		{
			unsigned t1 = 0, t2 = 0;
			if (N->second->l)
				t1 = N->second->l->v;
			if (N->second->r)
				t2 = N->second->r->v + E[i].val;
			N->second->v = std::max(t1,t2);
		}
//		std::cout << i << std::endl;
	}
	std::cout << "Ans: " << L[n-1][w]->v << std::endl;

	for (list_t::iterator it=L.begin(), end=L.end(); it != end; ++it)
		for (level_t::iterator it1=it->begin(), end1=it->end(); it1 != end1; ++it1)
			delete it1->second;
	delete [] E;
}

