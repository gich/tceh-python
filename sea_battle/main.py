# -*- coding: utf-8 -*-

from models import (
                    Board,
                    Person,
                    Shot,
                    ComputerStupid,
                    ComputerSmart,
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
    while True:
        print("Who is your opponent?")
        print("1. Player\n2. Smart computer\n3. Not smart computer")
        answer = input('Enter your choice: ')
        if answer == '1':
            player_2 = Person(input("Player two, enter your name: "))
            break
        elif answer == '2':
            player_2 = ComputerSmart('Smart comp')
            break
        elif answer == '3':
            player_2 = ComputerStupid('Not smart')
            break
        else:
            print('Bad input. Try again...')

    active_field = Board(field_size, available_ships)
    field_2 = Board(field_size, available_ships)

    # We play till all ships are killed
    while len(active_field.ships) > 0 and len(field_2.ships) > 0:
        try:
            print_both_fields(active_field, field_2, active_player, player_2)
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


def print_both_fields(board1, board2, player1, player2):
    print()
    cols = list(range(1, 11))
    cols = [' '] + list(map(str, cols))
    spaces = "     "
    width = (board1.size + 1) * 2
    print("{:^{width}}".format(player2.name, width=width), end=' ')
    print(spaces, end=' ')
    print("{:^{width}}".format(player1.name, width=width), end=' ')
    print()
    print(" ".join(cols), "   ", " ".join(cols))
    for i in range(board1.size):
        print(chr(65 + i), end=' ')
        for j in range(board1.size):
            print(board1.PRINT_MARKS[board1.secure_field[i][j]], end=' ')
        print(spaces, end='')
        print(chr(65 + i), end=' ')
        for j in range(board1.size):
            print(board2.PRINT_MARKS[board2.secure_field[i][j]], end=' ')
        print()
    print()


if __name__ == '__main__':
    main()
