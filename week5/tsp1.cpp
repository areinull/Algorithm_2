#include <iostream>
#include <fstream>
#include <vector>
#include <forward_list>
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
typedef std::forward_list<set_t> Level_t;

static float dist(const Node &n1, const Node &n2)
{
	return std::sqrt((n1.x - n2.x)*(n1.x-n2.x) + (n1.y - n2.y)*(n1.y - n2.y));
}

static int getIdx(const set_t &s)
{
	int acc = 0;
	for (auto e=s.cbegin(), end=s.cend(); e!=end; ++e)
	{
		acc |= 1 << *e;
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
		set_t tmp;
		tmp.insert(0);
		cur_level.push_front(tmp);
	}
	A[getIdx(cur_level.front())] = std::vector<float>(1, 0.0f);

	for (int m=2; m <= N; ++m)
	{
		std::cout << "S size: " << m << std::endl;
		for (auto it=prev_level.cbegin(), end=prev_level.cend(); it != end; ++it)
		{
			A.erase(getIdx(*it));
		}
		prev_level.swap(cur_level);
		cur_level.clear();

		for (int new_p=1; new_p < N; ++new_p)
		{
			for (auto s_old=prev_level.cbegin(), end=prev_level.cend(); s_old != end; ++s_old)
			{
				set_t s_new(*s_old);
				s_new.insert(new_p);
				const int s_new_idx = getIdx(s_new);
				if (s_new.size() == m && !A.count(s_new_idx))
				{
					A[s_new_idx].resize(N);
					A[s_new_idx][0] = std::numeric_limits<float>::infinity();
					cur_level.push_front(s_new);
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
							int s_prev_idx = getIdx(s_prev);
							assert(A.count(s_prev_idx) > 0);
							curmin = std::min(curmin, A[s_prev_idx][*k] + dist(Nodes[*k],Nodes[*j]));
						}
						A[s_new_idx][*j] = curmin;
					}
				}
			}
		}
	}

	float curmin = std::numeric_limits<float>::infinity();
	const int finIdx = getIdx(cur_level.front());
	for (int j=1; j<N; ++j)
	{
		curmin = std::min(curmin, A[finIdx][j] + dist(Nodes[j], Nodes[0]));
	}

	std::cout << "Result: " << curmin << std::endl;
}
