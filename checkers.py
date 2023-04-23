import argparse
import copy
import sys
import time
from copy import deepcopy

cache = {}  # you can use this to implement state caching!
terminal_checker = {}  # key is the evaluation value and value is the state
Board = [
    ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
    ['b', '.', 'b', '.', 'b', '.', 'b', '.'],
    ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['r', '.', 'r', '.', 'r', '.', 'r', '.'],
    ['.', 'r', '.', 'r', '.', 'r', '.', 'r'],
    ['r', '.', 'r', '.', 'r', '.', 'r', '.']
]
score_board = [[2.2, 2.1, 2.1, 0.5, 0.5, 2.1, 2.1, 2.2],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
      [2.2, 2, 2, 1, 1, 2, 2, 2.2]]
score_board1 = [[2.2, 2.1, 2.1, 0.5, 0.5, 2.1, 2.1, 2.2],
      [0, 1, 1, 0, 0, 0, 1, 0],
      [0, 1, 1, 2.5, 2.5, 1, 1, 0],
      [0, 1, 1, 3, 3, 3, 1, 0],
      [0, 1, 1, 3, 3, 3, 1, 0],
      [0, 1, 1, 2.5, 2.5, 2.5, 1, 0],
      [0, 1, 1, 0, 0, 0, 1, 0],
      [2.2, 2, 2, 1, 1, 2, 2, 2.2]]
player = ['r', 'R']
computer = ['b', 'B']
walkthrough = []


