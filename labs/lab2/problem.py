from state import State


CONFIG = {
    'min': 4,
    'max': 16,
    'default': 8
}


class Problem:
    def __init__(self, n=8):
        self.__n = n
        self.__state = State(n)
        self.__initial_state = self.__state.clone()
        self.__final_state = None

    def is_in_final_state(self, state):
        # is in final state if the number of queens is n
        return state.get_density() == self.__n

    def get_initial_state(self):
        return self.__initial_state.clone()

    # def is_correct_so_far(self, state):
    #     # is correct if it follows the constraints
    #     matrix, n = state.get()
    #     if n != self.__n:
    #         return False
    #     # sum of each row and column is 1 aka only one queen on row and col
    #     for i in range(n):
    #         sum_row = 0
    #         sum_col = 0
    #         for j in range(n):
    #             sum_row += matrix[i][j]
    #             sum_col += matrix[j][i]
    #         if sum_col > 1 or sum_row > 1:
    #             return False
    #     # no queens attacking each other on diagonals
    #     occ = state.get_list_occupied()
    #     for i in range(len(occ)):
    #         for j in range(i + 1, len(occ)):
    #             # | i1 - i2 | + | j1 - j2 | = 0
    #             i1 = occ[i][0]
    #             i2 = occ[j][0]
    #             j1 = occ[i][1]
    #             j2 = occ[j][1]
    #             attack = abs(i1 - i2) - abs(j1 - j2)
    #             if attack == 0:
    #                 return False
    #     return True

    def is_correct(self, state, sure=True):
        # is correct if it follows the constraints
        matrix, n = state.get()
        if n != self.__n:
            return False
        # sum of each row and column is 1 aka only one queen on row and col
        for i in range(n):
            sum_row = 0
            sum_col = 0
            for j in range(n):
                sum_row += matrix[i][j]
                sum_col += matrix[j][i]
            if sure:
                # check if the state IS a solution
                if sum_col != 1 or sum_row != 1:
                    return False
            else:
                # check if CAN BE a solution in the future
                if sum_col > 1 or sum_row > 1:
                    return False
        # no queens attacking each other on diagonals
        occ = state.get_list_occupied()
        for i in range(len(occ)):
            for j in range(i + 1, len(occ)):
                # | i1 - i2 | + | j1 - j2 | = 0
                i1 = occ[i][0]
                i2 = occ[j][0]
                j1 = occ[i][1]
                j2 = occ[j][1]
                attack = abs(i1 - i2) - abs(j1 - j2)
                if attack == 0:
                    return False
        return True

    # get the next list of state
    def expand(self, state):
        if self.is_in_final_state(state):
            return []
        generated_states = []
        matrix, n = state.get()
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 0:  # is not occupied by a queen
                    new_state = state.clone()
                    new_state.occupy(i, j)
                    generated_states.append(new_state)
        return generated_states
