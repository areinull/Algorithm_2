#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <set>
#include <limits>
#include <algorithm>
#include <cmath>
#include <assert.h>

struct Node
{
	float x,y;
};

typedef int set_t;
typedef std::map<set_t, std::vector<float> > A_t;
typedef std::set<set_t> Level_t;

static float dist(const Node &n1, const Node &n2)
{
	return std::sqrt((n1.x - n2.x)*(n1.x-n2.x) + (n1.y - n2.y)*(n1.y - n2.y));
}

static void setInsert(set_t &s, int v)
{
	assert(v < 32);
	s |= 1 << v;
}

static void setErase(set_t &s, int v)
{
	assert(v < 32);
	s &= ~(1 << v);
}

static int setSize(set_t s)
{
	int acc = 0;
	while (s)
	{
		acc += s & 1;
		s >>= 1;
	}
	return acc;
}

int main(int argc, char *argv[])
{
	if (argc != 2)
	{
		std::cout << "Usage: " << argv[0] << " FILE" << std::endl;
		return 1;
	}

	std::ifstream infile(argv[1]);
	int N;
	float x, y;
	infile >> N;
	std::cout << "Total nodes: " << N << std::endl;
	std::vector<Node> Nodes(N);
	for (int i=0; i<N; ++i)
	{
		infile >> x >> y;
		Nodes[i].x = x;
		Nodes[i].y = y;
	}
	infile.close();

	A_t A;
	Level_t prev_level;
	Level_t cur_level;
	{
		set_t tmp = 0;
		setInsert(tmp, 0);
		cur_level.insert(tmp);
	}
	A[*cur_level.cbegin()] = std::vector<float>(1, 0.0f);

	for (int m=2; m <= N; ++m)
	{
		std::cout << "S size: " << m << std::endl;
		for (auto it=prev_level.cbegin(), end=prev_level.cend(); it != end; ++it)
		{
			A.erase(*it);
		}
		prev_level.swap(cur_level);
		cur_level.clear();

		for (int new_p=1; new_p < N; ++new_p)
		{
			for (auto s_old=prev_level.cbegin(), end=prev_level.cend(); s_old != end; ++s_old)
			{
				set_t s_new(*s_old);
				setInsert(s_new, new_p);
				if (setSize(s_new) == m && !A.count(s_new))
				{
					A[s_new].resize(N);
					A[s_new][0] = std::numeric_limits<float>::infinity();
					cur_level.insert(s_new);
					for (int j=1; j<N; ++j)
					{
						if ((s_new & (1<<j)) == 0)
							continue;
						float curmin = std::numeric_limits<float>::infinity();
						set_t s_prev(s_new);
						setErase(s_prev, j);
						for (int k=0; k<N; ++k)
						{
							if (k == j || (s_new & (1<<k)) == 0)
								continue;
							assert(A.count(s_prev));
							curmin = std::min(curmin, A[s_prev][k] + dist(Nodes[k],Nodes[j]));
						}
						A[s_new][j] = curmin;
					}
				}
			}
		}
	}

	float curmin = std::numeric_limits<float>::infinity();
	for (int j=1; j<N; ++j)
	{
		curmin = std::min(curmin, A[*cur_level.cbegin()][j] + dist(Nodes[j], Nodes[0]));
	}

	std::cout << "Result: " << curmin << std::endl;
}
