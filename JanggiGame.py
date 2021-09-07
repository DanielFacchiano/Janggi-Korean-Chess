"""
Created on Feb 25, 2021
@author: Daniel Facchiano
Portfolio Project: Janggi Korean Chess
Korean Board Game involving the movement of game pieces with coordinate restrictions. Game is coded with an array
of pieces to simulate a board with moving pieces. Pieces have specific coordinate restrictions meaning they can only
make specific movements on the board. Movements are coordinate difference's calculated by subtracting and adding origin
coordinates and destination coordinates. Pieces can move in a special way for certain squares and have specific piece
restrictions (ex: cannon cannot jump over a another cannon). The Game is won when one player no longer has a valid move
to avoid check at the end of their turn.
"""


class Game_Piece:
    """
    Object represents a generic Janggi Game Piece. Pieces have a location the Board (a list in the game class,
    a team affiliation and their coordinate locations on the board. Pieces have specific operations depending on
     their classification but that is not dealt with here. This class contains getter setters and prototype function
     and various helper functions to help pieces find navigate the board
    """

    def __init__(self, player_color, coordinate):
        """
        Game piece constructor, sets coordinates and piece color
        """
        self.__player_color = player_color
        self.__coordinates = coordinate

    def has_path_to(self, d_coord, board):
        """
        All pieces must be able to detect a path to somewhere else on the board. This is generally accomplished by
        comparing pieces coordinate variable to a Destination Coordinate (Denoted d_coord). The difference between
        the x and y from origin coordinates (sometimes denoted o_coord) to d_coord will be compared to the piece's
        movement profile to determine if the piece had a path to the destination. Path detection generally used in
        valid_move function for path detecting phase of determining if a move is valid. Used to detect check as well.
        """
        return False

    def get_player_color(self):
        """
        Returns the player color of the selected game_piece
        """
        return self.__player_color

    def set_coordinates(self, new_coordinates):
        """
        Set location of game_piece to passed coordinate tuple
        """
        self.__coordinates = new_coordinates

    def get_coordinates(self):
        """
        Returns current coordinates of the Game Piece
        """
        return self.__coordinates

    def get_at_relative(self, relative_coordinates, board):
        """
        This function returns the object on the grid relative to the passed x and y values, useful for detecting
        where pieces are relative to another.
        """
        rel_y = self.get_coordinates()[0] + relative_coordinates[0]
        rel_x = self.get_coordinates()[1] + relative_coordinates[1]
        return board[rel_y][rel_x]

    def can_be_blocked_at(self, d_coord):
        """
        By default, a piece cannot be blocked and returns an empty list, overwritten for certain pieces
        """
        empty_list = []
        return empty_list

    def in_the_blue_palace(self, d_coord):
        """
        Takes coordinate, returns if in the blue palace.
        """
        if d_coord == (10, 4) or d_coord == (9, 4) or d_coord == (8, 4) or d_coord == (10, 5) or d_coord == (9, 5) or \
                d_coord == (8, 5) or d_coord == (10, 6) or d_coord == (9, 6) or d_coord == (8, 6):
            return True
        else:
            return False

    def in_the_red_palace(self, d_coord):
        """
        Takes coordinate, returns if in the red palace.
        """
        if d_coord == (1, 4) or d_coord == (2, 4) or d_coord == (3, 4) or d_coord == (1, 5) or d_coord == (2, 5) or \
                d_coord == (3, 5) or d_coord == (1, 6) or d_coord == (2, 6) or d_coord == (3, 6):
            return True
        else:
            return False


class General(Game_Piece):
    """
    Game piece represented as General, Game is over when the general is checkmated. General restricted to the
    Palace. General represented on board of Game object. General has basic movement.
    """

    def __init__(self, player_color, coordinate):
        """
        Calls super constructor
        """
        super().__init__(player_color, coordinate)

    def get_name(self):
        """
        Returns Name of Piece
        """
        return self.get_player_color() + " general"

    def has_path_to(self, d_coord, board):  # [y][x]
        """
        Determines movement for generals, will depend on  mostly on palace constraints
        Can move 1 in any direction, but if in palace corner squares or center, can move 1,1 in any direction or
        only towards the center depending on orientation.
        """
        # If we select the same square our piece is on as the destination, that square is "in range" of our piece.
        if self.get_coordinates()[0] == d_coord[0] and self.get_coordinates()[1] == d_coord[1]:
            return True

        y_dif = d_coord[0] - self.get_coordinates()[0]
        x_dif = d_coord[1] - self.get_coordinates()[1]
        # print(y_dif, " ", x_dif)
        piece_color = self.get_player_color()
        if piece_color == "blue":
            d_in_palace = self.in_the_blue_palace(d_coord)
        else:
            d_in_palace = self.in_the_red_palace(d_coord)

        if d_in_palace is False:
            return False

        # We have ensured our destination is not outside our own palace. So if we are in the center, any move is valid.
        if piece_color == "blue" and self.get_coordinates() == (9, 5):
            return True
        elif piece_color == "blue" and self.get_coordinates() != (9, 5) and d_coord == (9, 5):
            return True
        if piece_color == "red" and self.get_coordinates() == (2, 5):
            return True
        elif piece_color == "red" and self.get_coordinates() != (2, 5) and d_coord == (2, 5):
            return True
        # That should handle all of the Diagonal movements

        if y_dif == 0 and (x_dif == 1 or x_dif == -1):
            return True
        elif x_dif == 0 and (y_dif == 1 or y_dif == -1):
            return True
        else:
            return False


