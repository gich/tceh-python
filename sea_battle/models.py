# -*- coding: utf-8 -*-
from random import randint, choice
from custom_exceptions import AlreadyShootedException


class Board(object):

    PRINT_MARKS = {
        0: '-',
        # 0: chr(149),  # '•',  # empty cell
        1: '█',  # ship deck
        2: '*',  # missed shot
        3: 'X',  # wounded
        4: '█',  # killed
    }

    PRINT_MARKS_ENEMY = {
        0: '-',
        # 0: '•',  # empty cell
        1: '-',  # ship deck
        2: '*',  # missed shot
        3: 'X',  # wounded
        4: '█',  # killed
    }

    def __init__(self, size, ship_pref):

        self.size = int(size)
        self.ships = []
        self.killed_ships = []
        self.field = [[0] * self.size for _ in range(self.size)]
        self.__place_ships(ship_pref)

    def __place_ships(self, ship_pref):
        """
        Randomly places ships on field avoiding collisions
        :param ship_pref: dict with available ships
        :return: None
        """
        # get all available types of decks sorted desc
        ship_decks = list(ship_pref.keys())
        ship_decks.sort(reverse=True)

        for ship in ship_decks:
            ship_count = ship_pref[ship]
            while ship_count > 0:
                pos_x = randint(0, self.size - 1)
                pos_y = randint(0, self.size - 1)
                # direction delta stays unchanged for ship
                delta = choice([(0, 1), (1, 0)])

                i = ship
                current_ship = []
                while i > 0:
                    try:
                        if self.field[pos_x][pos_y] == 0:
                            self.field[pos_x][pos_y] = 1
                            current_ship.append((pos_x, pos_y))
                            i -= 1
                            pos_x += delta[0]
                            pos_y += delta[1]
                        else:  # cell already taken
                            i = ship
                            pos_x = randint(0, self.size - 1)
                            pos_y = randint(0, self.size - 1)
                            for c in current_ship:
                                self.field[c[0]][c[1]] = 0
                            current_ship = []
                    except IndexError:  # trying to place ship behind borders
                        i = ship
                        pos_x = randint(0, self.size - 1)
                        pos_y = randint(0, self.size - 1)
                        for c in current_ship:
                            self.field[c[0]][c[1]] = 0
                        current_ship = []
                # surround ship with dummy cells to prevent collisions
                self.__hold_cells_around(current_ship)
                ship_count -= 1
                self.ships.append(Ship(current_ship))

        # delete dummy cells
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] == 9:
                    self.field[i][j] = 0

    def __hold_cells_around(self, ship):

        for s in ship:
            x_coord, y_coord = s
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if self.field[x_coord+i][y_coord+j] == 0:
                            self.field[x_coord+i][y_coord+j] = 9
                    except IndexError:
                        pass

    def print_field_friend(self):
        """
        Prints battle field to console with visible ship
        :return:
        """
        print()
        cols = list(range(1, 11))
        cols = [' '] + list(map(str, cols))
        print(" ".join(cols))
        for i in range(self.size):
            print(chr(65+i), end=' ')
            for j in range(self.size):
                print(self.PRINT_MARKS[self.field[i][j]], end=" ")
            print()
        print()

    def print_field_enemy(self):
        """
        Prints battle field to console with hided ships
        :return:
        """
        print()
        cols = list(range(1, 11))
        cols = [' '] + list(map(str, cols))
        print(" ".join(cols))
        for i in range(self.size):
            print(chr(65+i), end=' ')
            for j in range(self.size):
                print(self.PRINT_MARKS_ENEMY[self.field[i][j]], end=" ")
            print()
        print()

    def perform_shot(self, shot):

        if self.field[shot.row][shot.column] in [2, 3, 4]:
            raise AlreadyShootedException
        elif self.field[shot.row][shot.column] == 0:
            self.field[shot.row][shot.column] = 2
            print('Missed!')
            return 0
        elif self.field[shot.row][shot.column] == 1:
            self.field[shot.row][shot.column] = 3
            print('Booooooom!!!!')
            self.__update_shooted_ships((shot.row, shot.column))
            return 1

    def __update_shooted_ships(self, coordinates):
        for ship in self.ships:
            if coordinates in ship.decks:
                ship.killed_decks.append(coordinates)
                ship.decks.remove(coordinates)
                if len(ship.decks) == 0:
                    print("The {}-deck ship is killed".format(
                        len(ship.killed_decks))
                    )
                    for killed_deck in ship.killed_decks:
                        x, y = killed_deck
                        self.field[x][y] = 4
                    self.killed_ships.append(ship)
                    self.ships.remove(ship)


class Player(object):
    def __init__(self, name):
        self.name = name
        self.is_player_turn = False


class Ship(object):
    def __init__(self, decks):
        self.decks = decks
        self.killed_decks = []


class Shot(object):
    def __init__(self, action):
        _row = ord(action[:1].upper()) - 65
        _column = int(action[1:]) - 1
        if _row < 0 or _column < 0:
            raise ValueError
        self.row = _row
        self.column = _column
