# -*- coding: utf-8 -*-

from models import Board, Person, Shot
from custom_exceptions import AlreadyShotException


def main():
    """
    Main logic for the game.
    The game finishes when one of the board have no more ships.
    Player can press Ctrl+C to stop the game
    """

    # defining default values
    field_size = 10
    available_ships = {1: 4, 2: 3, 3: 2, 4: 1}  # {ship_decks: ships_num}

    player_1 = Person(input("Player one, enter your name: "))
    player_2 = Person(input("Player two, enter your name: "))

    field_1 = Board(field_size, available_ships)
    field_2 = Board(field_size, available_ships)

    player_1.is_player_turn = True
    active_player = player_1
    active_field = field_2

    while len(field_1.ships) > 0 and len(field_2.ships) > 0:
        try:
            if player_1.is_player_turn:
                active_player = player_1
                active_field = field_2
            else:
                active_player = player_2
                active_field = field_1

            active_field.print_field_enemy()
            active_player.perform_shot(active_field)

            player_1.is_player_turn = not player_1.is_player_turn
            player_2.is_player_turn = not player_2.is_player_turn
        except KeyboardInterrupt:
            if input("Are you sure you want to quit? (y/n): ") == 'y':
                print('Bye...')
                return
            else:
                continue
    print('The winner is ----------------> {}'.format(active_player.name))

    # print field for looser
    if active_field == field_1:
        field_2.print_field_friend()
    else:
        field_1.print_field_friend()


if __name__ == '__main__':
    main()
