# genetic_algorithm.py

from __future__ import annotations

from heapq import nlargest
from random import choices, random
from statistics import mean
from typing import Callable, Generic, List, Tuple, TypeVar

from Chromosome import Chromosome

C = TypeVar('C', bound=Chromosome)  # 染色体类型


class GeneticAlgorithm(Generic[C]):

    def __init__(self,
                 initial_population: List[C],
                 threshold: float,
                 max_generations: int = 100,
                 mutation_chance: float = 0.01,
                 crossover_chance: float = 0.7,
                 selection_type: SelectionType = "TOURNAMENT"
                 ) -> None:
        '''
        initial_population:第一代染色体
        threshold:适应度阈值
        max_generations:最多运行代数
        mutation_chance:变异系数(每代每条染色体变异概率)
        crossover_chance:交换系数(双亲生出带有混合基因的染色体的概率)
        selection_type:双亲选择算法标识,目前支持:轮盘ROULETTE & 锦标赛TOURNAMENT

        注:若选择锦标赛双亲选择算法,可通过「self.num_participants」调节参加锦标赛的染色体数目,默认为染色体总数的一半
        '''
        self._population: List[C] = initial_population
        self._threshold: float = threshold
        self._max_generations: int = max_generations
        self._mutation_chance: float = mutation_chance
        self._crossover_chance: float = crossover_chance
        self._selection_type: str = selection_type
        self._fitness_key: Callable = type(self._population[0]).fitness

        self.num_participants: int = len(self._population) // 2

    def _pick_roulette(self, wheel: List[float]) -> Tuple[C, C]:
        '''
        使用轮盘式选择2个父母
        以适应度为权重,在全体染色体中随机选择2个染色体作为父母

        注:轮盘式选择法不适用于负适应度问题
        '''

        return tuple(choices(self._population, weights=wheel, k=2))

    def _pick_tournament(self, num_participants: int) -> Tuple[C, C]:
        '''
        使用锦标赛式选择2个父母
        随机选择num_participants并选择最好的2个
        '''

        participants: List[C] = choices(self._population, k=num_participants)
        return tuple(nlargest(2, participants, key=self._fitness_key))

    def _reproduce_and_replace(self) -> None:
        '''
        生成下一代染色体并填充进self._population
        '''

        new_population: List[C] = []

        while len(new_population) < len(self._population):
            # 选择2个父母
            if self._selection_type == "ROULETTE":
                parents: Tuple[C, C] = self._pick_roulette(
                    [x.fitness() for x in self._population])
            elif self._selection_type == "TOURNAMENT":
                parents = self._pick_tournament(self.num_participants)
            else:
                raise Exception("[ERROR]Incorrect Parent Selection Algorithm Identity Is Passed In")
            if random() < self._crossover_chance:
                # 双亲交换
                new_population.extend(parents[0].crossover(parents[1]))
            else:
                # 双亲直接进入下一代
                new_population.extend(parents)

        # 若染色体数为奇数,如果在某些条件下生成时多出一条染色体,那么就去掉它
        if len(new_population) > len(self._population):
            new_population.pop()

        self._population = new_population  # 替换引用

    # 概率变异每个个体
    def _mutate(self) -> None:
        for individual in self._population:
            if random() < self._mutation_chance:
                individual.mutate()

    def run(self) -> C:
        '''
        运行遗传算法并返回最优染色体
        '''

        best: C = max(self._population, key=self._fitness_key)
        for generation in range(self._max_generations):
            # 如果达到阈值，就立刻退出
            if best.fitness() >= self._threshold:
                return best
            print(
                f"Generation {generation} Best {best.fitness()} Avg {mean(map(self._fitness_key, self._population))}")
            self._reproduce_and_replace()
            self._mutate()
            highest: C = max(self._population, key=self._fitness_key)
            if highest.fitness() > best.fitness():
                best = highest  # 找到一个新的最优染色体
        return best
