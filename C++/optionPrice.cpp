#include <iostream>
#include <random>
#include <cmath>
using namespace std;

// payoff from the European call option
double payoff(double S,double strikePrice)
{
  return max( S - strikePrice , 0. ); // change this line here to solve for different European options
}

double monteCarlo(double S0,double strikePrice,double interestRate,double sigma,double maturity,int N)
{
  // declare the random number generator
  static mt19937 rng;
  // declare the distribution
  normal_distribution<> ND(0.,1.);
  ND(rng);
  // initialise sum
  double sum=0.;
  for(int i=0;i<N;i++)
  {
    double phi=ND(rng);
    // calculate stock price at T
    double ST=S0 * exp( (interestRate - 0.5*sigma*sigma)*maturity + phi*sigma*sqrt(maturity) );
    // add in payoff
    sum = sum + payoff(ST,strikePrice);
  }
  // return discounted value
  return sum/N*exp(-interestRate*maturity);
}

int main()
{
  // run for different 
  for(int M=100;M<=100000;M*=10)
  {
  // now store all the results
  vector<double> samples(M);
  // number of paths in each calculation
  int N=1000;

  cout << " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"<<endl;
  cout << " Run results with M="<<M<<" samples from V_N, where N="<<N<<"."<<endl;
  
  // run some calculations
  for(int i=0;i<M;i++)
  {
    samples[i] = monteCarlo(9.576,10.,0.05,0.4,0.75,N);
  }
  // estimate the mean from the sample
  double sum=0.;
  for(int i=0;i<M;i++)
  {
    sum+=samples[i];
  }
  double mean = sum/M;
  cout << " mean = " << mean << endl;

  // estimate the variance from the sample
  double sumvar=0.;
  for(int i=0;i<M;i++)
  {
    sumvar+=(samples[i]-mean)*(samples[i]-mean);
  }
  double variance = sumvar/(M-1);
  cout << " variance = " << variance << endl; 
  
  // get the standard deviation of the sample mean
  double sd = sqrt(variance/M);
  cout << " 95% confident result is in ["<<mean-2.*sd << "," << mean+2.*sd << "] with "<< N*M << " total paths." << endl;
  }
}