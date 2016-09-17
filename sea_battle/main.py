# -*- coding: utf-8 -*-

from models import Board


def main():
    # defining default values
    field_size = 10
    available_ships = {1: 4, 2: 3, 3: 2, 4: 1}  # {ship_decks: ships_num}

    field = Board(field_size, available_ships)
    field.print_field()
    # field.print_field_enemy()


if __name__ == '__main__':
    main()
