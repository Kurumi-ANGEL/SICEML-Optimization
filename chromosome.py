# chromosome.py

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple, Type, TypeVar

T = TypeVar('T', bound='Chromosome')  # 为返回自己


# 所有染色体的基类,必须重写所有方法
class Chromosome(ABC):
    @abstractmethod
    def fitness(self) -> float:
        '''适用度函数,以确定自己的适用度'''
        ...

    @classmethod
    @abstractmethod
    def random_instance(cls: Type[T]) -> T:
        '''类方法,创建一个携带随机选中基因的实例,用于填充第一代个体数据'''
        ...

    @abstractmethod
    def crossover(self: T, other: T) -> Tuple[T, T]:
        '''染色体交换,让本染色体与另一个同类结合并创建后代,即让自己与另一条染色体混合'''
        ...

    @abstractmethod
    def mutate(self) -> None:
        '''染色体变异,让自己体内数据发生相当随机的变化'''
        ...