class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board, cur_turn, parent=None):
        """
            store state's board information and who is making next turn
            :param board: board information
            :type board: List[List]
            :param cur_turn: the current player
            :type cur_turn: List[str]
        """
        self.board = board
        self.width = 8
        self.height = 8
        self.cur_turn = cur_turn
        self.parent = parent

    def generate_successor(self):
        """
            Generate a list of states that extends from current state based
            on current player
            :return: The list of successor states.
            :rtype: List[State]
        """
        states = []
        pieces = self.get_pieces()
        # check if piece should move upwards or downwards
        for piece in pieces:
            jump_list = self.jump_recurse(piece)
            if jump_list:
                states.extend(jump_list)
            else:
                slide_list = self.slide(piece)
                states.extend(slide_list)
        return states

    def get_pieces(self):
        """
            get all location of pieces coordinate information to a tuple
            and store it to a list. Tuple format like (x, y) where x is x-axis
            and y is y-axis
            :rtype: List[Tuple]
        """
        pieces = []
        for row in range(self.width):
            for column in range(self.height):
                if self.board[row][column] in self.cur_turn:
                    pieces.append((column, row))
        return pieces

    def slide(self, piece):
        """
            Returns a list of states after a piece makes a jump in any possible
            direction based on current payer
            :param piece: The x-coordinate and y-coordinate
            of the piece's current position.
            :type piece: Tuple(int, int)
            :return: a list of State objects representing the board after the jump.
            :rtype: List[State]
        """
        states = []
        x = piece[0]
        y = piece[1]
        if self.cur_turn == player:
            if self.board[y][x] == 'r':
                movement = [(1, -1), (-1, -1)]
            else:
                movement = [(1, -1), (-1, -1), (1, 1), (-1, 1)]
        else:
            if self.board[y][x] == 'b':
                movement = [(1, 1), (-1, 1)]
            else:
                movement = [(1, -1), (-1, -1), (1, 1), (-1, 1)]
        for x_dir, y_dir in movement:
            new_board = deepcopy(self.board)
            x_update = x + x_dir
            y_update = y + y_dir
            if x_update >= self.width or x_update < 0 or y_update < 0 or \
                    y_update >= self.height:
                continue
            if new_board[y_update][x_update] == '.':
                new_board[y_update][x_update] = new_board[y][x]
                new_board[y][x] = '.'
                states.append(
                    State(queen_checker(new_board), get_opp_char(self.cur_turn), self))
        return states

    def jump_helper(self, piece):
        """
            Returns a list of states after a piece makes a jump in any possible
            direction based on current payer
            :param piece: The x-coordinate and y-coordinate
            of the piece's current position.
            :type piece: Tuple(int, int)
            :return: a list of State objects representing the board after the jump.
            :rtype: List[State]
        """
        all_jumps = []
        if self.cur_turn == player:
            if self.board[piece[1]][piece[0]] == 'r':
                movement = [(2, -2), (-2, -2)]
            else:
                movement = [(2, -2), (-2, -2), (2, 2), (-2, 2)]
        else:
            if self.board[piece[1]][piece[0]] == 'b':
                movement = [(2, 2), (-2, 2)]
            else:
                movement = [(2, -2), (-2, -2), (2, 2), (-2, 2)]
        for x_dir, y_dir in movement:
            jumps = self.jump(piece[0], piece[1], x_dir, y_dir)
            if jumps is not None:
                all_jumps.append(jumps)
        return all_jumps

    def jump(self, i, j, x_dir, y_dir):
        """
        Returns a state after a piece makes a jump in a given direction.

        :param i: The x-coordinate of the piece's current position.
        :type i: int
        :param j: The y-coordinate of the piece's current position.
        :type j: int
        :param x_dir: The x-direction of the jump.
        :type x_dir: int
        :param y_dir: The y-direction of the jump.
        :type y_dir: int
        :return: board objects representing the board after the jump.
        :rtype: State
        """
        x_mid, y_mid = i + x_dir // 2, j + y_dir // 2
        x_next, y_next = i + x_dir, j + y_dir
        if x_next < 0 or x_next >= self.width or y_next < 0 or y_next >= self.height:
            return None
        if self.board[y_mid][x_mid] in get_opp_char(self.cur_turn) and \
                self.board[y_next][x_next] == '.':
            new_board = deepcopy(self.board)
            new_board[y_next][x_next] = new_board[j][i]
            new_board[j][i] = '.'
            new_board[y_mid][x_mid] = '.'
            new_state = State(new_board, self.cur_turn, self)
            cache[str(new_state.board)] = (x_next, y_next)
            return new_state
        else:
            return None

    def jump_recurse(self, piece):
        """
            Returns list of states after piece makes jump.
            :param piece: The x-coordinate and y-coordinate of the
            piece's current position.
            :type piece: tuple(int, int)
            :return: state objects representing the board after the jump.
            :rtype: List[State]
        """
        list_state = []
        all_jumps = self.jump_helper(piece)
        while all_jumps:
            next_state = all_jumps.pop(0)
            arr = next_state.jump_helper(cache[str(next_state.board)])
            if arr:
                for single_state in arr:
                    all_jumps.append(single_state)
            else:
                list_state.append(
                    State(queen_checker(next_state.board),
                          get_opp_char(self.cur_turn), next_state.parent))
        return list_state

    def eval(self):
        """
            Returns a int that represents board's value
            :rtype: int
        """
        score = 0
        # check checker's weight by comparing their number
        for row in self.board:
            score += 1 * (row.count('r') - row.count('b')) + 2.5 * (
                    row.count('R') - row.count('B'))
        for row in range(self.height):
            for column in range(self.width):
                if self.board[row][column] in ['r', 'R']:
                    # check the weight by comparing their position for row and
                    # column
                    if self.board[row][column] == 'r':
                        # check r's security
                        if not is_safe_r(self.board, row, column):
                            score -= 2
                        elif is_enhance_r(self.board, row, column):
                            score += 8
                        if row != 0:
                            score += (self.height - row) * 0.5 + \
                                     (7 - abs(column - 3) * 1)
                        # if checker has chance to become king, then become it.
                        else:
                            score += 2.5
                    else:
                        # check R's security
                        if not is_safe_r(self.board, row, column):
                            score -= 5
                        score += 1.5 * (7 - abs(column - 3) * 0.5) + \
                                 (self.height - row) * 0.5
                        # R's position, a little bit hard coding
                        score += score_board1[row][column]
                if self.board[row][column] in ['b', 'B']:
                    if self.board[row][column] == 'b':
                        # check b's security
                        if not is_safe_b(self.board, row, column):
                            score += 2
                        elif is_enhance_b(self.board, row, column):
                            score -= 5.5
                        if row != 7:
                            score -= (self.height - row) * 0.5 + \
                                     (7 - abs(column - 3) * 0.5)
                        # if checker has chance to become king, then become it.
                        else:
                            # check B's security
                            score += 2.5
                    else:
                        if not is_safe_b(self.board, row, column):
                            score -= 5
                        score -= 1.5 * (7 - abs(column - 3) * 0.5) + \
                                 (self.height - row) * 0.5
        return score

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")


