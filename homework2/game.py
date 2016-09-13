# -*- coding: utf-8 -*-

# random module is used to shuffle field, see§:
# https://docs.python.org/3/library/random.html#random.shuffle
import random
import sys


# Empty tile, there's only one empty cell on a field:
EMPTY_MARK = 'x'

# Dictionary of possible moves if a form of:
# key -> delta to move the empty tile on a field.
MOVES = {
    'w': -4,
    's': 4,
    'a': -1,
    'd': 1,
}


def shuffle_field():
    """
    This method is used to create a field at the very start of the game.
    :return: list with 16 randomly shuffled tiles,
    one of which is a empty space.
    """

    field = list(range(1, 16))

    # check if the field can be solved
    while True:
        random.shuffle(field)
        pairs = 0
        for i in range(0, 14):
            for j in range(i+1, 15):
                if field[i] > field[j]:
                    pairs += 1
        pairs += 4
        if pairs % 2 == 0:
            field.append(EMPTY_MARK)
            return field


def print_field(field):
    """
    This method prints field to user.
    :param field: current field state to be printed.
    :return: None
    """

    for i in range(0, 15, 4):
        for element in field[i:i+4]:
            print ('{:^3}'.format(element)),
        print ('')


def is_game_finished(field):
    """
    This method checks if the game is finished.
    :param field: current field state.
    :return: True if the game is finished, False otherwise.
    """

    finished_state = list(range(1, 16))
    finished_state.append(EMPTY_MARK)

    return field == finished_state


def perform_move(field, key):
    """
    Moves empty-tile inside the field.
    :param field: current field state.
    :param key: move direction.
    :return: new field state (after the move).
    :raises: IndexError if the move can't me done.
    """

    empty_index = field.index(EMPTY_MARK)
    new_index = empty_index + MOVES[key]

    # new_index can be out of range or
    # while moving left or right we should avoid change of row for new_index
    if new_index in range(0, 17) and \
        abs(new_index % 4 - empty_index % 4) != 3:
        field[empty_index], field[empty_index+MOVES[key]] = \
            field[empty_index+MOVES[key]], field[empty_index]
        return field
    else:
        raise IndexError


def handle_user_input():
    """
    Handles user input. List of accepted moves:
        'w' - up,
        's' - down,
        'a' - left,
        'd' - right
    :return: <str> current move.
    """

    if sys.version_info[0] == 2:
        input_function = raw_input
    else:
        input_function = input

    while True:
        user_move = input_function('Your move: ')
        if user_move in MOVES:
            return user_move
        else:
            print ('incorrect input. Please use "wasd" keys.')


def main():
    """
    The main method. It stars when the program is called.
    It also calls other methods.
    :return: None
    """

    field = shuffle_field()
    total_moves = 0
    while not is_game_finished(field):
        print_field(field)
        try:
            move = handle_user_input()
            perform_move(field, move)
            total_moves += 1
        except KeyboardInterrupt:
            print('\nshutting down...')
            break
        except IndexError:
            print ("Incorrect move!")
    if is_game_finished(field):
        print("You've finished the game in {} moves".format(total_moves))


if __name__ == '__main__':
    # See what this means:
    # http://stackoverflow.com/questions/419163/what-does-if-name-main-do

    main()
