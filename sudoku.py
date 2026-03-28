class Solution:
    def update_inf_dict(self, inf_dict, k, elem):
        i, j = k
        for pos in range(9):
            if (i, pos) in inf_dict  and pos!=j:
                inf_dict[(i, pos)][elem-1] = 1
            if (pos, j) in inf_dict and pos!=i:
                inf_dict[(pos, j)][elem - 1] = 1
        start_i = 3 * (i//3) 
        start_j = 3 * (j//3)
        for incr_i in range(3):
            for incr_j in range(3):
                if (start_i + incr_i, start_j + incr_j)  in inf_dict.keys() and (start_i + incr_i, start_j + incr_j)!=(i,j) :
                    inf_dict[(start_i + incr_i, start_j + incr_j)][elem - 1] = 1

    def create_inf_dict(self, board, inf_dict):
        for i in range(9):
            for j in range(9):
                if board[i][j] == ".":
                    # Let's now fill the infeasibility dict for (i, j) entry
                    # numbers present in the same row and column
                    inf_dict[(i, j)] = [0]*9
                    for k in range(9):
                        if board[i][k]!="." :
                            inf_dict[(i, j)][int(board[i][k])-1] = 1
                        if board[k][j]!=".":
                            inf_dict[(i, j)][int(int(board[k][j]))-1] = 1
                    # numbers in the same subsquare
                    start_i = 3 * (i//3) 
                    start_j = 3 * (j//3)
                    for incr_i in range(3):
                        for incr_j in range(3):
                            if board[start_i + incr_i][start_j + incr_j]!=".":
                                inf_dict[(i, j)][int(board[start_i + incr_i][start_j + incr_j])-1] = 1
    
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        inf_dict = {}   
        # create infeasibility dict
        self.create_inf_dict(board, inf_dict)
        # write a dfs to fill a feasible number, update infeasibility dict, and backtrack if Sudoku inf
        import copy 
        unfilled = list(inf_dict.keys())
        def _is_Possible(inf_dict, part_fillings, k):
            # check for infeasibility
            for cell in inf_dict:
                if cell not in part_fillings and sum(inf_dict[cell]) == 9:
                    return False
            flag_unfil = 1
            for i in range(1, 10):
                #print(k, i-1)
                if inf_dict[k][i-1]==0:
                    part_fillings[k] = i
                    pass_dict = copy.deepcopy(inf_dict)
                    #del pass_dict[k]
                    self.update_inf_dict(pass_dict, k, i)
                    remaining = [cell for cell in unfilled if cell not in part_fillings]
                    if remaining == []:
                        return True
                    k_next = min(remaining, key=lambda cell: sum(1 for x in inf_dict[cell] if x == 0))
                    if _is_Possible(pass_dict, part_fillings,  k_next):
                        return True
                    del part_fillings[k]
            return False

        fillings = {}
        _is_Possible(inf_dict, fillings, unfilled[0])
        for k in fillings:
            board[k[0]][k[1]] = str(fillings[k])
