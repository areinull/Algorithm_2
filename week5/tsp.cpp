#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <limits>
#include <algorithm>
#include <cmath>
#include <assert.h>

struct Node
{
	float x,y;
};

typedef std::unordered_set<int> set_t;
typedef std::unordered_map<int, std::vector<float> > A_t;
typedef std::unordered_map<int, set_t> Level_t;

static int findSet(const Level_t &level, const set_t &s)
{
	for (Level_t::const_iterator it=level.cbegin(), end=level.cend(); it != end; ++it)
	{
		if (it->second == s)
			return it->first;
	}
	return -1;
}

static float dist(const Node &n1, const Node &n2)
{
	return std::sqrt((n1.x - n2.x)*(n1.x-n2.x) + (n1.y - n2.y)*(n1.y - n2.y));
}

static void printLevel(const Level_t &lvl)
{
	for (auto s=lvl.cbegin(), s_end=lvl.cend(); s != s_end; ++s)
	{
		std::cout << s->first << ": [";
		for (auto e=s->second.cbegin(), e_end = s->second.cend(); e != e_end; ++e)
		{
			std::cout << *e << ',';
		}
		std::cout << "]\n";
	}
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
	int cnt = 0;
	Level_t prev_level;
	Level_t cur_level;
	{
		set_t tmp;
		tmp.insert(0);
		cur_level[cnt++] = tmp;
	}
	A[findSet(cur_level, cur_level[0])] = std::vector<float>(1, 0.0f);

	for (int m=2; m <= N; ++m)
	{
//		std::cout << "-----------------\nS size: " << m << std::endl;
		std::cout << "S size: " << m << std::endl;
		for (Level_t::const_iterator it=prev_level.cbegin(), end=prev_level.cend(); it != end; ++it)
		{
			A.erase(it->first);
		}
		prev_level.swap(cur_level);
		cur_level.clear();
/*
		std::cout << "prev_level:\n";
		printLevel(prev_level);
		std::cout << std::endl;
*/		
		for (int new_p=1; new_p < N; ++new_p)
		{
			for (Level_t::const_iterator s_old=prev_level.cbegin(), end=prev_level.cend(); s_old != end; ++s_old)
			{
				set_t s_new(s_old->second);
				s_new.insert(new_p);
				if (s_new.size() == m && findSet(cur_level, s_new) == -1)
				{
/*
					std::cout << '[';
					for (auto e=s_new.cbegin(), e_end=s_new.cend(); e!=e_end; ++e)
					{
						std::cout << *e << ',';
					}
					std::cout << ']' << std::endl;
*/
					int s_new_idx = cnt++;
					A[s_new_idx].resize(N);
					A[s_new_idx][0] = std::numeric_limits<float>::infinity();
					cur_level[s_new_idx] = s_new;
					for (auto j=s_new.cbegin(), j_end=s_new.cend(); j != j_end; ++j)
					{
						if (*j == 0)
							continue;
						float curmin = std::numeric_limits<float>::infinity();
						set_t s_prev(s_new);
						s_prev.erase(*j);
						for (auto k=s_new.cbegin(), k_end=s_new.cend(); k != k_end; ++k)
						{
							if (*k == *j)
								continue;
							int s_prev_idx = findSet(prev_level, s_prev);
							assert(s_prev_idx != -1);
							curmin = std::min(curmin, A[s_prev_idx][*k] + dist(Nodes[*k],Nodes[*j]));
						}
						A[s_new_idx][*j] = curmin;
					}
				}
			}
		}
	}

	float curmin = std::numeric_limits<float>::infinity();
	for (int j=1; j<N; ++j)
	{
		curmin = std::min(curmin, A[cur_level.cbegin()->first][j] + dist(Nodes[j], Nodes[0]));
	}

	std::cout << "Result: " << curmin << std::endl;
}
