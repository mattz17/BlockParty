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
Misha Schwartz, and Jaisie Sin.

=== Module Description ===

This file contains the hierarchy of player classes.
"""
from __future__ import annotations
from typing import List, Optional, Tuple
import random
import pygame

from block import Block
from goalsepehr import Goal, generate_goals

from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE


def create_players(num_human: int, num_random: int, smart_players: List[int]) \
        -> List[Player]:
    """Return a new list of Player objects.

    <num_human> is the number of human player, <num_random> is the number of
    random players, and <smart_players> is a list of difficulty levels for each
    SmartPlayer that is to be created.

    The list should contain <num_human> HumanPlayer objects first, then
    <num_random> RandomPlayer objects, then the same number of SmartPlayer
    objects as the length of <smart_players>. The difficulty levels in
    <smart_players> should be applied to each SmartPlayer object, in order.
    """
    # TODO: Implement Me
    goals = generate_goals(num_human + num_random + len(smart_players))
    player_list = []
    for i in range(num_human):
        player_list.append(HumanPlayer(i, goals[i]))
    for i in range(num_human, num_human + num_random):
        player_list.append(RandomPlayer(i, goals[i]))
    for i in range(num_human + num_random,
                   num_human + num_random + len(smart_players)):
        player_list.append(SmartPlayer(i, goals[i],
                                       smart_players[i - num_human -
                                                     num_random]))
    return player_list


def _get_block(block: Block, location: Tuple[int, int], level: int) -> \
        Optional[Block]:
    """Return the Block within <block> that is at <level> and includes
    <location>. <location> is a coordinate-pair (x, y).

    A block includes all locations that are strictly inside of it, as well as
    locations on the top and left edges. A block does not include locations that
    are on the bottom or right edge.

    If a Block includes <location>, then so do its ancestors. <level> specifies
    which of these blocks to return. If <level> is greater than the level of
    the deepest block that includes <location>, then return that deepest block.

    If no Block can be found at <location>, return None.

    Preconditions:
        - 0 <= level <= max_depth
    """
    # TODO: Implement me
    # can i import board_size
    if block.size < location[0] < 0 or block.size < location[1] < 0 or \
            block.level > block.max_depth:
        # no block at location
        return None
    elif block.level == level and block.size >= location[0] - \
            block.position[0] >= 0 and block.size >= location[1] - \
            block.position[1] >= 0:
        return block
    else:
        for child in block.children:
            if _get_block(child, location, level) is not None:
                return _get_block(child, location, level)
        return None


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.
    """
    id: int
    goal: Goal

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.id = player_id

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player.

        If no block is selected by the player, return None.
        """
        raise NotImplementedError

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event.
        """
        raise NotImplementedError

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a potential move to make on the game board.

        The move is a tuple consisting of a string, an optional integer, and
        a block. The string indicates the move being made (i.e., rotate, swap,
        or smash). The integer indicates the direction (i.e., for rotate and
        swap). And the block indicates which block is being acted on.

        Return None if no move can be made, yet.
        """
        raise NotImplementedError


def _create_move(action: Tuple[str, Optional[int]], block: Block) -> \
        Tuple[str, Optional[int], Block]:
    """ Returns a tuple that represents a move for a human player. """
    return action[0], action[1], block


class HumanPlayer(Player):
    """A human player.
    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.
    === Private Attributes ===
    _level:
        The level of the Block that the user selected most recently.
    _desired_action:
        The most recent action that the user is attempting to do.

    == Representation Invariants concerning the private attributes ==
        _level >= 0
    """
    id: int
    goal: Goal
    _level: int
    _desired_action: Optional[Tuple[str, Optional[int]]]

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        Player.__init__(self, player_id, goal)

        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._desired_action = None

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player based on
        the position of the mouse on the screen and the player's desired level.

        If no block is selected by the player, return None.
        """
        mouse_pos = pygame.mouse.get_pos()
        block = _get_block(board, mouse_pos, self._level)

        return block

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        the mapping in KEY_ACTION, as well as the W and S keys for changing
        the level.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_ACTION:
                self._desired_action = KEY_ACTION[event.key]
            elif event.key == pygame.K_w:
                self._level = max(0, self._level - 1)
                self._desired_action = None
            elif event.key == pygame.K_s:
                self._level += 1
                self._desired_action = None

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return the move that the player would like to perform. The move may
        not be valid.

        Return None if the player is not currently selecting a block.
        """
        block = self.get_selected_block(board)

        if block is None or self._desired_action is None:
            return None
        else:
            move = _create_move(self._desired_action, block)

            self._desired_action = None
            return move


class RandomPlayer(Player):
    """ A Player that does random moves.
    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.

    === Private Attributes ===
    _proceed:
      True when the player should make a move, False when the player should
      wait.
    """
    id: int
    goal: Goal
    _proceed: bool

    def __init__(self, player_id: int, goal: Goal) -> None:
        # TODO: Implement Me
        Player.__init__(self, player_id, goal)
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid, randomly generated move.

        A valid move is a move other than PASS that can be successfully
        performed on the <board>.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove
        # TODO: Implement Me

        valid_move = False          # checker for validity
        all_moves = [ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE,
                     SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH,
                     COMBINE, PAINT]
        final_move = None
        while not valid_move:
            block = None
            move_type = 0
            while block is None:
                block_level = random.randint(0, board.max_depth)
                move_type = random.randint(0, len(all_moves) - 1)
                random_x = random.randint(0, board.size)
                random_y = random.randint(0, board.size)
                block = _get_block(board, (random_x, random_y), block_level)
            block_copy = block.create_copy()
            if move_type == 0:
                if block_copy.rotate(1):
                    final_move = (ROTATE_CLOCKWISE + (block,))
                    valid_move = True
            elif move_type == 1:
                if block_copy.rotate(3):
                    final_move = (ROTATE_COUNTER_CLOCKWISE + (block,))
                    valid_move = True
            elif move_type == 2:
                if block_copy.swap(0):
                    final_move = (SWAP_HORIZONTAL + (block,))
                    valid_move = True
            elif move_type == 3:
                if block_copy.swap(1):
                    final_move = (SWAP_VERTICAL + (block,))
                    valid_move = True
            elif move_type == 4:
                if block_copy.smash():
                    final_move = (SMASH + (block,))
                    valid_move = True
            elif move_type == 5:
                if block_copy.combine():
                    final_move = (COMBINE + (block,))
                    valid_move = True
            else:  # move_type == 6:
                if block_copy.paint(self.goal.colour):
                    final_move = (PAINT + (block,))
                    valid_move = True

        self._proceed = False  # Must set to False before returning!
        return final_move


class SmartPlayer(Player):
    """ A strategic player with a certain level of difficulty.
    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.
    difficulty:
        This player's difficulty level.
    === Private Attributes ===
    _proceed:
      True when the player should make a move, False when the player should
      wait.
    """
    id: int
    goal: Goal
    difficulty: int
    _proceed: bool

    def __init__(self, player_id: int, goal: Goal, difficulty: int) -> None:
        # TODO: Implement Me
        Player.__init__(self, player_id, goal)
        self.difficulty = difficulty
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def _generate_move_helper(self, board: Block, move_list: List) -> None:
        """ Append a valid move for self on board to move_list."""
        valid_move = False          # checker for validity
        all_moves = [ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE,
                     SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH,
                     COMBINE, PAINT]
        final_move = None
        while not valid_move:
            block = None
            move_type = random.randint(0, len(all_moves) - 1)
            board_copy = board.create_copy()
            random_x = 0
            random_y = 0
            block_level = 0
            while block is None:
                # repeat if the block selected is None, i.e. no block at
                # that position at that depth
                block_level = random.randint(0, board.max_depth)
                random_x = random.randint(0, board.size)
                random_y = random.randint(0, board.size)
                block = _get_block(board_copy, (random_x, random_y),
                                   block_level)
            board_block = _get_block(board, (random_x, random_y), block_level)
            if move_type == 0:
                if block.rotate(1):
                    final_move = (ROTATE_CLOCKWISE +
                                  (block, self.goal.score(board_copy),
                                   board_block))
                    valid_move = True
            elif move_type == 1:
                if block.rotate(3):
                    final_move = (ROTATE_COUNTER_CLOCKWISE +
                                  (block, self.goal.score(board_copy),
                                   board_block))
                    valid_move = True
            elif move_type == 2:
                if block.swap(0):
                    final_move = (SWAP_HORIZONTAL +
                                  (block, self.goal.score(board_copy),
                                   board_block))
                    valid_move = True
            elif move_type == 3:
                if block.swap(1):
                    final_move = (SWAP_VERTICAL +
                                  (block, self.goal.score(board_copy),
                                   board_block))
                    valid_move = True
            elif move_type == 4:
                if block.smash():
                    final_move = (SMASH + (block, self.goal.score(board_copy),
                                           board_block))
                    valid_move = True
            elif move_type == 5:
                if block.combine():
                    final_move = (COMBINE + (block, self.goal.score(board_copy),
                                             board_block))
                    valid_move = True
            else:  # move_type == 6:
                if block.paint(self.goal.colour):
                    final_move = (PAINT + (block, self.goal.score(board_copy),
                                           board_block))
                    valid_move = True

        move_list.append(final_move)

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid move by assessing multiple valid moves and choosing
        the move that results in the highest score for this player's goal (i.e.,
        disregarding penalties).

        A valid move is a move other than PASS that can be successfully
        performed on the <board>. If no move can be found that is better than
        the current score, this player will pass.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove
        # TODO: Implement Me
        move_list = []
        current_score = self.goal.score(board)
        best_move = PASS + (board, current_score, board)
        while len(move_list) < self.difficulty:
            self._generate_move_helper(board, move_list)
        for move in move_list:
            if move[3] > current_score:
                current_score = move[3]
                best_move = move
        actual_action = best_move[0], best_move[1], best_move[4]
        self._proceed = False  # Must set to False before returning!
        return actual_action  # FIXME


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'actions', 'block',
            'goal', 'pygame', '__future__'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
