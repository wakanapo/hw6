#pragma once
#include <cstdio>
#include <string>
#include <vector>

class TSP
{
  struct Position {
    double x;
    double y;
  };

  public:
  TSP(std::string inputfile, std::string datafile,
      const double crossoverProbability, const double mutationProbability);
  void setFirstPopulation(std::string filename);
    void nextPopulation();
    double getBestFitness() const;
    std::vector<int> getBestPath() const;
    double getLowestTotalDistance() const;
    double getAverageDistance() const;
    
  private:
    const double crossoverProbability, mutationProbability;
    double totalDistance(std::vector<int>* chromosone) const;
    std::vector<Position> m_cities;
    std::vector<int>* bestChromosone;
    std::vector<std::vector<int>*> solutions;
    std::vector<std::vector<int>*> newPopulation;
    size_t m_chromenum;

    static double randomInclusive(const double max);
    static double randomExclusive(const double max);
    static bool areChromosonesEqual(std::vector<int>chromosoneA,
                                    std::vector<int> chromosoneB);
    double evaluateFitness(std::vector<int>* chromosone) const;
    std::vector<int> rouletteSelection(std::vector<double>* fitness) const;
    void repairOffspring(std::vector<int>* offspringToRepair, int missingIndex,
                         std::vector<int>* other);
    void mutate(std::vector<int>* chromosone);
    void crossover(std::vector<int>* parentA, std::vector<int>* parentB,
                   std::vector<int>* offspringA, std::vector<int>* offspringB);
    bool hasDuplicate(std::vector<int>* chromosone, size_t populationCount);
    void copyToNewPopulation(std::vector<int>* chromosone);
};

