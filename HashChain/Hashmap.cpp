#include "hash_func.h"
#include <iostream>
#include <windows.h>
using namespace std;

int main() {
	
	HashMap H;
	HashMap1 H1;
	double t1, t2,t3;
	int* value = new int;
	t1 = GetTickCount64();
	for (int i = 0; i < 100000; i++)
	{
		H.put(i, i * 4);
		//printf("Input <%d,*d>", i, i * 4);
	}
	
	for (int i = 99999; i >= 0; i--)
	{
		//cout << i << "," << i*4 << endl;
		H.get(i, *value);
			//cout <<i<<","<< *value << endl;
	}
	t2 = GetTickCount64();
	for (int i = 0; i < 10000000; i++)
	{
		H1.put(i, i * 4);
		//printf("Input <%d,*d>", i, i * 4);
	}

	for (int i = 99999; i >= 0; i--)
	{
		//cout << i << "," << i*4 << endl;
		H1.get(i, *value);
		//cout <<i<<","<< *value << endl;
	}
	t3 = GetTickCount64();
	cout << "New time = " << ((t2 - t1) * 1.0 ) << endl;
	cout << "Old time = " << ((t3 - t2) * 1.0 ) << endl;
}