def is_safe_r(board, row, col):
    """
        Returns if red state is secure
        :param board: The board of state
        :type board: List[List[str]]
        :param row: The row of current piece
        :type row: int
        :param col: The col of current piece
        :type col: int
        :return: indicating if rea piece is safe or under threaten
        :rtype: Boolean
    """
    if col == 0 or col == 7 or row == 0 or row == 7:
        return True
    # i think we should put more weight on central piece.
    threaten_upper_left = not (board[row - 1][col - 1] in ['b', 'B']
                               and board[row + 1][col + 1] == '.')
    threaten_upper_right = not (board[row - 1][col + 1] in ['b', 'B']
                                and board[row + 1][col - 1] == '.')
    threaten_down_right = not (board[row + 1][col + 1] == 'B'
                               and board[row - 1][col - 1] == '.')
    threaten_down_left = not (board[row + 1][col - 1] == 'B'
                              and board[row - 1][col + 1] == '.')
    return threaten_down_right or threaten_down_left \
           or threaten_upper_left or threaten_upper_right


def is_enhance_r(board, row, col):
    """
        Returns if red state is enhaced(backed up by two piece)
        :param board: The board of state
        :type board: List[List[str]]
        :param row: The row of current piece
        :type row: int
        :param col: The col of current piece
        :type col: int
        :return: indicating if rea piece is safe or under threaten
        :rtype: Boolean
    """
    if row == 0 or row == 7 or col == 0 or col == 7:
        return False
    # i think we should put more weight on central piece.
    enhanced_down_left = board[row + 1][col - 1] in ['r', 'R']
    enhanced_down_right = board[row + 1][col + 1] in ['r', 'R']
    return enhanced_down_right and enhanced_down_left


def is_enhance_b(board, row, col):
    """
        Returns if black state is enhanced(backed up by two piece)
        :param board: The board of state
        :type board: List[List[str]]
        :param row: The row of current piece
        :type row: int
        :param col: The col of current piece
        :type col: int
        :return: indicating if rea piece is safe or under threaten
        :rtype: Boolean
    """
    if row == 0 or row == 7 or col == 0 or col == 7:
        return False
    # i think we should put more weight on central piece.
    enhanced_up_left = board[row - 1][col - 1] in ['b', 'B']
    enhanced_up_right = board[row - 1][col + 1] in ['b', 'B']
    return enhanced_up_left and enhanced_up_right


def is_safe_b(board, row, col):
    """
        Returns if red state is secure
        :param board: The board of state
        :type board: List[List[str]]
        :param row: The row of current piece
        :type row: int
        :param col: The col of current piece
        :type col: int
        :return: indicating if rea piece is safe or under threaten
        :rtype: Boolean
    """
    if col == 0 or col == 7 or row == 0 or row == 7:
        return True
    # i think we should put more weight on central piece.
    threaten_upper_left = not (board[row - 1][col - 1] == 'R'
                               and board[row + 1][col + 1] == '.')
    threaten_upper_right = not (board[row - 1][col + 1] == 'R'
                                and board[row + 1][col - 1] == '.')
    threaten_down_right = not (board[row + 1][col + 1] in ['r', 'R']
                               and board[row - 1][col - 1] == '.')
    threaten_down_left = not (board[row + 1][col - 1] in ['r', 'R']
                              and board[row - 1][col + 1] == '.')
    return threaten_down_right or threaten_down_left \
           or threaten_upper_left or threaten_upper_right


def cutoff_test(s, depth):
    """
        Returns list of states after piece makes jump.
        :param depth: The depth of state
        :type depth: int
        :param s: The State of board.
        :type s: State
        :return: a boolean that indicates if state is terminal state
        :rtype: Boolean
    """
    if depth == 0:
        return True
    player_eliminate = True
    rival_eliminate = True
    for row in s.board:
        if player_eliminate == False and rival_eliminate == False:
            break
        for column in row:
            if column in player:
                player_eliminate = False
            if column in computer:
                rival_eliminate = False
    return player_eliminate or rival_eliminate


def get_solution(final_state):
    """
            :param final_state: final state
            :type final_state: State
            :rtype: List[State]
    """
    # tracing through from goal state to initial state
    walk_through = []
    while final_state is not None:
        walk_through.append(final_state)
        final_state = final_state.parent
    return walk_through[::-1]


