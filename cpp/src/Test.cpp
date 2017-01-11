//============================================================================
// Name        : Test.cpp
// Author      : Martin Takac
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
using namespace std;

#include <vector>
#include <stdio.h>      /* printf, scanf, puts, NULL */
#include <stdlib.h>     /* srand, rand */
#include <time.h>

#include <time.h>
#include <sys/time.h>


double get_wall_time(){
    struct timeval time;
    if (gettimeofday(&time,NULL)){
        //  Handle error
        return 0;
    }
    return (double)time.tv_sec + (double)time.tv_usec * .000001;
}

int main() {

	int N = 203;
	int d = 40;

	std::vector<double> distances(N * N, 0);
	std::vector<double> B(d * d, 0);

	cout << "Started" << endl;
	std::vector<double> features(N * d);
	for (int i = 0; i < features.size(); i++) {
		features[i] = rand() / (RAND_MAX + 0.0);
	}
	for (int i = 0; i < B.size(); i++) {
		B[i] = rand() / (RAND_MAX + 0.0);
	}

	cout << "Going to compute Distance" << endl;
	double start = get_wall_time();
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			int idx = i * N + j;
			for (int k = 0; k < d; k++) {
				for (int l = 0; l < d; l++) {

					distances[idx] +=  (features[i * d + k] - features[j * d + k]) * B[k * d + l]
								* (features[i * d + l]
								- features[j * d + l]);
				}
			}

		}
	}
	double end = get_wall_time();
	cout << "DONE " << end-start << endl;
	return 0;
}
