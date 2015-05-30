#include <iostream>
#include <vector>
#include <stdlib.h>
#include <fstream>
#include <cmath>

struct Clause
{
	int x;
	int y;
	bool (*fn)(bool a, bool b);

	Clause(int x_, int y_): x(abs(x_)), y(abs(y_))
	{
		if (x_ >= 0 && y_ >= 0)
			fn = [](bool a, bool b) { return a || b; };
		else if (x_ < 0 && y_ >= 0)
			fn = [](bool a, bool b) { return !a || b; };
		else if (x_ >= 0 && y_ < 0)
			fn = [](bool a, bool b) { return a || !b; };
		else
			fn = [](bool a, bool b) { return !a || !b; };
	}

	bool check(const std::vector<bool> &A) const
	{
		return (*fn)(A[x],A[y]);
	}

	static int checkAll(const std::vector<Clause> &C, const std::vector<bool> &A)
	{
		for (int i=0; i < C.size(); ++i)
		{
			if (!C[i].check(A))
				return i;
		}
		return -1;
	}
};

static void randomize(std::vector<bool> &A)
{
	for (int i=0; i < A.size(); ++i)
	{
		A[i] = (rand() % 2)? true: false;
	}
}


int main(int argc, char *argv[])
{
	if (argc != 2)
	{
		std::cout << "Usage: " << argv[0] << " FILE" << std::endl;
		return 1;
	}

	std::vector<bool> A;
	std::vector<Clause> C;

	std::ifstream infile(argv[1]);
	int N;
	{
		int x,y;
		infile >> N;
		std::cout << "Total: " << N << std::endl;
		A = std::vector<bool>(N+1);
		C.reserve(N);
		for (int i=0; i<N; ++i)
		{
			infile >> x >> y;
			C.push_back(Clause(x,y));
		}
	}
	infile.close();

	bool res = false;
	const int totalLoop = std::ceil(std::log2(N));
	//const unsigned long long totalInner = 2*N*N;
	const unsigned long long totalInner = N;
	for (int i=1; i<=totalLoop && !res; ++i)
	{
		std::cout << "Outer loop " << i << " of " << totalLoop << std::endl;
		randomize(A);
		int prevProg = -1;
		for (unsigned long long j=0; j<totalInner; ++j)
		{
			const int progress = j*100./totalInner;
			if (progress != prevProg)
			{
				std::cout << progress << " %" << std::endl;
				prevProg = progress;
			}
			const int k = Clause::checkAll(C,A);
			if (k == -1)
			{
				res = true;
				break;
			}
			int m;
			if (rand() % 2)
				m = C[k].x;
			else
				m = C[k].y;
			A[m] = !A[m];
		}
	}
	std::cout << "Answer: " << res << std::endl;
}
