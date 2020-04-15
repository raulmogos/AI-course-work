import time
import queue
import subprocess as sp

from random import choice

from problem import Problem


class Controller:
    def __init__(self, problem):
        self.__problem = problem

    def dfs(self):  # backtracking
        stack = [self.__problem.get_initial_state()]
        while stack:  # not empty
            actual = stack.pop()
            # if a solution is found
            if self.__problem.is_in_final_state(actual):
                # print(actual)
                if self.__problem.is_correct(actual):
                    return actual
            # continue with new generated states
            new_states = self.__problem.expand(actual)
            for state in new_states:
                # we put only the state that seem to have a good solution in the end
                if self.__problem.is_correct(state, sure=False):
                    # sp.call('cls', shell=True), print(state), time.sleep(0.05)
                    stack.append(state)
            del actual

    def heuristic(self, states):
        # get only the valid ones
        return [state for state in states if self.__problem.is_correct(state, sure=False)]

    def greedy_bfs(self):
        q = queue.Queue()
        q.put(self.__problem.get_initial_state())
        while not q.empty():
            actual = q.get()
            # if a solution is found
            if self.__problem.is_in_final_state(actual) and self.__problem.is_correct(actual):
                return actual
            # continue with new generated states
            new_states = self.__problem.expand(actual)
            # get only valid states
            heuristics = self.heuristic(new_states)
            # get a random one
            greedy_best_one = choice(heuristics) if heuristics else None
            greedy_best_one and q.put(greedy_best_one)
            del actual

    def greedy(self):
        # run the greedy_bfs() until it finds a correct solution
        sol = self.greedy_bfs()
        while not sol:
            sol = self.greedy_bfs()
        return sol
