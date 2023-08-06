"""
Benchmarks are here for you to test the performance of different search algorithms and to help you to reproduce our results. They can also be used to test your installation of deephyper or to discover the many parameters of a search. In deephyper we have two different kinds of benchmark. The first type is `hyper parameters search` benchmark and the second type is  `neural architecture search` benchmark. To see a full explanation about the different kind of search please refer to the following pages: :ref:`available-hps-benchmarks` & :ref:`available-nas-benchmarks`.
"""

from deephyper.benchmark.problem import Problem, HpProblem, NaProblem

__all__ = ['Problem', 'HpProblem', 'NaProblem']
