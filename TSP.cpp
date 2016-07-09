#include "TSP.h"
#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <iostream>
#include <cassert>
#include <algorithm>
#include <sstream>
#include <fstream>
#include <vector>
#include <iterator>

TSP::TSP(std::string inputfile, std::string datafile,
         double crossoverProbability, double mutationProbability) :
  crossoverProbability(crossoverProbability),
  mutationProbability(mutationProbability) {
  srand((unsigned int)time(NULL));
  std::ifstream ifs(inputfile);
  std::string x, y;
  int index = 0;
  getline(ifs, x);
  while (1) {
    getline(ifs, x, ',');
    getline(ifs, y);
    if (!ifs)
      break;
    m_cities.push_back({stof(x), stof(y)});
    index++;
  }
  setFirstPopulation(datafile);
  m_chromenum = solutions.size();
  }

void TSP::setFirstPopulation(std::string filename)
{
  std::ifstream ifs(filename);
  std::string x;
  getline(ifs, x);
  while(1) {
    auto* chromosone = new std::vector<int>;
    while (1) {
      getline(ifs, x);
      if (!ifs || !(std::all_of(x.cbegin(), x.cend(), isdigit)))
        break;
      chromosone->push_back(stof(x));
    }
    solutions.push_back(chromosone);
    if (!ifs)
      break;
  }
}


double TSP::getBestFitness() const
{
  return evaluateFitness(bestChromosone);
}

double TSP::getAverageDistance() const
{
  double distance = 0;
  for(size_t i = 0; i < m_chromenum; i++)
    distance += totalDistance(solutions[i]);
  return distance / m_chromenum;
}

std::vector<int> TSP::getBestPath() const
{
  return *bestChromosone;
}

double TSP::getLowestTotalDistance() const
{
  return totalDistance(bestChromosone);
}

void TSP::nextPopulation()
{
  std::vector<double> fitness(m_chromenum);
  for(size_t i = 0; i < m_chromenum; i++)
  {
    fitness[i] = evaluateFitness(solutions[i]);
  }
  size_t eliteIndex1 = 0, eliteIndex2 = 0;
  eliteIndex1 =
    std::max_element(fitness.begin(), fitness.end()) - fitness.begin();
  this->bestChromosone = solutions[eliteIndex1];

  double highestFitness = 0;
  for(size_t i = 0; i < m_chromenum; i++)
  {
    if(i != eliteIndex1 && fitness[i] > highestFitness)
    {
      highestFitness = fitness[i];
      eliteIndex2 = i;
    }
  }

  size_t offspringCount = 0;
  copyToNewPopulation(solutions[eliteIndex1]);
  ++offspringCount;
  copyToNewPopulation(solutions[eliteIndex2]);
  ++offspringCount;
  while(true)
  {    
    std::vector<int> parentA;
    std::vector<int> parentB;
    parentA = rouletteSelection(&fitness);
    parentB = rouletteSelection(&fitness);
    while (parentB == parentA)
    {
      parentB = rouletteSelection(&fitness);
    }
    std::vector<int>* offspringA = new std::vector<int>(m_cities.size());
    std::vector<int>* offspringB = new std::vector<int>(m_cities.size());
    crossover(&parentA, &parentB, offspringA, offspringB);
    mutate(offspringA);
    mutate(offspringB);

    if(!hasDuplicate(offspringA, offspringCount)) {
      copyToNewPopulation(offspringA);
      ++offspringCount;
    }
    if(offspringCount == m_chromenum)
      break;
    if(!hasDuplicate(offspringB, offspringCount)) {
      copyToNewPopulation(offspringB);
      ++offspringCount;
    }
    if(offspringCount == m_chromenum)
      break;
  }
  for(size_t i = 0; i < m_chromenum; i++) 
    solutions[i] = newPopulation[i];
}

bool TSP::hasDuplicate(std::vector<int>* chromosone, size_t populationCount)
{
  for(size_t i = 0; i < populationCount; i++) {    
    if(*chromosone != *newPopulation[i])
      return false;
    else
      return true;
  }
  return false;
}

void TSP::mutate(std::vector<int>* chromosone)
{
  {
    double random = randomInclusive(1);
    if(random > mutationProbability)
    {
      return;
    }
  }

  int tmp;
  int random1 = (int)randomExclusive(m_cities.size());
  int random2 = (int)randomExclusive(m_cities.size());
  while(random1 == random2)
  {
    random2 = (int)randomExclusive(m_cities.size());
  }

  tmp = chromosone->at(random1);
  chromosone->at(random1) = chromosone->at(random2);
  chromosone->at(random2) = tmp;

}

