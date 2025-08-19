import itertools
import random


class Evolution:
    def __init__(self, population_count, keep_count):
        self.population_count = population_count
        self.keep_count = keep_count

    def execute(self, rankable_chromosomes):
        # selection
        sorted_chromosomes =  [w.chromosome for w in sorted(rankable_chromosomes)]
        keep_chromosomes = sorted_chromosomes[:self.keep_count]

        # cross over
        reproduction_times = (self.population_count - self.keep_count) / self.keep_count
        offspring = [c for c in keep_chromosomes]

        for _ in range(int(reproduction_times)):
            for c1, c2 in itertools.batched(keep_chromosomes, 2):
                split_index = random.randint(0, len(c1) - 1)
                offspring.append(c1[:split_index] + c2[split_index:])
                offspring.append(c2[:split_index] + c1[split_index:])

        #mutation
        for chromosome in offspring[self.keep_count:]:
            for i in range(len(chromosome)):
                if random.randint(0, 4) == 1:
                    chromosome[i] = random.random() * 2 - 1

        return offspring