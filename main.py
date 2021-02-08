from prettytable import PrettyTable
from math import sqrt
import random



class Hoppers(object):
    def __init__(self, playerOneIsBot = False, playerTwoIsBot = False):
        # Tablero 10 x 10
        self.current_state = [[1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                              [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                              [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                              [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                              [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                              [0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
                              [0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
                              [0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
                              [0, 0, 0, 0, 0, 2, 2, 2, 2, 2]]

        self.playerOne = 1
        self.playerTwo = 2
        self.player_turn = self.playerOne
        self.playerOneIsBot = playerOneIsBot
        self.playerTwoIsBot = playerTwoIsBot

        # Lista de coordenadas en donde estan las piezas de los jugadores 
        self.playerOneCornerCamp = []
        self.playerTwoCornerCamp = []
        self.corner_camps()

        self.game()
    
    def board(self):
        board = PrettyTable()
        board.hrules = 1
        board.header = False
        # board.padding_width = 0
        board.add_rows(self.current_state)
        # print("\n", " 0", "  1", "  2", "  3", "  4", "  5", "  6", "  7", "  8", "  9")
        print(board)
    
    def board2(self, tablero):
        board = PrettyTable()
        board.hrules = 1
        board.header = False
        # board.padding_width = 0
        board.add_rows(tablero)
        # print("\n", " 0", "  1", "  2", "  3", "  4", "  5", "  6", "  7", "  8", "  9")
        print(board)


    def corner_camps(self):
        self.playerOneCornerCamp = [(0,0), (1,0), (2,0), (3,0), (4,0),
                                    (0,1), (1,1), (2,1), (3,1),
                                    (0,2), (1,2), (2,2),
                                    (0,3), (1,3),
                                    (0,4)]
        self.playerTwoCornerCamp = [(9,5),
                                    (8,6), (9,6),
                                    (7,7), (8,7), (9,7),
                                    (6,8), (7,8), (8,8), (9,8),
                                    (5,9), (6,9), (7,9), (8,9), (9,9)]

    def next_turn(self):
        self.player_turn = 2 if self.player_turn == 1 else 1

    # TODO -----------------------------------------------------
    def check_if_there_is_winner(self, board):
        p1v = [self.current_state[position[1]][position[0]] for position in self.playerOneCornerCamp]
        p2v = [self.current_state[position[1]][position[0]] for position in self.playerTwoCornerCamp]

        if 1 in p2v and 0 not in p2v:
            print("El jugador 1 ha ganado")
            return True       
        if 2 in p1v and 0 not in p1v:
            print("El jugador 2 ha ganado")
            return True
        
        return False

    def move_piece(self, pfrom, to):
        pfrom = self.toTuple(pfrom)
        to = self.toTuple(to)
        self.current_state[pfrom[1]][pfrom[0]] = 0
        self.current_state[to[1]][to[0]] = self.player_turn

    def game(self):
        self.board()

        while not self.check_if_there_is_winner(self.current_state):
            if self.player_turn == self.playerOne:
                print("Jugador 1: ")
            else:
                print("Jugador 2: ")

            if (self.player_turn == 1 and self.playerOneIsBot) or (self.player_turn == 2 and self.playerTwoIsBot) :
                player_piece_move, player_coords_move = self.playAIbot()
            else:
                player_piece_move = input("Ingrese las coordenadas (x,y) de la pieza a mover: ")
                player_coords_move = input("Ingrese las coordenadas (x,y) donde desea mover: ")
            
            self.move_piece(player_piece_move, player_coords_move)
            self.next_turn()
            self.board()

    def toTuple(self, pinput):
        x, y = pinput.split(",")
        x, y = int(x), int(y)
        return (x, y)

          
    # TODO ----------------------------
    
    def playAIbot(self):
        movement_value, best_move = self.minimax(self.current_state, 1, self.player_turn)
        # print(best_move)
        move_from = "{x},{y}".format(x=best_move[0][0], y=best_move[0][1])
        move_to = "{x},{y}".format(x=best_move[1][0], y=best_move[1][1])
        return move_from, move_to
        # return best_move

    def boardIA(self, boardI):
        board = PrettyTable()
        board.add_rows(self.current_state)
        print(board)

    def minimax(self, board, depth, maximising=True, alfa=float("-inf"), beta=float("inf")):
        if self.check_if_there_is_winner(board):
            return self.eval(board, self.player_turn), None

        if depth == 0:
            random_move = random.choice(self.get_possible_moves(board, self.player_turn))
            return self.eval(board, self.player_turn), random_move

        best_value = float("-inf") if maximising else float("inf")
        oponent = 2 if self.player_turn == 1 else 2
        eval_player = self.player_turn if maximising else oponent
        moves = self.get_possible_moves(board, eval_player)
        
        for move in moves:
            # Move piece
            piece_value = board[move[0][1]][move[0][0]]
            board[move[0][1]][move[0][0]] = 0
            board[move[1][1]][move[1][0]] = piece_value

            # next_player = 2 if player_value == 1 else 2
            movement_value, _ = self.minimax(board, depth - 1, not maximising, alfa, beta)

            # Move the piece back
            board[move[0][1]][move[0][0]] = piece_value
            board[move[1][1]][move[1][0]] = 0

            if maximising and movement_value > best_value:
                best_move = move
                best_value = movement_value
                alfa = max(alfa, best_value)

            if not maximising and movement_value < best_value:
                best_move = move
                best_value = movement_value
                beta = min(beta, best_value)

            if (beta <= alfa):
                return best_value, best_move

        return best_value, best_move

    def eval(self, board, player_value):
        value = 0
        for y in range(len(board)):
            for x in range(len(board[y])):
                position = board[y][x]
                if int(position) == 1:
                    distances = [self.get_distance((x, y), go_to) for go_to in self.playerTwoCornerCamp if board[go_to[1]][go_to[0]] == 0]
                    # distances = []
                    # for go_to in self.playerTwoCornerCamp:
                    #     if board[go_to[1]][go_to[0]] == 0:
                    #         distances.append(self.get_distance((x, y), go_to))
                    value -= max(distances) if len(distances) else -50



                elif int(position) == 2:
                    distances = [self.get_distance((x, y), go_to) for go_to in self.playerOneCornerCamp if board[go_to[1]][go_to[0]] == 0]
                    value += max(distances) if len(distances) else -50

        if player_value == 2:
            value *= -1

        return value

    def get_distance(self, a, b):
        return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
        

    def get_possible_moves(self, board, player_turn):
        moves = []
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] != player_turn: continue

                actual_position = (x, y)
                cardinals_coords = self.get_cardinals_coords(actual_position)

                for cardinal in cardinals_coords:
                    if cardinals_coords[cardinal] and self.is_possible_movement(board, actual_position, cardinals_coords[cardinal]):
                        moves.append((actual_position, cardinals_coords[cardinal]))
        return moves

    def is_possible_movement(self, board, pfrom, to):
        coords = self.get_cardinals_coords(pfrom)
        n1, ne1, e1, se1, s1, so1, o1, no1 = coords["n1"], coords["ne1"], coords["e1"], coords["se1"], coords["s1"], coords["so1"], coords["o1"], coords["no1"]
        n2, ne2, e2, se2, s2, so2, o2, no2 = coords["n2"], coords["ne2"], coords["e2"], coords["se2"], coords["s2"], coords["so2"], coords["o2"], coords["no2"]

        if board[to[1]][to[0]] != 0:
            return False

        if to in [n1, ne1, e1, se1, s1, so1, o1, no1]:
            return True
        elif to in [n2, ne2, e2, se2, s2, so2, o2, no2]:
            if to == n2 and board[n1[1]][n1[0]] != 0:
                return True
            elif to == ne2 and board[ne1[1]][ne1[0]] != 0:
                return True
            elif to == e2 and board[e1[1]][e1[0]] != 0:
                return True
            elif to == se2 and board[se1[1]][se1[0]] != 0:
                return True
            elif to == s2 and board[s1[1]][s1[0]] != 0:
                return True
            elif to == so2 and board[so1[1]][so1[0]] != 0:
                return True
            elif to == o2 and board[o1[1]][o1[0]] != 0:
                return True
            elif to == no2 and board[no1[1]][no1[0]] != 0:
                return True
            else:
                return False
        return False

    def get_cardinals_coords(self, position):
        n1 = (position[0], position[1] - 1)
        n1 = None if n1[0] < 0 or n1[0] > 9 or n1[1] < 0 or n1[1] > 9 else n1
        ne1 = (position[0] + 1, position[1] - 1)
        ne1 = None if ne1[0] < 0 or ne1[0] > 9 or ne1[1] < 0 or ne1[1] > 9 else ne1
        e1 = (position[0] + 1, position[1])
        e1 = None if e1[0] < 0 or e1[0] > 9 or e1[1] < 0 or e1[1] > 9 else e1
        se1 = (position[0] + 1, position[1] + 1)
        se1 = None if se1[0] < 0 or se1[0] > 9 or se1[1] < 0 or se1[1] > 9 else se1
        s1 = (position[0], position[1] + 1)
        s1 = None if s1[0] < 0 or s1[0] > 9 or s1[1] < 0 or s1[1] > 9 else s1
        so1 = (position[0] - 1, position[1] + 1)
        so1 = None if so1[0] < 0 or so1[0] > 9 or so1[1] < 0 or so1[1] > 9 else so1
        o1 = (position[0] - 1, position[1])
        o1 = None if o1[0] < 0 or o1[0] > 9 or o1[1] < 0 or o1[1] > 9 else o1
        no1 = (position[0] - 1, position[1] - 1)
        no1 = None if no1[0] < 0 or no1[0] > 9 or no1[1] < 0 or no1[1] > 9 else no1
        n2 = (position[0], position[1] - 2)
        n2 = None if n2[0] < 0 or n2[0] > 9 or n2[1] < 0 or n2[1] > 9 else n2
        ne2 = (position[0] + 2, position[1] - 2)
        ne2 = None if ne2[0] < 0 or ne2[0] > 9 or ne2[1] < 0 or ne2[1] > 9 else ne2
        e2 = (position[0] + 2, position[1])
        e2 = None if e2[0] < 0 or e2[0] > 9 or e2[1] < 0 or e2[1] > 9 else e2
        se2 = (position[0] + 2, position[1] + 2)
        se2 = None if se2[0] < 0 or se2[0] > 9 or se2[1] < 0 or se2[1] > 9 else se2
        s2 = (position[0], position[1] + 2)
        s2 = None if s2[0] < 0 or s2[0] > 9 or s2[1] < 0 or s2[1] > 9 else s2
        so2 = (position[0] - 2, position[1] + 2)
        so2 = None if so2[0] < 0 or so2[0] > 9 or so2[1] < 0 or so2[1] > 9 else so2
        o2 = (position[0] - 2, position[1])
        o2 = None if o2[0] < 0 or o2[0] > 9 or o2[1] < 0 or o2[1] > 9 else o2
        no2 = (position[0] - 2, position[1] - 2)
        no2 = None if no2[0] < 0 or no2[0] > 9 or no2[1] < 0 or no2[1] > 9 else no2

        return {"n1": n1, "ne1": ne1, "e1": e1, "se1": se1, "s1": s1, "so1": so1, "o1": o1, "no1": no1, "n2": n2, "ne2": ne2, "e2": e2, "se2": se2, "s2": s2, "so2": so2, "o2": o2, "no2": no2}



Hoppers(True, True)

        
        
            

  







    