void TSP::crossover(std::vector<int>* parentA, std::vector<int>* parentB,
                    std::vector<int>* offspringA, std::vector<int>* offspringB)
{
  {
    double random = randomInclusive(1);
    if(random > crossoverProbability)
    {
      *offspringA = *parentA;
      *offspringB = *parentB;
      return;
    }
  }

  int cutOffIndex1 = (int)randomInclusive(m_cities.size());
  int cutOffIndex2 = (int)randomInclusive(m_cities.size());
  while(cutOffIndex2 == cutOffIndex1)
  {
    cutOffIndex2 = (int)randomExclusive(m_cities.size());
  }

  unsigned int start;
  unsigned int end;
  if(cutOffIndex1 < cutOffIndex2)
  {
    start = cutOffIndex1;
    end = cutOffIndex2;
  }
  else
  {
    start = cutOffIndex2;
    end = cutOffIndex1;
  }
  *offspringA = *parentA;
  *offspringB = *parentB;

  std::copy(parentB->begin() + start, parentB->begin() + end,
            offspringA->begin() + start);
  std::copy(parentA->begin() + start, parentA->begin() + end,
            offspringB->begin() + start);

  for(size_t i = 0; i < m_cities.size(); i++)
  {
    if((i >= start && i < end)) {
    }
    else
    {
      for(size_t j = start; j < end; j++) {
        if(offspringA->at(i) == offspringA->at(j))
          offspringA->at(i) = -1;
        if(offspringB->at(i) == offspringB->at(j))
          offspringB->at(i) = -1;
      }
    }

  }
  for(size_t j = 0; j < m_cities.size(); j++)
  {
    if(offspringA->at(j) == -1)
      repairOffspring(offspringA, j, offspringB);
    if(offspringB->at(j) == -1)
      repairOffspring(offspringB, j, offspringA);
  }
}

void TSP::repairOffspring(std::vector<int>* offspringToRepair, int missingIndex,
                          std::vector<int>* other)
{
  for(size_t i = 0; i < m_cities.size(); i++)
  {
    auto missing = find(offspringToRepair->begin(),
                        offspringToRepair->begin() + m_cities.size(),
                        other->at(i));
    if(missing == (offspringToRepair->begin() + m_cities.size()))
    {
      offspringToRepair->at(missingIndex) = other->at(i);
      break;
    }
  }
}

void TSP::copyToNewPopulation(std::vector<int>* chromosone)
{
  assert("Index out of bounds");
  newPopulation.push_back(chromosone);
}

std::vector<int> TSP::rouletteSelection(std::vector<double>* fitness) const {
  double sum = 0;
  for(size_t i = 0; i < m_chromenum; i++)
  {
    sum += fitness->at(i);
  }
  double random = randomInclusive(sum);
  sum = 0;
  for(size_t i = 0; i < m_chromenum; i++)
  {
    sum += fitness->at(i);
    if(sum >= random)
    {
      return *solutions[i];
    }
  }
  assert(false && "A chromosone should have been picked by now");
  return std::vector<int>{};
}

double TSP::evaluateFitness(std::vector<int>* chromosone) const
{
  return 1/totalDistance(chromosone);
}

double TSP::totalDistance(std::vector<int>* chromosone) const
{
  double distance = 0;
  size_t i;
  for(i = 0; i < m_cities.size() - 1; i++)
  {
    Position p1 = m_cities[chromosone->at(i)];
    Position p2 = m_cities[chromosone->at(i+1)];
    double dx = p1.x - p2.x;
    double dy = p1.y - p2.y;

    distance += sqrt((pow(dx, 2.0) + pow(dy, 2.0)));
  }
  Position p1 = m_cities[chromosone->at(i)];
  Position p2 = m_cities[chromosone->at(0)];
  double dx = p1.x - p2.x;
  double dy = p1.y - p2.y; 
  distance += sqrt((pow(dx, 2.0) + pow(dy, 2.0)));

  return distance;
}

double TSP::randomExclusive(double max)
{
  return ((double)rand() * max) / ((double)RAND_MAX + 1);
}

double TSP::randomInclusive(double max)
{
  return ((double)rand() * max) / (double)RAND_MAX;
}

