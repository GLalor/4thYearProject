#include <iostream>
#include <math.h>
#include <random>
#include <cmath>
using namespace std;

// payoff from the European call option
//double payoff(double S, double strikePrice)
//{
//	return max(S - strikePrice, 0.); // change this line here to solve for different European options
//}
__global__
void monteCarlo(int X,float *S0, float *strikePrice, float *interestRate, float *sigma, float *maturity, int N)
{
	// declare the random number generator
	static mt19937 rng;
	// declare the distribution
	normal_distribution<> ND(0., 1.);
	ND(rng);
	// initialise sum
	double sum = 0.;
	for (int i = 0; i<N; i++)
	{
		int index = threadIdx.x;
		int stride = blockDim.x;
		for (int i = index; i < X; i += stride) {
			double phi = ND(rng);
			// calculate stock price at T
			double ST = S0[i] * exp((interestRate[i] - 0.5*sigma[i] *sigma[i])*maturity[i] + phi*sigma[i] * (maturity[i] * maturity[i]));
			// add in payoff
			sum = sum + max(ST - strikePrice[i], 0.0);
		}
	}
	// return discounted value
	//return sum / N*exp(-interestRate*maturity);
}

int main()
{
	int X = 1 << 20;
	float *x, *y, *j, *k, *l;

	// Allocate Unified Memory – accessible from CPU or GPU
	cudaMallocManaged(&x, X * sizeof(float));
	cudaMallocManaged(&y, X * sizeof(float));
	cudaMallocManaged(&j, X * sizeof(float));
	cudaMallocManaged(&k, X * sizeof(float));
	cudaMallocManaged(&l, X * sizeof(float));

	// initialize x and y arrays on the host
	for (int i = 0; i < X; i++) {
		x[i] = 9.576;
		y[i] = 10.0f;
		j[i] = 0.05f;
		k[i] = 0.04;
		l[i] = 0.75f;
	}
	// run for different 
	for (int M = 100; M <= 10000; M *= 10)
	{
		int N = 10000;
		// now store all the results
		vector<double> samples(M);
		

		
		cout << " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" << endl;
		cout << " Run results with M=" << M << " samples from V_N, where N=" << N << "." << endl;

		// run some calculations
		for (int i = 0; i<M; i++)
		{
			int blockSize = 256;
			int numBlocks = (N + blockSize - 1) / blockSize;
			// Run kernel on 1M elements on the GPU
			monteCarlo <<<numBlocks, blockSize>>>(X,x, y, j, k, l, N);
			// Wait for GPU to finish before accessing on host
			cudaDeviceSynchronize();
		}
		// estimate the mean from the sample
		double sum = 0.;
		for (int i = 0; i<M; i++)
		{
			sum += samples[i];
		}
		double mean = sum / M;
		cout << " mean = " << mean << endl;

		// estimate the variance from the sample
		double sumvar = 0.;
		for (int i = 0; i<M; i++)
		{
			sumvar += (samples[i] - mean)*(samples[i] - mean);
		}
		double variance = sumvar / (M - 1);
		cout << " variance = " << variance << endl;

		// get the standard deviation of the sample mean
		double sd = sqrt(variance / M);
		cout << " 95% confident result is in [" << mean - 2.*sd << "," << mean + 2.*sd << "] with " << N*M << " total paths." << endl;

	}
	// Free memory
	cudaFree(x);
	cudaFree(y);
	cudaFree(j);
	cudaFree(k);
	cudaFree(l);
}