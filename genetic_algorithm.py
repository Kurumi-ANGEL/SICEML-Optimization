# genetic_algorithm.py

from __future__ import annotations
from typing import TypeVar, Generic, List, Tuple, Callable
from enum import Enum
from random import choices, random
from heapq import nlargest
from statistics import mean
from chromosome import Chromosome

C = TypeVar('C', bound=Chromosome) # 染色体类型


class GeneticAlgorithm(Generic[C]):
    SelectionType = Enum("SelectionType", "ROULETTE TOURNAMENT")

    def __init__(self, initial_population: List[C], threshold: float, max_generations: int = 100, mutation_chance: float = 0.01, crossover_chance: float = 0.7, selection_type: SelectionType = SelectionType.TOURNAMENT) -> None:
        self._population: List[C] = initial_population
        self._threshold: float = threshold
        self._max_generations: int = max_generations
        self._mutation_chance: float = mutation_chance
        self._crossover_chance: float = crossover_chance
        self._selection_type: GeneticAlgorithm.SelectionType = selection_type
        self._fitness_key: Callable = type(self._population[0]).fitness

    # 使用轮盘式选择2个父母
    # 注:轮盘式选择法不适用于负适应度问题
    def _pick_roulette(self, wheel: List[float]) -> Tuple[C, C]:
        return tuple(choices(self._population, weights=wheel, k=2))

    # 随机选择num_participants并选择最好的2个
    def _pick_tournament(self, num_participants: int) -> Tuple[C, C]:
        participants: List[C] = choices(self._population, k=num_participants)
        return tuple(nlargest(2, participants, key=self._fitness_key))

    # 用新一代个体取代种群
    def _reproduce_and_replace(self) -> None:
        new_population: List[C] = []
        # 继续努力，直到我们填满新一代
        while len(new_population) < len(self._population):
            # 选择2个父母
            if self._selection_type == GeneticAlgorithm.SelectionType.ROULETTE:
                parents: Tuple[C, C] = self._pick_roulette([x.fitness() for x in self._population])
            else:
                parents = self._pick_tournament(len(self._population) // 2)
            # 可能是双亲交叉
            if random() < self._crossover_chance:
                new_population.extend(parents[0].crossover(parents[1]))
            else:
                new_population.extend(parents)
        # 如果我们有一个奇数，我们会多出一个，所以我们去掉它
        if len(new_population) > len(self._population):
            new_population.pop()
        self._population = new_population # 替换引用

    # 概率变异每个个体
    def _mutate(self) -> None:
        for individual in self._population:
            if random() < self._mutation_chance:
                individual.mutate()

    # 运行max_generations迭代的遗传算法
    # 并返回找到的最佳个体
    def run(self) -> C:
        best: C = max(self._population, key=self._fitness_key)
        for generation in range(self._max_generations):
            # 如果达到阀值，就立刻退出
            if best.fitness() >= self._threshold:
                return best
            print(f"Generation {generation} Best {best.fitness()} Avg {mean(map(self._fitness_key, self._population))}")
            self._reproduce_and_replace()
            self._mutate()
            highest: C = max(self._population, key=self._fitness_key)
            if highest.fitness() > best.fitness():
                best = highest # 找到一个新的最好的
        return best # 最好的是_max_generations