def max_value(s, alpha, beta, depth):
    chosen_move = None
    if cutoff_test(s, depth):
        return chosen_move, s.eval()
    v = float('-inf')
    all_successor = s.generate_successor()
    for successor in all_successor:
        no_use_object, successor_v = min_value(successor, alpha, beta, depth - 1)
        if v < successor_v:
            v = successor_v
            chosen_move = successor
        if v >= beta:
            return chosen_move, v
        alpha = max(alpha, v)
    return chosen_move, v


def min_value(s, alpha, beta, depth):
    chosen_move = None
    if cutoff_test(s, depth):
        return chosen_move, s.eval()
    v = float('inf')
    all_successor = s.generate_successor()
    for successor in all_successor:
        no_use_object, successor_v = max_value(successor, alpha, beta, depth - 1)
        if v > successor_v:
            v = successor_v
            chosen_move = successor
        if v <= alpha:
            return chosen_move, v
        beta = min(beta, v)
    return chosen_move, v


def alpha_beta_search(s):
    cur_state = s
    walkthrough.append(cur_state)
    next_state, v = max_value(s, float("-inf"), float("inf"), 1)
    flip = 0
    walkthrough.append(next_state)
    while next_state is not None:
        if flip == 0:
            cur_state = next_state
            next_state, v = min_value(next_state, float("-inf"), float("inf"), 1)
            flip = 1
        else:
            cur_state = next_state
            next_state, v = max_value(next_state, float("-inf"), float("inf"), 1)
            flip = 0
        if next_state is not None:
            walkthrough.append(next_state)
    return cur_state, v


def get_opp_char(cur):
    if cur == ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']


def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'


def queen_checker(board):
    for z in range(len(board[0])):
        if board[0][z] == 'r':
            board[0][z] = 'R'
    for m in range(len(board[7])):
        if board[7][m] == 'b':
            board[7][m] = 'B'
    return board


def read_from_file(filename):

    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board


