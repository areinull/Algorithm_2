#include <iostream>
#include <algorithm>
#include <fstream>
#include <vector>
#include <assert.h>
#include <limits>

struct Edge
{
	int t;
	int h;
	int w;
	Edge(int tail, int head, int weight): t(tail), h(head), w(weight) {}
};

typedef std::vector<Edge> Edges_t;
typedef std::vector<Edges_t> AdjList_t;

int main(int argc, char **argv)
{
	if (argc != 2)
	{
		std::cout << "Usage: " << argv[0] << " FILE" << std::endl;
		return 1;
	}

	std::ifstream infile(argv[1]);
	int n, m;
	infile >> n >> m;
	
	AdjList_t V(n);
	for (int line=0; line < m; ++line)
	{
		int t,h,w;
		infile >> t >> h >> w;
		--t;
		--h;
		V[t].push_back(Edge(t,h,w));
	}

	infile.close();
	std::cout << "Total V " << n << ", total E " << m << std::endl;

	assert(V.size() == n);

	std::cout << "Init A" << std::endl;
	std::vector<int> A_cur(n*n);
	std::vector<int> A_prev(n*n);
	for (int i = 0; i < n; ++i)
		for (int j = 0; j < n; ++j)
		{
			if (i == j)
				A_cur[i*n+j] = 0;
			else
			{
				int min_w = std::numeric_limits<int>::max();
				for (Edges_t::const_iterator it=V[i].begin(), end=V[i].end(); it != end; ++it)
				{
					if (it->h == j && it->w < min_w)
					{
						min_w = it->w;
					}
				}
				A_cur[i*n + j] = min_w;
			}
		}

	std::cout << "Fill A" << std::endl;
	for (int k = 1; k < n; ++k)
	{
		A_cur.swap(A_prev);
		for (int i = 0; i < n; ++i)
			for (int j = 0; j < n; ++j)
			{
				int tmp = A_prev[i*n+k]+A_prev[k*n+j];
				if (A_prev[i*n+k] == std::numeric_limits<int>::max() || A_prev[k*n+j] == std::numeric_limits<int>::max())
					tmp = std::numeric_limits<int>::max();
				A_cur[i*n+j] = std::min(A_prev[i*n+j], tmp);
			}
	}

	std::cout << "Find answer" << std::endl;
	int cur_min = std::numeric_limits<int>::max();
	for (int i = 0; i < n; ++i)
		for (int j = 0; j < n; ++j)
		{
			if (i == j)
			{
				if (A_cur[i*n+j] < 0)
				{
					std::cout << "Found negative cycle " << i << std::endl;
					return 0;
				}
			}
			else
			{
				cur_min = std::min(cur_min, A_cur[i*n+j]);
			}
		}

	std::cout << "Answer: " << cur_min << std::endl;
}

