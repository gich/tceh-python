# -*- coding: utf-8 -*-

from models import (
                    Board,
                    Person,
                    Shot,
                    ComputerStupid
                    )
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

    active_player = Person(input("Player one, enter your name: "))
    # player_2 = Person(input("Player two, enter your name: "))
    player_2 = ComputerStupid('Not smart')

    active_field = Board(field_size, available_ships)
    field_2 = Board(field_size, available_ships)

    # We play till all ships are killed
    while len(active_field.ships) > 0 and len(field_2.ships) > 0:
        try:
            active_field.print_field_enemy()
            while True:
                try:
                    shot = active_player.perform_shot(active_field)
                    if not active_field.handle_shot(shot):
                        break
                    else:
                        active_field.print_field_enemy()
                except AlreadyShotException:
                    print("You have already shot here. Try again.")
                    continue
                except IndexError:
                    print('Bad input. Try again.')
                    continue
            active_player, player_2 = player_2, active_player
            active_field, field_2 = field_2, active_field

        except KeyboardInterrupt:
            if input("Are you sure you want to quit? (y/n): ") == 'y':
                print('Bye...')
                return
            else:
                continue
    print('The winner is ----------------> {}'.format(active_player.name))

    # print field for looser
    field_2.print_field_friend()


if __name__ == '__main__':
    main()
