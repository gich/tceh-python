from random import randint, choice


class Board(object):

    PRINT_MARKS = {
        0: '•',  # empty cell
        1: '█',  # ship deck
        2: '*',  # missed shot
        3: '=',  # wounded
        4: 'X',  # killed
    }

    PRINT_MARKS_ENEMY = {
        0: '•',  # empty cell
        1: '•',  # ship deck
        2: '*',  # missed shot
        3: '=',  # wounded
        4: 'X',  # killed
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
            while ship_pref[ship] > 0:
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
                ship_pref[ship] -= 1
                self.ships.append(Ship(current_ship))

        # delete dummy cells
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] == 9:
                    self.field[i][j] = 0

    def __hold_cells_around(self, ship):

        for s in ship:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x = s[0]
                    y = s[1]
                    try:
                        if self.field[x+i][y+j] == 0:
                            self.field[x+i][y+j] = 9
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


class Player(object):
    def __init__(self, name):
        self.name = name


class Ship(object):
    def __init__(self, decks):
        self.decks = decks
        self.killed_decks = []


class Shot(object):
    def __init__(self):
        pass
