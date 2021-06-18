"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import math
import random
from typing import List, Tuple
from block import Block
from settings import colour_name, COLOUR_LIST


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    # TODO: Implement Me
    # We make all goals Perimeter if goal_type == 0, and Blob if goal_type == 1
    goal_type = random.randint(0, 1)
    colour_list_copy = COLOUR_LIST[:]
    goal_list = []

    for _ in range(num_goals):
        random_colour = random.randint(0, len(colour_list_copy) - 1)
        if goal_type == 0:
            new_goal = PerimeterGoal(colour_list_copy[random_colour])
        else:
            new_goal = BlobGoal(colour_list_copy[random_colour])
        goal_list.append(new_goal)
        colour_list_copy.remove(new_goal.colour)
    return goal_list


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    # TODO: Implement me
    if block.level == block.max_depth:
        return [[block.colour]]
    if len(block.children) == 0:
        dimension = 2 ** (block.max_depth - block.level)
        matrix = []
        for i in range(dimension):
            col = []
            for j in range(dimension):
                col.append(block.colour)
            matrix.append(col)
        return matrix
    else:
        matrix = []
        child_0 = _flatten(block.children[0])
        child_1 = _flatten(block.children[1])
        child_2 = _flatten(block.children[2])
        child_3 = _flatten(block.children[3])
        for i in range(len(child_0)):
            col = []
            for j in range(len(child_0)):
                col.append(child_1[i][j])
            for j in range(len(child_0)):
                col.append(child_2[i][j])
            matrix.append(col)
        for i in range(len(child_0)):
            col = []
            for j in range(len(child_0)):
                col.append(child_0[i][j])
            for j in range(len(child_0)):
                col.append(child_3[i][j])
            matrix.append(col)
        return matrix


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """ A goal for most perimeter filled. """
    def score(self, board: Block) -> int:
        # TODO: Implement me

        flattened_board = _flatten(board)
        count = 0
        top = flattened_board[0]
        bottom = flattened_board[len(flattened_board) - 1]
        left = []
        right = []
        for sublist in flattened_board:
            left.append(sublist[0])
            right.append(sublist[len(flattened_board) - 1])
        for colour in top:
            if colour == self.colour:
                count += 1
        for colour in bottom:
            if colour == self.colour:
                count += 1
        for colour in left:
            if colour == self.colour:
                count += 1
        for colour in right:
            if colour == self.colour:
                count += 1
        return count

    def description(self) -> str:
        " Return a string representing a description of perimeter goal. "
        # TODO: Implement me
        return f'Outline the greatest amount of the game board\'s perimeter' \
               f' with {colour_name(self.colour)}!'


class BlobGoal(Goal):
    """ A goal for biggest blob."""
    def score(self, board: Block) -> int:
        # TODO: Implement me
        flattened_board = _flatten(board)
        visited_map = []
        dummy_visited_map = []
        for i in range(len(flattened_board)):
            sublist = []
            for j in range(len(flattened_board)):
                sublist.append(-1)
            visited_map.append(sublist)
            dummy_visited_map.append(sublist[:])

        dummy_flattened_board = _flatten(board)

        maximum = 0
        for i in range(len(flattened_board)):
            for j in range(len(flattened_board)):
                if self._undiscovered_blob_size((i, j), dummy_flattened_board,
                                                dummy_visited_map) > maximum:
                    maximum = self._undiscovered_blob_size((i, j),
                                                           flattened_board,
                                                           visited_map)
        return maximum

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        # TODO: Implement me

        count = 0
        if board[pos[0]][pos[1]] == self.colour and visited[pos[0]][pos[1]] == -1:
            visited[pos[0]][pos[1]] = 1
            count += 1
        else:
            visited[pos[0]][pos[1]] = 0
            return 0

        if 0 <= pos[0] - 1 < len(board) and 0 <= pos[1] < len(
                board) and visited[pos[0] - 1][pos[1]] == -1:

            if board[pos[0] - 1][pos[1]] == self.colour:
                count = count + self._undiscovered_blob_size((pos[0] - 1,
                                                              pos[1]),
                                                             board, visited)
                visited[pos[0] - 1][pos[1]] = 1
            else:
                visited[pos[0] - 1][pos[1]] = 0

        if 0 <= pos[0] + 1 < len(board) and 0 <= pos[1] < len(
                board) and visited[pos[0] + 1][pos[1]] == -1:

            if board[pos[0] + 1][pos[1]] == self.colour:
                count = count + self._undiscovered_blob_size((pos[0] + 1,
                                                              pos[1]),
                                                             board, visited)
                visited[pos[0] + 1][pos[1]] = 1
            else:
                visited[pos[0] + 1][pos[1]] = 0

        if 0 <= pos[0] < len(board) and 0 <= pos[1] - 1 < len(
                board) and visited[pos[0]][pos[1] - 1] == -1:

            if board[pos[0]][pos[1] - 1] == self.colour:
                count = count + self._undiscovered_blob_size((pos[0],
                                                              pos[1] - 1),
                                                             board, visited)
                visited[pos[0]][pos[1] - 1] = 1
            else:
                visited[pos[0]][pos[1] - 1] = 0

        if 0 <= pos[0] < len(board) and 0 <= pos[1] + 1 < len(
                board) and visited[pos[0]][pos[1] + 1] == -1:

            if board[pos[0]][pos[1] + 1] == self.colour:
                count = count + self._undiscovered_blob_size((pos[0],
                                                              pos[1] + 1),
                                                             board, visited)
                visited[pos[0]][pos[1] + 1] = 1
            else:
                visited[pos[0]][pos[1] + 1] = 0

        return count

    def description(self) -> str:
        # TODO: Implement me
        return f'Create the largest collection or "blob" of adjacent' \
               f' {colour_name(self.colour)} squares!'


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