if __name__ == '__main__':
    # board_final2 = [
    #     ['.', '.', '.', '.', 'a'],
    #     ['.', 'b', '.', '.', '.'],
    #     ['.', '.', '.', '.', '.'],
    #     ['.', '.', '.', '.', '.'],
    #     ['.', '.', '.', '.', '.'],
    # ]
    # board_final1 = [
    #     ['a', '.', '.', '.', '.'],
    #     ['.', '.', '.', 'b', '.'],
    #     ['.', '.', '.', '.', '.'],
    #     ['.', '.', '.', '.', '.'],
    #     ['.', '.', '.', '.', '.'],
    # ]
    # board_intermediate = [
    #     ['.', '.', '.', '.', '.'],
    #     ['.', 'b', '.', 'b', '.'],
    #     ['.', '.', 'a', '.', '.'],
    #     ['.', '.', '.', '.', '.'],
    #     ['.', '.', '.', '.', '.'],
    # ]
    # board_1 = [
    #     ['.', '.', '.', '.', '.'],
    #     ['.', 'b', '.', 'b', '.'],
    #     ['.', '.', '.', '.', '.'],
    #     ['.', 'b', '.', '.', '.'],
    #     ['r', '.', '.', '.', '.'],
    # ]
    # t1 = [
    #     ['.', '.', '.', '.', '.', '.', '.', '.'],
    #     ['.', '.', '.', '.', 'b', '.', '.', '.'],
    #     ['.', '.', '.', '.', '.', '.', '.', 'R'],
    #     ['.', '.', 'b', '.', 'b', '.', '.', '.'],
    #     ['.', '.', '.', 'b', '.', '.', '.', 'r'],
    #     ['.', '.', '.', '.', '.', '.', '.', '.'],
    #     ['.', '.', '.', 'r', '.', '.', '.', '.'],
    #     ['.', '.', '.', '.', 'B', '.', '.', '.']
    # ]
    #
    # t2 = [
    #     ['.', '.', '.', '.', '.', '.', '.', '.'],
    #     ['.', '.', '.', '.', 'b', '.', '.', '.'],
    #     ['.', '.', '.', '.', '.', '.', '.', 'R'],
    #     ['.', '.', 'b', '.', 'b', '.', 'r', '.'],
    #     ['.', '.', '.', 'b', '.', '.', '.', '.'],
    #     ['.', '.', '.', '.', '.', '.', '.', '.'],
    #     ['.', '.', '.', 'r', '.', '.', '.', '.'],
    #     ['.', '.', '.', '.', 'B', '.', '.', '.']
    # ]
    #
    # t3 = [
    #     ['.', '.', '.', '.', '.', '.', '.', '.'],
    #     ['.', '.', '.', '.', 'b', '.', '.', '.'],
    #     ['.', '.', '.', '.', '.', '.', '.', 'R'],
    #     ['.', '.', 'b', '.', 'b', '.', 'r', '.'],
    #     ['.', '.', '.', 'b', '.', '.', '.', '.'],
    #     ['.', '.', 'B', '.', '.', '.', '.', '.'],
    #     ['.', '.', '.', '.', '.', '.', '.', '.'],
    #     ['.', '.', '.', '.', '.', '.', '.', '.'],
    # ]
    #
    # t4 = [['.', '.', '.', '.', '.', '.', '.', '.'],
    #       ['.', '.', '.', '.', 'b', '.', '.', '.'],
    #       ['.', '.', '.', '.', '.', 'r', '.', 'R'],
    #       ['.', '.', 'b', '.', 'b', '.', '.', '.'],
    #       ['.', '.', '.', 'b', '.', '.', '.', '.'],
    #       ['.', '.', 'B', '.', '.', '.', '.', '.'],
    #       ['.', '.', '.', '.', '.', '.', '.', '.'],
    #       ['.', '.', '.', '.', '.', '.', '.', '.']]
    #
    # t5 = [['.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', 'R'],
    #         ['.', '.', 'b', '.', 'b', '.', 'b', '.'],
    #         ['.', '.', '.', 'b', '.', '.', '.', '.'],
    #         ['.', '.', 'B', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', '.'],
    #         ['.', '.', '.', '.', '.', '.', '.', '.']]
    # tt3 = [['.', '.', '.', '.', '.', '.', '.', 'b'],
    #          ['.', '.', '.', '.', 'r', '.', 'b', '.'],
    #          ['.', '.', '.', '.', '.', 'r', '.', '.'],
    #          ['.', '.', 'B', '.', 'r', '.', 'b', '.'],
    #          ['.', '.', '.', '.', '.', '.', '.', '.'],
    #          ['.', '.', '.', '.', '.', '.', '.', '.'],
    #          ['.', '.', '.', '.', '.', '.', '.', '.'],
    #          ['.', '.', '.', '.', '.', '.', '.', '.']]
    # t7 = [['.', 'B', '.', 'B', '.', '.', '.', '.'],
    #          ['.', '.', '.', '.', '.', '.', '.', '.'],
    #          ['.', '.', '.', 'B', '.', '.', '.', '.'],
    #          ['.', '.', '.', '.', '.', '.', '.', '.'],
    #          ['.', '.', '.', 'R', '.', '.', '.', '.'],
    #          ['.', '.', '.', '.', '.', '.', '.', '.'],
    #          ['.', '.', '.', '.', '.', '.', '.', '.'],
    #          ['.', '.', 'R', '.', 'R', '.', '.', '.']]
    # player = ['r', 'R']
    # state = State(t7, computer)
    # # state.jump(2, 3, 2, 2)
    # # for i in state.board:
    # #     print(i)
    # states = state.generate_successor()
    # for state in states:
    #     for q in state.board:
    #         print(q)
    #     print(state.eval())
    #     print("-------------")
    # state, value = alpha_beta_search(state)
    # for i in get_solution(state):
    #     for j in i.board:
    #         print(j)
    #     print('---------')
    #
    #
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    initial_board = read_from_file(args.inputfile)
    state = State(initial_board, player)
    turn = 'r'
    ctr = 0

    sys.stdout = open(args.outputfile, 'w')

    sys.stdout = sys.__stdout__

    # write output into txt file.
    final_state, score = alpha_beta_search(state)
    # print board of each state in walkthrough list
    with open(args.outputfile, 'w') as f:
        for i, state in enumerate(walkthrough):
            for row in state.board:
                f.write(''.join(row) + '\n')
            f.write('\n')