class Guard(Game_Piece):
    """
    Game piece represented as Guard. Guards movement is restricted to the palace. Located on the board of the game
    object. Guard can move 1 space x or why, and move along palace diagonals
    """

    def __init__(self, player_color, coordinate):
        """
        Calls super constructor
        """
        super().__init__(player_color, coordinate)

    def get_name(self):
        """
        Returns name of Piece
        """
        return self.get_player_color() + " guard"

    def has_path_to(self, d_coord, board):  # [y][x]
        """
        Will use basically the same movement constraints present for the general.
        """
        # If we select the same square, we are passing our turn, which is a valid move
        if self.get_coordinates()[0] == d_coord[0] and self.get_coordinates()[1] == d_coord[1]:
            return True

        y_dif = d_coord[0] - self.get_coordinates()[0]
        x_dif = d_coord[1] - self.get_coordinates()[1]
        # print(y_dif, " ", x_dif)
        piece_color = self.get_player_color()

        if piece_color == "blue":
            d_in_palace = self.in_the_blue_palace(d_coord)
        else:
            d_in_palace = self.in_the_red_palace(d_coord)

        if d_in_palace is False:
            return False

        # We have ensured our destination is not outside our own palace. So if we are in the center, any move is valid.
        if piece_color == "blue" and self.get_coordinates() == (9, 5):
            return True
        elif piece_color == "blue" and self.get_coordinates() != (9, 5) and d_coord == (9, 5):
            return True
        if piece_color == "red" and self.get_coordinates() == (2, 5):
            return True
        elif piece_color == "red" and self.get_coordinates() != (2, 5) and d_coord == (2, 5):
            return True
        # That should handle all of the Diagonal movements

        if y_dif == 0 and (x_dif == 1 or x_dif == -1):
            return True
        elif x_dif == 0 and (y_dif == 1 or y_dif == -1):
            return True
        else:
            return False


class Horse(Game_Piece):
    """
    Game piece represented as Horse. Piece represented on Board of Game object. Movement same as chess Knight, but
    horses cannot jump over a piece one square in front of them.
    """

    def __init__(self, player_color, coordinate):
        """
        Calls game_piece super constructor
        """

        super().__init__(player_color, coordinate)

    def get_name(self):
        """
        Returns name of Piece
        """
        return self.get_player_color() + " horse"

    def has_path_to(self, d_coord, board):  # [y][x]
        """
        Horses can move 2,(1 or -1), -2,(1 or -1), (1 or -1),-2 or (1 or -1), 2 if they are not being blocked
        There are 8 horse movements and four ways to block any of these movements (4 checks)
        """
        # If we select the same square, we are moving to our own square,
        # which means we have path to because we can "pass"
        if self.get_coordinates()[0] == d_coord[0] and self.get_coordinates()[1] == d_coord[1]:
            return True

        y_dif = d_coord[0] - self.get_coordinates()[0]
        x_dif = d_coord[1] - self.get_coordinates()[1]
        # print(y_dif, " ", x_dif)
        if y_dif == -2 and (x_dif == 1 or x_dif == -1) and self.get_at_relative((-1, 0), board) is None:
            return True
        if y_dif == 2 and (x_dif == 1 or x_dif == -1) and self.get_at_relative((1, 0), board) is None:
            return True
        if x_dif == 2 and (y_dif == 1 or y_dif == -1) and self.get_at_relative((0, 1), board) is None:
            return True
        if x_dif == -2 and (y_dif == 1 or y_dif == -1) and self.get_at_relative((0, -1), board) is None:
            return True

        return False

    def can_be_blocked_at(self, d_coord):
        """
        This function is only called when the piece is already confirmed to have a valid path to d_coord
        Function returns the square Horse can be blocked at depending on movement.
        """
        square_list = []
        y_dif = d_coord[0] - self.get_coordinates()[0]
        x_dif = d_coord[1] - self.get_coordinates()[1]
        if y_dif == -2 and (x_dif == 1 or x_dif == -1):
            square_list.append((self.get_coordinates()[0] + (-1), self.get_coordinates()[1]))
        elif y_dif == 2 and (x_dif == 1 or x_dif == -1):
            square_list.append((self.get_coordinates()[0] + 1, self.get_coordinates()[1]))
        elif x_dif == 2 and (y_dif == 1 or y_dif == -1):
            square_list.append((self.get_coordinates()[0], self.get_coordinates()[1] + 1))
        elif x_dif == -2 and (y_dif == 1 or y_dif == -1):
            square_list.append((self.get_coordinates()[0], self.get_coordinates()[1] + (-1)))

        return square_list


class Elephant(Game_Piece):
    """
    Game piece represented as Elephant. piece represented on Board of Game object. Movement similar to horse.
    """

    def __init__(self, player_color, coordinate):
        """
        Calls super constructor
        """
        super().__init__(player_color, coordinate)

    def get_name(self):
        """
        Returns name of the Piece
        """
        return self.get_player_color() + " elephant"

    def has_path_to(self, d_coord, board):  # [y][x]
        """
        Very similar to Horse, but now our moves are 3,(2 or -2), -3,(2 or -2), (2 or -2),-3 or (2 or -2), 3 and
        there are now 2 potential squares we must check to see if we are being blocked for each of the 8
        movements.
        """
        # If we select the same square, we are moving to our own square,
        # which means we have path to because we can "pass"
        if self.get_coordinates()[0] == d_coord[0] and self.get_coordinates()[1] == d_coord[1]:
            return True

        y_dif = d_coord[0] - self.get_coordinates()[0]
        x_dif = d_coord[1] - self.get_coordinates()[1]
        # print(y_dif, " ", x_dif)
        if y_dif == -3 and x_dif == 2:
            if self.get_at_relative((-2, 1), board) is None and self.get_at_relative((-1, 0), board) is None:
                return True
        if y_dif == -3 and x_dif == -2:
            if self.get_at_relative((-2, -1), board) is None and self.get_at_relative((-1, 0), board) is None:
                return True
        if y_dif == -2 and x_dif == 3:
            if self.get_at_relative((-1, 2), board) is None and self.get_at_relative((0, 1), board) is None:
                return True
        if y_dif == 2 and x_dif == 3:
            if self.get_at_relative((1, 2), board) is None and self.get_at_relative((0, 1), board) is None:
                return True
        if y_dif == 3 and x_dif == 2:
            if self.get_at_relative((2, 1), board) is None and self.get_at_relative((1, 0), board) is None:
                return True
        if y_dif == 3 and x_dif == -2:
            if self.get_at_relative((2, -1), board) is None and self.get_at_relative((1, 0), board) is None:
                return True
        if y_dif == 2 and x_dif == -3:
            if self.get_at_relative((1, -2), board) is None and self.get_at_relative((0, -1), board) is None:
                return True
        if y_dif == -2 and x_dif == -3:
            if self.get_at_relative((-1, -2), board) is None and self.get_at_relative((0, -1), board) is None:
                return True
        return False

    def can_be_blocked_at(self, d_coord):
        """
        This function is only called when the piece is already confirmed to have a valid path to d_coord
        Functions return squares enemy piece could move to in order to block move to d_coord
        """
        square_list = []
        y_dif = d_coord[0] - self.get_coordinates()[0]
        x_dif = d_coord[1] - self.get_coordinates()[1]
        if y_dif == -3 and x_dif == 2:
            square_list.append((self.get_coordinates()[0] + (-1), self.get_coordinates()[1]))
            square_list.append((self.get_coordinates()[0] + (-2), self.get_coordinates()[1] + (1)))
        elif y_dif == -3 and x_dif == -2:
            square_list.append((self.get_coordinates()[0] + (-2), self.get_coordinates()[1] + (-1)))
            square_list.append((self.get_coordinates()[0] + (-1), self.get_coordinates()[1]))
        elif y_dif == -2 and x_dif == 3:
            square_list.append((self.get_coordinates()[0] + (-1), self.get_coordinates()[1] + (2)))
            square_list.append((self.get_coordinates()[0], self.get_coordinates()[1] + 1))
        elif y_dif == 2 and x_dif == 3:
            square_list.append((self.get_coordinates()[0] + (1), self.get_coordinates()[1] + (2)))
            square_list.append((self.get_coordinates()[0] + (0), self.get_coordinates()[1] + 1))
        elif y_dif == 3 and x_dif == 2:
            square_list.append((self.get_coordinates()[0] + (2), self.get_coordinates()[1] + (1)))
            square_list.append((self.get_coordinates()[0] + (1), self.get_coordinates()[1]))
        elif y_dif == 3 and x_dif == -2:
            square_list.append((self.get_coordinates()[0] + (2), self.get_coordinates()[1] + (-1)))
            square_list.append((self.get_coordinates()[0] + (1), self.get_coordinates()[1]))
        elif y_dif == 2 and x_dif == -3:
            square_list.append((self.get_coordinates()[0] + (1), self.get_coordinates()[1] + (-2)))
            square_list.append((self.get_coordinates()[0], self.get_coordinates()[1] + (-1)))
        elif y_dif == -2 and x_dif == -3:
            square_list.append((self.get_coordinates()[0] + (-1), self.get_coordinates()[1] + (-2)))
            square_list.append((self.get_coordinates()[0], self.get_coordinates()[1] + (-1)))

        return square_list


