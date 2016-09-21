# -*- coding: utf-8 -*-

from random import randint, choice
from custom_exceptions import AlreadyShotException


class Board(object):
    EMPTY = 0
    SHIP = 1
    MISSED = 2
    WOUND = 3
    KILLED = 4
    DUMMY = 5

    PRINT_MARKS = {
        EMPTY: '-',
        # 0: chr(149),  # '•',
        SHIP: 'H',
        MISSED: '*',
        WOUND: 'X',
        KILLED: '█',
    }

    def __init__(self, size, ship_pref):

        self.size = int(size)
        self.ships = []
        self.killed_ships = []
        self.field = [[self.EMPTY] * self.size for _ in range(self.size)]
        self.__place_ships(ship_pref)

    def __place_ships(self, all_ships):
        """
        Randomly places ships on field avoiding collisions
        :param all_ships: dict with available ships
        :return: None
        """
        # get all available types of ships sorted desc
        ship_types = list(all_ships.keys())
        ship_types.sort(reverse=True)

        for typ in ship_types:
            for _ in range(all_ships[typ]):
                ship = self.__place_ship_randomly(typ)

                # surround ship with dummy cells to prevent collisions
                self.__place_dummies_around(ship)

                self.ships.append(ship)
        self.__delete_dummies()

    def __place_ship_randomly(self, decks_num):
        pos_x = randint(0, self.size - 1)
        pos_y = randint(0, self.size - 1)

        # direction - vertical or horizontal delta
        delta = choice([(0, 1), (1, 0)])

        decks_coord = []
        decks_to_place = decks_num

        while decks_to_place > 0:
            try:
                if self.field[pos_x][pos_y] == self.EMPTY:
                    self.field[pos_x][pos_y] = self.SHIP
                    decks_coord.append((pos_x, pos_y))
                    decks_to_place -= 1
                    pos_x += delta[0]
                    pos_y += delta[1]
                else:  # cell already taken
                    raise IndexError
            except IndexError:  # trying to place ship behind borders
                decks_to_place = decks_num
                pos_x = randint(0, self.size - 1)
                pos_y = randint(0, self.size - 1)
                for c in decks_coord:
                    self.field[c[0]][c[1]] = self.EMPTY
                    decks_coord = []

        return Ship(decks_coord)

    def __place_dummies_around(self, ship):
        """
        Places dummy cells round the ship
        :param ship: list of tuple(x, y) with coordinates
        :return: None
        """
        for deck_coord in ship.decks:
            x_coord, y_coord = deck_coord
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if self.field[x_coord+i][y_coord+j] == self.EMPTY:
                            self.field[x_coord+i][y_coord+j] = self.DUMMY
                    except IndexError:
                        pass

    def __delete_dummies(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] == self.DUMMY:
                    self.field[i][j] = self.EMPTY

    def print_field(self, field_to_print):
        print()
        cols = list(range(1, 11))
        cols = [' '] + list(map(str, cols))
        print(" ".join(cols))
        for i in range(self.size):
            print(chr(65 + i), end=' ')
            for j in range(self.size):
                print(self.PRINT_MARKS[field_to_print[i][j]], end=" ")
            print()
        print()

    def print_field_friend(self):
        """
        Prints battle field to console with visible ships
        :return:
        """
        self.print_field(self.field)

    def print_field_enemy(self):
        """
        Prints battle field to console with hided ships
        :return:
        """
        self.print_field(self.secure_field)

    def handle_shot(self, shot):
        """
        Handles the shot received
        :param shot: Shot() from player
        :return: False if player miss, or True if player hits the ship
        :except: AlreadyShotException if player repeat his shot
        """
        if self.field[shot.row][shot.column] in [self.MISSED,
                                                 self.KILLED,
                                                 self.WOUND]:
            raise AlreadyShotException
        elif self.field[shot.row][shot.column] == 0:
            self.field[shot.row][shot.column] = 2
            print('Missed!')
            return False
        elif self.field[shot.row][shot.column] == 1:
            self.field[shot.row][shot.column] = 3
            print('Booooooom!!!!')
            self.__update_shot_ships((shot.row, shot.column))
            return True

    def __update_shot_ships(self, coordinates):
        """
        Updates ships and killed_ships attributes in Board instance
        and updates decks in wounded ship
        :param coordinates: tuple(x, y) with wounded deck
        :return:
        """
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
                        self.field[x][y] = self.KILLED
                    self.killed_ships.append(ship)
                    self.ships.remove(ship)

    @property
    def secure_field(self):
        def hide(val):
            return self.EMPTY if val == self.SHIP else val

        secure_field = []
        for row in self.field:
            secure_field.append(list(map(hide, row)))

        return secure_field


class Player(object):
    def __init__(self, name):
        self.name = name
        self.is_player_turn = False

    def perform_shot(self, board):
        raise NotImplemented


class Person(Player):
    def perform_shot(self, board):
        while True:
            action = input("Your turn, {}: ".format(self.name))
            try:
                shot = Shot(action)
                if not board.handle_shot(shot):
                    break
                else:
                    board.print_field_enemy()

            except AlreadyShotException:
                print("You have already shot here. Try again.")
                continue
            except (ValueError, IndexError):
                print('Bad input. Try again.')
                continue


class ComputerStupid(Player):
    def perform_shot(self, board):
        pass


class ComputerSmart(Player):
    def perform_shot(self, board):
        pass


class ComputerSuperSmart(Player):
    def perform_shot(self, board):
        pass


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
