#include "TSP.h"
#include <iostream>
#include <limits>
#include <assert.h>

#include <sys/time.h>

namespace {
double getUs() {
  struct timeval tv;
  gettimeofday(&tv, nullptr);
  return tv.tv_sec + (double)tv.tv_usec * 1E-6;
}
}

int main(int argc, const char *argv[])
{
  if (argc < 3) {
    std::cout << "example: ./a.out inputfile datafile" << std::endl;
    return -1;
  }
    /* crossoverProbability probability, mutation probability */
  TSP *tsp = new TSP(argv[1], argv[2], 0.8, 0.2);
  size_t generations = 0, generationsWithoutImprovement = 0;
  double bestFitness = -1;
  std::vector<double> executionTimes;
  double elapsedTime = 0;
  while(generationsWithoutImprovement < 100)
  {
    double before = getUs();
    tsp->nextPopulation();
    ++generations;
    double newFitness = tsp->getBestFitness();
    if(newFitness > bestFitness)
    {
      bestFitness = newFitness;
      generationsWithoutImprovement = 0;
    }
    else
    {
      ++generationsWithoutImprovement;
    }
    double after = getUs();
    executionTimes.push_back(after - before);
    elapsedTime += after - before;
  }
  // std::cerr << "Total Time: " << elapsedTime << " [s]" << std::endl;
  // std::cerr << "Average per loop: "
  //           << elapsedTime * 1E3 / executionTimes.size() << " [ms]"
  //           << std::endl;
  std::cout << "index" << std::endl;
  for (std::string::size_type i = 0; i < tsp->getBestPath().size(); i++)
    std::cout << tsp->getBestPath()[i] << std::endl;
  delete tsp;
  return 0;
}