class Chariot(Game_Piece):
    """
    Game piece represented as Chariot. Piece represented on Board of Game object. Movement similar to rook.
    """

    def __init__(self, player_color, coordinate):
        """
        Calls super constructor
        """
        super().__init__(player_color, coordinate)

    def get_name(self):
        """
        Returns piece name
        """
        return self.get_player_color() + " chariot"

    def palace_moves(self, d_coord, board):
        """
        5 starting positions per palace, 2 variations for each of the 4 corners. 18 total conditions.
        """
        # We know that we are in either the red palace seeking a destination in red or vice versa. So any move
        # we make from the center to any of the 8 squares we could be in, are always in range.
        if self.get_coordinates() == (2, 5) or self.get_coordinates() == (9, 5):
            return True

        if self.get_coordinates() == (8, 4) and d_coord == (9, 5):
            return True
        if self.get_coordinates() == (8, 4) and d_coord == (10, 6) and board[9][5] is None:
            return True

        if self.get_coordinates() == (8, 6) and d_coord == (9, 5):
            return True
        if self.get_coordinates() == (8, 6) and d_coord == (10, 4) and board[9][5] is None:
            return True

        if self.get_coordinates() == (10, 4) and d_coord == (9, 5):
            return True
        if self.get_coordinates() == (10, 4) and d_coord == (8, 6) and board[9][5] is None:
            return True

        if self.get_coordinates() == (10, 6) and d_coord == (9, 5):
            return True
        if self.get_coordinates() == (10, 6) and d_coord == (8, 4) and board[9][5] is None:
            return True
        #
        if self.get_coordinates() == (1, 4) and d_coord == (2, 5):
            return True
        if self.get_coordinates() == (1, 4) and d_coord == (3, 6) and board[2][5] is None:
            return True

        if self.get_coordinates() == (1, 6) and d_coord == (2, 5):
            return True
        if self.get_coordinates() == (1, 6) and d_coord == (3, 4) and board[2][5] is None:
            return True

        if self.get_coordinates() == (3, 4) and d_coord == (2, 5):
            return True
        if self.get_coordinates() == (3, 4) and d_coord == (1, 6) and board[2][5] is None:
            return True

        if self.get_coordinates() == (3, 6) and d_coord == (2, 5):
            return True
        if self.get_coordinates() == (3, 6) and d_coord == (1, 4) and board[2][5] is None:
            return True

    def has_path_to(self, d_coord, board):  # [y][x]
        """
        With chariots, we must see if we are being blocked by checking if something is present in any
        of the squares in between the chariot and its destination. I will accomplish this by by calculating
         the x or y difference, and looping through those slots in x or y direction to determine if a piece
         is in the way or not, if not, it is a valid move.
         """

        # If we select the same square, we are moving to our own square,
        # which means we have path to because we can "pass"
        if self.get_coordinates()[0] == d_coord[0] and self.get_coordinates()[1] == d_coord[1]:
            return True

        y_dif = d_coord[0] - self.get_coordinates()[0]
        x_dif = d_coord[1] - self.get_coordinates()[1]
        # print(y_dif, " ", x_dif)

        p_moves = False
        if self.in_the_blue_palace(self.get_coordinates()) and self.in_the_blue_palace(d_coord):
            p_moves = self.palace_moves(d_coord, board)
        if self.in_the_red_palace(self.get_coordinates()) and self.in_the_red_palace(d_coord):
            p_moves = self.palace_moves(d_coord, board)
        if p_moves is True:
            return True

        # Chariot has 4 case depending on if its moving in -x, x, y, or -y.
        # Chariots can only move on one axis
        if y_dif != 0 and x_dif != 0:
            return False
        # if y difference is negative we iterate through the difference in that direction (-1 or +1 for the actual
        # piece) to see if any other pieces are in between it and it's destination
        if x_dif == 0 and y_dif < 0:
            for y in range(-1, y_dif, -1):
                if self.get_at_relative((y, 0), board) is not None:
                    return False
        elif x_dif == 0 and y_dif > 0:
            for y in range(1, y_dif):
                if self.get_at_relative((y, 0), board) is not None:
                    return False
        elif y_dif == 0 and x_dif > 0:
            for x in range(1, x_dif):
                if self.get_at_relative((0, x), board) is not None:
                    return False
        else:  # y_dif ==0 and x_dif < 0:
            for x in range(-1, x_dif, -1):
                if self.get_at_relative((0, x), board) is not None:
                    return False
        # Nothing is in the way
        return True

    def can_be_blocked_at(self, d_coord):
        """
        This function is only called when the piece is already confirmed to have a valid path to d_coord
        Loops through orgin to destination and returns all squares in between
        """
        square_list = []
        y_dif = d_coord[0] - self.get_coordinates()[0]
        x_dif = d_coord[1] - self.get_coordinates()[1]

        if x_dif == 0 and y_dif < 0:
            for y in range(-1, y_dif, -1):
                square_list.append((self.get_coordinates()[0] + (y), self.get_coordinates()[1]))
        elif x_dif == 0 and y_dif > 0:
            for y in range(1, y_dif):
                square_list.append((self.get_coordinates()[0] + y, self.get_coordinates()[1]))
        elif y_dif == 0 and x_dif > 0:
            for x in range(1, x_dif):
                square_list.append((self.get_coordinates()[0], self.get_coordinates()[1] + x))
        elif y_dif == 0 and x_dif < 0:
            for x in range(-1, x_dif, -1):
                square_list.append((self.get_coordinates()[0], self.get_coordinates()[1] + x))

        return square_list


class Cannon(Game_Piece):
    """
    Game piece represented as Cannon. Piece represented on Board of Game object. Piece jumps other pieces
    """

    def __init__(self, player_color, coordinate):
        """
        Calls super constructor
        """
        super().__init__(player_color, coordinate)

    def get_name(self):
        """
        Returns name of piece
        """
        return self.get_player_color() + " cannon"

    def palace_moves(self, d_coord, board):
        """
        Handles the 4 palace moves a Cannon can make. Makes sure a piece is in the center of palace
        """

        if self.get_coordinates() == (1, 4) and d_coord == (3, 6):
            if board[2][5] is not None:
                return True

        if self.get_coordinates() == (1, 6) and d_coord == (3, 4):
            if board[2][5] is not None:
                return True

        if self.get_coordinates() == (3, 6) and d_coord == (1, 4):
            if board[2][5] is not None:
                return True

        if self.get_coordinates() == (3, 4) and d_coord == (1, 6):
            if board[2][5] is not None:
                return True

        if self.get_coordinates() == (8, 4) and d_coord == (10, 6):
            if board[9][5] is not None:
                return True

        if self.get_coordinates() == (8, 6) and d_coord == (10, 4):
            if board[9][5] is not None:
                return True

        if self.get_coordinates() == (10, 6) and d_coord == (8, 4):
            if board[9][5] is not None:
                return True

        if self.get_coordinates() == (10, 4) and d_coord == (8, 6):
            if board[9][5] is not None:
                return True

        return False

    def has_path_to(self, d_coord, board):  # [y][x]
        """
        Functions Similar to Chariot, will need to make sure that there is exactly one pieces between
        target and destination, will detect in a manner similar to chariot, if more than one or No pieces
        are between the target and the destination than the move is considered to be invalid
        """
        # If we select the same square, we are moving to our
        # own square, which means we have path to because we can "pass"
        if self.get_coordinates()[0] == d_coord[0] and self.get_coordinates()[1] == d_coord[1]:
            return True
        if board[d_coord[0]][d_coord[1]] is not None:
            if "cannon" in board[d_coord[0]][d_coord[1]].get_name():
                return False
        y_dif = d_coord[0] - self.get_coordinates()[0]
        x_dif = d_coord[1] - self.get_coordinates()[1]
        # print(y_dif, " ", x_dif)

        p_moves = False
        if self.in_the_blue_palace(self.get_coordinates()) and self.in_the_blue_palace(d_coord):
            p_moves = self.palace_moves(d_coord, board)
        if self.in_the_red_palace(self.get_coordinates()) and self.in_the_red_palace(d_coord):
            p_moves = self.palace_moves(d_coord, board)
        if p_moves is True:
            return True

        # Cannon Also has 4 case depending on if its moving in -x, x, y, or -y.
        if y_dif != 0 and x_dif != 0:
            return False
        # if y difference is negative we iterate through the difference in that direction (-1 or +1 for the actual
        # piece) to see if any other pieces are in between it and it's destination
        pieces_between = 0
        if x_dif == 0 and y_dif < 0:
            for y in range(-1, y_dif, -1):
                if self.get_at_relative((y, 0), board) is not None:
                    if "cannon" in self.get_at_relative((y, 0), board).get_name():
                        return False
                    pieces_between = pieces_between + 1
        elif x_dif == 0 and y_dif > 0:
            for y in range(1, y_dif):
                if self.get_at_relative((y, 0), board) is not None:
                    if "cannon" in self.get_at_relative((y, 0), board).get_name():
                        return False
                    pieces_between = pieces_between + 1
        elif y_dif == 0 and x_dif > 0:
            for x in range(1, x_dif):
                if self.get_at_relative((0, x), board) is not None:
                    if "cannon" in self.get_at_relative((0, x), board).get_name():
                        return False
                    pieces_between = pieces_between + 1
        else:  # y_dif ==0 and x_dif < 0:
            for x in range(-1, x_dif, -1):
                if self.get_at_relative((0, x), board) is not None:
                    if "cannon" in self.get_at_relative((0, x), board).get_name():
                        return False
                    pieces_between = pieces_between + 1

        if pieces_between == 1:
            return True
        else:
            return False

    def get_jumped_piece_coord(self, d_coord, board):
        """
        To properly handle the can_be_blocked_at function (as well as returning this square for checkmate checks)
        We need to first get the coordinates of the piece we are jumping.
        """
        y_dif = d_coord[0] - self.get_coordinates()[0]
        x_dif = d_coord[1] - self.get_coordinates()[1]
        if x_dif == 0 and y_dif < 0:
            for y in range(-1, y_dif, -1):
                if self.get_at_relative((y, 0), board) is not None:
                    return (self.get_coordinates()[0] + y), self.get_coordinates()[1]
        elif x_dif == 0 and y_dif > 0:
            for y in range(1, y_dif):
                if self.get_at_relative((y, 0), board) is not None:
                    return (self.get_coordinates()[0] + y), self.get_coordinates()[1]
        elif y_dif == 0 and x_dif > 0:
            for x in range(1, x_dif):
                if self.get_at_relative((0, x), board) is not None:
                    return self.get_coordinates()[0], (self.get_coordinates()[1] + x)
        elif y_dif == 0 and x_dif < 0:
            for x in range(-1, x_dif, -1):
                if self.get_at_relative((0, x), board) is not None:
                    return self.get_coordinates()[0], (self.get_coordinates()[1] + x)

    def can_be_blocked_at(self, jp_coord, d_coord):
        """
        Using the jumped Piece coordinate, we return all the squares between the cannon and its destination
        that are not the jumped pieces square.
        """

        square_list = []
        y_dif = d_coord[0] - self.get_coordinates()[0]
        x_dif = d_coord[1] - self.get_coordinates()[1]
        if x_dif == 0 and y_dif < 0:
            for y in range(-1, y_dif, -1):
                if ((self.get_coordinates()[0] + y), self.get_coordinates()[1]) != jp_coord:
                    square_list.append((self.get_coordinates()[0] + y, self.get_coordinates()[1]))

        elif x_dif == 0 and y_dif > 0:
            for y in range(1, y_dif):
                if ((self.get_coordinates()[0] + y), self.get_coordinates()[1]) != jp_coord:
                    square_list.append((self.get_coordinates()[0] + y, self.get_coordinates()[1]))

        elif y_dif == 0 and x_dif > 0:
            for x in range(1, x_dif):
                if ((self.get_coordinates()[0]), self.get_coordinates()[1] + x) != jp_coord:
                    square_list.append((self.get_coordinates()[0], self.get_coordinates()[1] + x))

        elif y_dif == 0 and x_dif < 0:
            for x in range(-1, x_dif, -1):
                if ((self.get_coordinates()[0]), self.get_coordinates()[1] + x) != jp_coord:
                    square_list.append((self.get_coordinates()[0], self.get_coordinates()[1] + x))

        return square_list


class Soldier(Game_Piece):
    """
    Game piece represented as soldier. Piece represented on Board of Game object. Cant move backwards, moves
    one space.
    """

    def __init__(self, player_color, coordinate):
        """
        Calls super constructor
        """
        super().__init__(player_color, coordinate)

    def get_name(self):
        """
        Returns Name of piece
        """
        return self.get_player_color() + " soldier"

    def palace_moves(self, d_coord, y_dif, x_dif):
        """
        If were in center of the red or blue palace, and our destination is somewhere else in the red or blue palace,
        it must be a valid move.
        """
        if self.get_coordinates() == (2, 5):
            return True
        if self.get_coordinates() == (9, 5):
            return True

        if self.get_coordinates() == (1, 4) or self.get_coordinates() == (1, 6) or self.get_coordinates() == (3, 4) \
                or self.get_coordinates() == (3, 6):
            if d_coord == (2, 5):
                return True

        if self.get_coordinates() == (8, 4) or self.get_coordinates() == (8, 6) or self.get_coordinates() == (10, 4) \
                or self.get_coordinates() == (10, 6):
            if d_coord == (9, 5):
                return True

        if self.get_player_color() == "blue":
            if y_dif == 1 and x_dif == 0:
                return True
        else:
            if y_dif == -1 and x_dif == 0:
                return True

        return False

    def has_path_to(self, d_coord, board):  # [y][x]
        """
        Detects if the passed piece has a path to the destination
        any direction except backwards. Soldiers can move 1 space freely within the palace like Guards and Generals.
        """
        # If we select the same square, we are moving to our own square,
        # which means we have path to because we can "pass"
        if self.get_coordinates()[0] == d_coord[0] and self.get_coordinates()[1] == d_coord[1]:
            return True

        player_color = self.get_player_color()
        # This lets us know which way is "forwards"
        if player_color == "blue":
            y_multiplier = -1
        else:
            y_multiplier = 1

        y_dif = d_coord[0] - self.get_coordinates()[0]
        x_dif = d_coord[1] - self.get_coordinates()[1]
        # print(y_dif, " ", x_dif)
        p_moves = False

        if self.in_the_blue_palace(self.get_coordinates()) and self.in_the_blue_palace(d_coord):
            p_moves = self.palace_moves(d_coord, y_dif, x_dif)

        if self.in_the_red_palace(self.get_coordinates()) and self.in_the_red_palace(d_coord):
            p_moves = self.palace_moves(d_coord, y_dif, x_dif)

        if p_moves is True:
            return True

        if y_dif == 0 and (x_dif == 1 or x_dif == -1):
            return True
        elif y_dif == 1 * y_multiplier and x_dif == 0:
            return True
        else:
            return False


class JanggiGame:
    """
    Game class, contains the actual game we are playing! It does this by interacting with game piece objects from other
     classes on board array. Simulate Janggi by representing Board as coordinates and implenting rules based upon those
      coordinates. Game is currently run with commands in python console. Game is played on Board array by checking if
      moves are valid and moving them if such. Turns are toggled upon succesul moves. The Game is over when the General
       is checkmated. Is Janggi, Korean Chess!
    """

    def __init__(self):
        """
        Dresses the board, sets game state, sets player's turn
        """
        self.__board = [[None for i in range(10)] for j in range(11)]
        self.__blue_active_pieces = []
        self.__red_active_pieces = []
        self.set_up_board()
        self.__game_state = "UNFINISHED"
        self.__color_turn = "blue"
        self.__board[0][0] = (self.get_player_turn() + "'s turn").upper()

    def get_blue_active_pieces(self):
        """
        returns blue active pieces list
        """
        return self.__blue_active_pieces

    def get_red_active_pieces(self):
        """
        Returns red active pieces list
        """
        return self.__red_active_pieces

    def add_to_blue_active_pieces(self, item):
        """
        Appends pass object to blue active pieces
        """
        self.__blue_active_pieces.append(item)

    def add_to_red_active_pieces(self, item):
        """
        Appends passed object to red active pieces
        """
        self.__red_active_pieces.append(item)

    def delete_from_blue_active_pieces(self, item):
        """
        Deletes passed object from blue active pieces
        """
        self.__blue_active_pieces.remove(item)

    def delete_from_red_active_pieces(self, item):
        """
        Deletes passed object from red active pieces
        """
        self.__red_active_pieces.remove(item)

    def set_up_board(self):
        """
        Initiates game piece objects on the board and in their respective active pieces list
        """
        # Set up column letters
        self.set_piece(0, 1, "a"), self.set_piece(0, 2, "b"), self.set_piece(0, 3, "c"), self.set_piece(0, 4, "d"),
        self.set_piece(0, 5, "e"), self.set_piece(0, 6, "f"), self.set_piece(0, 7, "g"), self.set_piece(0, 8, "h"),
        self.set_piece(0, 9, "i")

        # Set up row numbers
        self.set_piece(1, 0, "1"), self.set_piece(2, 0, "2"), self.set_piece(3, 0, "3"), self.set_piece(4, 0, "4"),
        self.set_piece(5, 0, "5"), self.set_piece(6, 0, "6"), self.set_piece(7, 0, "7"), self.set_piece(8, 0, "8"),
        self.set_piece(9, 0, "9"), self.set_piece(10, 0, "10")

        # place red pieces on the board, add them to red_active_pieces_list
        self.set_piece(2, 5, General("red", (2, 5))), self.add_to_red_active_pieces(self.get_piece(2, 5))
        self.set_piece(1, 1, Chariot("red", (1, 1))), self.add_to_red_active_pieces(self.get_piece(1, 1))
        self.set_piece(1, 2, Elephant("red", (1, 2))), self.add_to_red_active_pieces(self.get_piece(1, 2))
        self.set_piece(1, 3, Horse("red", (1, 3))), self.add_to_red_active_pieces(self.get_piece(1, 3))
        self.set_piece(1, 4, Guard("red", (1, 4))), self.add_to_red_active_pieces(self.get_piece(1, 4))
        self.set_piece(1, 6, Guard("red", (1, 6))), self.add_to_red_active_pieces(self.get_piece(1, 6))
        self.set_piece(1, 7, Elephant("red", (1, 7))), self.add_to_red_active_pieces(self.get_piece(1, 7))
        self.set_piece(1, 8, Horse("red", (1, 8))), self.add_to_red_active_pieces(self.get_piece(1, 8))
        self.set_piece(1, 9, Chariot("red", (1, 9))), self.add_to_red_active_pieces(self.get_piece(1, 9))
        self.set_piece(4, 1, Soldier("red", (4, 1))), self.add_to_red_active_pieces(self.get_piece(4, 1))
        self.set_piece(3, 2, Cannon("red", (3, 2))), self.add_to_red_active_pieces(self.get_piece(3, 2))
        self.set_piece(4, 3, Soldier("red", (4, 3))), self.add_to_red_active_pieces(self.get_piece(4, 3))
        self.set_piece(4, 5, Soldier("red", (4, 5))), self.add_to_red_active_pieces(self.get_piece(4, 5))
        self.set_piece(4, 7, Soldier("red", (4, 7))), self.add_to_red_active_pieces(self.get_piece(4, 7))
        self.set_piece(3, 8, Cannon("red", (3, 8))), self.add_to_red_active_pieces(self.get_piece(3, 8))
        self.set_piece(4, 9, Soldier("red", (4, 9))), self.add_to_red_active_pieces(self.get_piece(4, 9))

        # place blue pieces on the board, add them to blue_active_pieces list
        self.set_piece(9, 5, General("blue", (9, 5))), self.add_to_blue_active_pieces(self.get_piece(9, 5))
        self.set_piece(10, 1, Chariot("blue", (10, 1))), self.add_to_blue_active_pieces(self.get_piece(10, 1))
        self.set_piece(10, 2, Elephant("blue", (10, 2))), self.add_to_blue_active_pieces(self.get_piece(10, 2))
        self.set_piece(10, 3, Horse("blue", (10, 3))), self.add_to_blue_active_pieces(self.get_piece(10, 3))
        self.set_piece(10, 4, Guard("blue", (10, 4))), self.add_to_blue_active_pieces(self.get_piece(10, 4))
        self.set_piece(10, 6, Guard("blue", (10, 6))), self.add_to_blue_active_pieces(self.get_piece(10, 6))
        self.set_piece(10, 7, Elephant("blue", (10, 7))), self.add_to_blue_active_pieces(self.get_piece(10, 7))
        self.set_piece(10, 8, Horse("blue", (10, 8))), self.add_to_blue_active_pieces(self.get_piece(10, 8))
        self.set_piece(10, 9, Chariot("blue", (10, 9))), self.add_to_blue_active_pieces(self.get_piece(10, 9))
        self.set_piece(7, 1, Soldier("blue", (7, 1))), self.add_to_blue_active_pieces(self.get_piece(7, 1))
        self.set_piece(8, 2, Cannon("blue", (8, 2))), self.add_to_blue_active_pieces(self.get_piece(8, 2))
        self.set_piece(7, 3, Soldier("blue", (7, 3))), self.add_to_blue_active_pieces(self.get_piece(7, 3))
        self.set_piece(7, 5, Soldier("blue", (7, 5))), self.add_to_blue_active_pieces(self.get_piece(7, 5))
        self.set_piece(7, 7, Soldier("blue", (7, 7))), self.add_to_blue_active_pieces(self.get_piece(7, 7))
        self.set_piece(8, 8, Cannon("blue", (8, 8))), self.add_to_blue_active_pieces(self.get_piece(8, 8))
        self.set_piece(7, 9, Soldier("blue", (7, 9))), self.add_to_blue_active_pieces(self.get_piece(7, 9))

    def set_piece(self, y, x, obj):
        """
        Set passed object on the board at coordinates [y][x]
        """
        self.__board[y][x] = obj

    def get_piece(self, y_coord, x_coord):
        """
        Returns Piece at passed coordinate on the board [y][x]
        """
        return self.__board[y_coord][x_coord]

    def print_board(self):
        """
        Loops through every variable present in the board and prints it to screen in board format
        """
        for x in self.get_board():
            for y in x:
                if isinstance(y, str):
                    print(y.ljust(15, " "), end='')
                elif y is not None:
                    st = y.get_name() + " "
                    print(st.ljust(15, " "), end='')
                else:
                    st = str(y) + " "
                    print(st.ljust(15, " "), end='')
            print()

    def get_player_turn(self):
        """
        Returns who's turn it is
        """
        return self.__color_turn

    def get_board(self):
        """
        Returns the board
        """
        return self.__board

    def set_player_turn(self, new_color):
        """
        Sets players color
         """
        self.__color_turn = new_color

    def get_game_state(self):
        """
        returns gamestate, indicating if the game is finished or if a player has won
        """
        return self.__game_state

    def set_game_state(self, new_state):
        """
        Sets gamestate to passed string
        """
        self.__game_state = new_state

    @staticmethod
    def str_coord(coord_string):
        """
        Takes a coordinate string, checks if its valid, converts it into y x coordinate tupple.
        If invalid, we return false. Static because no reason for it not to be.
        """
        valid = False
        letter = coord_string[0]
        number = coord_string[1:]

        if letter == "a" or letter == "b" or letter == "c" or letter == "d" or letter == "i" \
                or letter == "f" or letter == "g" or letter == "h" or letter == "i" or letter == "e":
            if number == "1" or number == "2" or number == "3" or number == "4" or number == "5" \
                    or number == "6" or number == "7" or number == "8" or number == "9" or number == "10":
                valid = True

        if not valid:
            return False, False
        else:
            y_coord = int(number)
            if letter == "a":
                x_coord = 1
            elif letter == "b":
                x_coord = 2
            elif letter == "c":
                x_coord = 3
            elif letter == "d":
                x_coord = 4
            elif letter == "e":
                x_coord = 5
            elif letter == "f":
                x_coord = 6
            elif letter == "g":
                x_coord = 7
            elif letter == "h":
                x_coord = 8
            elif letter == "i":
                x_coord = 9

            return y_coord, x_coord

    def make_move(self, origin, destination):
        """
        Converts coordinates and checks if they are valid. Checks if it's the correct players turn, checks if there
        is a piece at the location. Checks if the proposed move is a valid move. If it is a valid move we
        will update the board and pieces lists as needed. Once turn has been made we toggle the color turn variable
         to the other player's color. Finally, we check if we put the other player in check, if we did, we then
         check to see if we put them in checkmate, if so, toggle gamestate and the game is finished.
        """
        if self.get_game_state() != "UNFINISHED":
            return False
        o_coord = self.str_coord(origin)
        d_coord = self.str_coord(destination)
        if o_coord[0] == False or o_coord[1] == False \
                or d_coord[0] == False or d_coord[1] == False:
            # print("invalid input")
            return False
        # We know input is valid, we have an origin coordinate and a destination coordinate
        # Now we will check if there is a piece at the origin, if so, we will check if its that players turn, if so we
        # pass the origin and destination coordinates to its valid_move function to see if it returns true, signifying
        # that we can make the move, then we make the move, change turn, return true, and we are done.
        if self.get_piece(o_coord[0], o_coord[1]) is None:
            return False
        else:
            team_color = self.get_piece(o_coord[0], o_coord[1]).get_player_color()
        if team_color != self.get_player_turn():
            return False

        is_valid = self.is_valid_move(o_coord, d_coord)
        # print("Move was valid = ", is_valid)
        # If the move is valid, we make the move
        if is_valid:
            o_temp = self.get_piece(o_coord[0], o_coord[1])
            # If were capturing a piece, we need to handle its deletion from the game
            d_temp = None
            if self.get_piece(d_coord[0], d_coord[1]) is not None and self.get_piece(d_coord[0], d_coord[1]) != \
                    self.get_piece(o_coord[0], o_coord[1]):
                d_temp = self.get_piece(d_coord[0], d_coord[1])
            # set old origin location to empty
            self.set_piece(o_coord[0], o_coord[1], None)
            if d_temp is not None:
                if team_color == "red":
                    self.delete_from_blue_active_pieces(d_temp)
                else:
                    self.delete_from_red_active_pieces(d_temp)
            o_temp.set_coordinates(d_coord)
            self.set_piece(d_coord[0], d_coord[1], o_temp)
            # valid move made, toggle turn
            if self.get_player_turn() == "blue":
                self.set_player_turn("red")
            else:
                self.set_player_turn("blue")

            self.set_piece(0, 0, ((self.get_player_turn() + "'s turn").upper()))

            if team_color == "blue":
                if self.is_in_check("red"):
                    if self.in_checkmate("red"):
                        self.set_game_state("BLUE_WON")
                        self.set_piece(0, 0, "BLUE WON")
            else:
                if self.is_in_check("blue"):
                    if self.in_checkmate("blue"):
                        self.set_game_state("RED_WON")
                        self.set_piece(0, 0, "RED WON")

            return True
        else:
            return False

    def is_valid_move(self, o_coord, d_coord):
        """
        This function tells us if a proposed move is valid, meaning we are not attacking our own color, we are
        moving into a square that is in range of the selected piece, and if by moving our piece we put our general in
        check. We prepare for the check, check by "making" the proposed move and checking the check function, if the
         move is in check after being "made" we know if it is valid or not. After this check, we always return the board
         and pieces list to their previous state, regardless of whether the move is valid or not. That is handled by
         make_move function.
        """
        if self.get_piece(o_coord[0], o_coord[1]) is None:
            return False

        team = self.get_piece(o_coord[0], o_coord[1]).get_player_color()

        # Handles if we are attacking a teammate. extra condition to ignore if passing turn
        if self.get_piece(d_coord[0], d_coord[1]) is not None and \
                self.get_piece(d_coord[0], d_coord[1]).get_player_color() == team and \
                self.get_piece(d_coord[0], d_coord[1]) != self.get_piece(o_coord[0], o_coord[1]):
            return False

        if self.get_piece(o_coord[0], o_coord[1]).has_path_to(d_coord, self.get_board()):
            d_temp = None
            o_temp = self.get_piece(o_coord[0], o_coord[1])
            if self.get_piece(d_coord[0], d_coord[1]) is not None:
                d_temp = self.get_piece(d_coord[0], d_coord[1])
                if o_temp != d_temp:
                    if d_temp.get_player_color() == "red":
                        self.delete_from_red_active_pieces(d_temp)
                    else:
                        self.delete_from_blue_active_pieces(d_temp)
            self.set_piece(o_coord[0], o_coord[1], None)
            self.set_piece(d_coord[0], d_coord[1], o_temp)
            o_temp.set_coordinates(d_coord)

            in_check = self.is_in_check(o_temp.get_player_color())
            self.set_piece(d_coord[0], d_coord[1], d_temp)
            self.set_piece(o_coord[0], o_coord[1], o_temp)
            o_temp.set_coordinates(o_coord)

            if d_temp is not None:
                if d_temp != o_temp:
                    if d_temp.get_player_color() == "red":
                        self.add_to_red_active_pieces(d_temp)
                    else:
                        self.add_to_blue_active_pieces(d_temp)
            if in_check:
                return False
            else:
                return True
        else:
            return False

    def is_in_check(self, defending_color):
        """
        We detect check by getting the attacking teams active_pieces list, and seeing if any of their pieces has a path
        to the defending generals coordinates. The defending generals will always be at [0] of the active pieces list
        because that specific piece is never deleted and re-added in any manner by valid_move.
         """

        if defending_color == "red":
            attacker_list = self.get_blue_active_pieces()
            defending_general_coord = self.get_red_active_pieces()[0].get_coordinates()
        else:
            attacker_list = self.get_red_active_pieces()
            defending_general_coord = self.get_blue_active_pieces()[0].get_coordinates()

        for x in attacker_list:
            if x.has_path_to(defending_general_coord, self.get_board()):
                return True

        return False

    def get_blue_palace_squares(self):
        """
        Checkmate Helper Function, returns Blue palace square coordinates.
        """
        square_list = []
        square_list.append((10, 4)), square_list.append((9, 4)), square_list.append((8, 4))
        square_list.append((10, 5)), square_list.append((9, 5)), square_list.append((8, 5)),
        square_list.append((10, 6)), square_list.append((9, 6)), square_list.append((8, 6))
        return square_list

    def get_red_palace_squares(self):
        """
        Checkmate Helper Function, returns Red palace square coordinates.
        """
        square_list = []
        square_list.append((1, 4)), square_list.append((2, 4)), square_list.append((3, 4))
        square_list.append((1, 5)), square_list.append((2, 5)), square_list.append((3, 5)),
        square_list.append((1, 6)), square_list.append((2, 6)), square_list.append((3, 6))
        return square_list

    def get_checkers(self, defending_color):
        """
        Let checkers be pieces threatening check on the opposing general. Loops through attacking active pieces,
        and returns all pieces with a path to the defending general.
        """
        checkers = []
        if defending_color == "red":
            attacker_list = self.get_blue_active_pieces()
            defending_general_coord = self.get_red_active_pieces()[0].get_coordinates()
        else:
            attacker_list = self.get_red_active_pieces()
            defending_general_coord = self.get_blue_active_pieces()[0].get_coordinates()

        for x in attacker_list:
            if x.has_path_to(defending_general_coord, self.get_board()):
                checkers.append(x)

        return checkers

    def in_checkmate(self, defending_color):
        """
        If at the end of red/blues turn, they have put there opponent in check, then we pass their opponent's
        color to this function to see if they have beaten their opponent, and if the game is over. The first thing
        we do is check if the threatened general has any valid moves within his own palace, if so, he is not in
        checkmate. Moving on, we check if the opponent's pieces attacking the general can be blocked by a valid
        move of any of the defending teams pieces or if they can be captured. Finally, we must also check
        if we are being attacked by a Cannon, if the Piece the Cannon is jumping is our own, and if we can block said
        Cannon by moving our piece such that the Cannon can no longer jump over it.
        This implementation avoids the quadratic solution of checking every valid move for every square for
        every defending piece.
        """
        if defending_color == "blue":
            defending_list = self.get_blue_active_pieces()
            defending_general_coord = self.get_blue_active_pieces()[0].get_coordinates()
            checkers = self.get_checkers("blue")
            palace_squares = self.get_blue_palace_squares()
        else:
            defending_list = self.get_red_active_pieces()
            defending_general_coord = self.get_red_active_pieces()[0].get_coordinates()
            checkers = self.get_checkers("red")
            palace_squares = self.get_red_palace_squares()

        for x in palace_squares:
            if self.is_valid_move(defending_general_coord, x):
                return False

        coords_to_block_checkers = []
        jumped_pieces_coords = []
        for x in checkers:
            if "cannon" in x.get_name():
                jumped_pieces_coords.append(x.get_jumped_piece_coord(defending_general_coord, self.get_board()))
                coords_to_block_checkers = coords_to_block_checkers + \
                                           x.can_be_blocked_at(jumped_pieces_coords[-1], defending_general_coord)
                coords_to_block_checkers.append(x.get_coordinates())
            else:
                coords_to_block_checkers = coords_to_block_checkers + x.can_be_blocked_at(defending_general_coord)
                coords_to_block_checkers.append(x.get_coordinates())

        for defender in defending_list:
            # print("defender is", defender.get_name())
            for square in coords_to_block_checkers:
                # print("attempting move for defender at", defender.get_coordinates(), "moving to", square)
                if self.is_valid_move(defender.get_coordinates(), square):
                    # print("it was valid")
                    return False

        # Worst case scenario we have an enemy cannon jumping our piece to attack our general, costly solution
        # of checking every single square on the board. (to see if we can block cannon by moving out of its jump)
        #  This check can occur twice if two cannons are checking us
        # (of which im not sure is even possible, but implemented just in case)
        for jp_coord in jumped_pieces_coords:
            jp = self.get_piece(jp_coord[0], jp_coord[1])
            if jp.get_player_color() == defending_color:
                for x in range(1, 10):
                    for y in range(1, 11):
                        if self.is_valid_move(jp_coord, (y, x)):
                            return False
        return True


def main():
    game = JanggiGame()
    move_result = game.make_move('c1', 'e3')  # should be False because it's not Red's turn
    move_result = game.make_move('a7', 'b7')
    blue_in_check = game.is_in_check('blue')
    game.make_move('a4', 'a5')  # should return True
    state = game.get_game_state()  # should return UNFINISHED
    game.make_move('b7', 'b6')  # should return True
    game.make_move('b3', 'b6')  # should return False because it's an invalid move
    game.make_move('a1', 'a4')  # should return True
    game.make_move('c7', 'd7')  # should return True
    game.make_move('a4', 'a4')  # this will pass the Red's turn and return True
    game.print_board()


if __name__ == "__main__":
    main()
