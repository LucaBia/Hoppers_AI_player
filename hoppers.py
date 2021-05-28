# Gian Luca Rivera - 18049

from prettytable import PrettyTable
import numpy
import xmltodict
import json


class Hoppers(object):
    def __init__(self, playerOneIsBot=False, playerTwoIsBot=False, bot1Level=1, bot2Level=1):
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
        self.bot1Level = bot1Level
        self.bot2Level = bot2Level
        self.winner = None

        self.lastMovePiece = None
        self.lastMoveCoords = None

        # Lista de coordenadas en donde estan las piezas de los jugadores
        self.playerOneCornerCamp = []
        self.playerTwoCornerCamp = []
        self.corner_camps()

    def board(self):
        board = PrettyTable()
        board.hrules = 1
        board.header = False
        board.add_rows(self.current_state)
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
        if self.player_turn == 1:
            self.player_turn = 2
        else:
            self.player_turn = 1

    def check_if_there_is_winner(self, board):
        p1v = [self.current_state[position[1]][position[0]] for position in self.playerOneCornerCamp]
        p2v = [self.current_state[position[1]][position[0]] for position in self.playerTwoCornerCamp]
        # print("P1V: ", p1v)
        # print("P2V: ", p2v)

        if 1 in p2v and 0 not in p2v:
            self.winner = "El jugador 1 ha ganado"
            return True
        if 2 in p1v and 0 not in p1v:
            self.winner = "El jugador 2 ha ganado"
            return True

        return False

    def toTuple(self, pinput):
        x, y = pinput.split(",")
        x, y = int(x), int(y)
        return (x, y)

    def move_piece(self, from_, to, player):
        from_ = self.toTuple(from_)
        to = self.toTuple(to)
        self.current_state[from_[1]][from_[0]] = 0
        self.current_state[to[1]][to[0]] = player

    def game(self):
        self.board()

        while not self.check_if_there_is_winner(self.current_state):
            if self.player_turn == self.playerOne:
                print("Jugador 1: ")
            else:
                print("Jugador 2: ")

            if (self.player_turn == 1 and self.playerOneIsBot) or (self.player_turn == 2 and self.playerTwoIsBot) :
                rival_move_xml = None

                # player_piece_move, player_coords_move = self.playAIBot(self.bot1Level)
                if self.lastMovePiece and self.lastMoveCoords:
                    xml = {
                        'move': {
                            'from': {
                                '@row': self.lastMovePiece[0],
                                '@col': self.lastMovePiece[1]
                            },
                            'to': {
                                '@row': self.lastMoveCoords[0],
                                '@col': self.lastMoveCoords[1]
                            },
                            'path': {
                                'pos': []
                            }
                        }
                    }
                    rival_move_xml = xmltodict.unparse(xml, pretty = True, short_empty_elements=True)

                self.playAIBot(rival_move_xml)
            else:
                player_piece_move = input("Ingrese las coordenadas (x,y) de la pieza a mover: ")
                player_coords_move = input("Ingrese las coordenadas (x,y) donde desea mover: ")
                self.move_piece(player_piece_move, player_coords_move, self.player_turn)

            self.next_turn()
            self.board()
        print(self.winner)

    # From here minimax functions begin
    def hypotenuse (self, a, b):
        return numpy.hypot((a[0]-b[0]),(a[1]-b[1]))

    def heuristic(self, board, player_turn):
        value = 0
        for y in range(len(board)):
            for x in range(len(board[y])):
                position = board[y][x]
                if int(position) == 1:
                    distances = []
                    for go_to in self.playerTwoCornerCamp:
                        if board[go_to[1]][go_to[0]] == 0:
                            distances.append(self.hypotenuse((x, y), go_to))
                    value -= max(distances) if len(distances) else -50
                elif int(position) == 2:
                    distances = []
                    for go_to in self.playerOneCornerCamp:
                        if board[go_to[1]][go_to[0]] == 0:
                            distances.append(self.hypotenuse((x, y), go_to))
                    value += max(distances) if len(distances) else -50
        if player_turn == 2:
            value *= -1

        return value

    def cardinals_points(self, position):
        n1 = (position[0], position[1] - 1)
        if n1[0] < 0 or n1[0] > 9 or n1[1] < 0 or n1[1] > 9:
            n1 = None

        ne1 = (position[0] + 1, position[1] - 1)
        if ne1[0] < 0 or ne1[0] > 9 or ne1[1] < 0 or ne1[1] > 9:
            ne1 = None

        e1 = (position[0] + 1, position[1])
        if e1[0] < 0 or e1[0] > 9 or e1[1] < 0 or e1[1] > 9:
            e1 = None

        se1 = (position[0] + 1, position[1] + 1)
        if se1[0] < 0 or se1[0] > 9 or se1[1] < 0 or se1[1] > 9:
            se1 = None

        s1 = (position[0], position[1] + 1)
        if s1[0] < 0 or s1[0] > 9 or s1[1] < 0 or s1[1] > 9:
            s1 = None

        so1 = (position[0] - 1, position[1] + 1)
        if so1[0] < 0 or so1[0] > 9 or so1[1] < 0 or so1[1] > 9:
            so1 = None

        o1 = (position[0] - 1, position[1])
        if o1[0] < 0 or o1[0] > 9 or o1[1] < 0 or o1[1] > 9:
            o1 = None

        no1 = (position[0] - 1, position[1] - 1)
        if no1[0] < 0 or no1[0] > 9 or no1[1] < 0 or no1[1] > 9:
            no1 = None

        n2 = (position[0], position[1] - 2)
        if n2[0] < 0 or n2[0] > 9 or n2[1] < 0 or n2[1] > 9:
            n2 = None

        ne2 = (position[0] + 2, position[1] - 2)
        if ne2[0] < 0 or ne2[0] > 9 or ne2[1] < 0 or ne2[1] > 9:
            ne2 = None

        e2 = (position[0] + 2, position[1])
        if e2[0] < 0 or e2[0] > 9 or e2[1] < 0 or e2[1] > 9:
            e2 = None

        se2 = (position[0] + 2, position[1] + 2)
        if se2[0] < 0 or se2[0] > 9 or se2[1] < 0 or se2[1] > 9:
            se2 = None

        s2 = (position[0], position[1] + 2)
        if s2[0] < 0 or s2[0] > 9 or s2[1] < 0 or s2[1] > 9:
            s2 = None

        so2 = (position[0] - 2, position[1] + 2)
        if so2[0] < 0 or so2[0] > 9 or so2[1] < 0 or so2[1] > 9:
            so2 = None

        o2 = (position[0] - 2, position[1])
        if o2[0] < 0 or o2[0] > 9 or o2[1] < 0 or o2[1] > 9:
            o2 = None

        no2 = (position[0] - 2, position[1] - 2)
        if no2[0] < 0 or no2[0] > 9 or no2[1] < 0 or no2[1] > 9:
            no2 = None

        return (n1, ne1, e1, se1, s1, so1, o1, no1, n2, ne2, e2, se2, s2, so2, o2, no2)

    def jumps(self, board, position):
        cardinals = self.cardinals_points(position)
        n1, ne1, e1, se1, s1, so1, o1, no1 = cardinals[0], cardinals[1], cardinals[2], cardinals[3], cardinals[4], cardinals[5], cardinals[6], cardinals[7]
        n2, ne2, e2, se2, s2, so2, o2, no2 = cardinals[8], cardinals[9], cardinals[10], cardinals[11], cardinals[12], cardinals[13], cardinals[14], cardinals[15]

        for coord in [n1, ne1, e1, se1, s1, so1, o1, no1]:
            if  coord:
                if board[coord[1]][coord[0]] != 0:
                    if coord == n1 and n2 and board[n2[1]][n2[0]] == 0:
                        return True
                    elif coord == ne1 and ne2 and board[ne2[1]][ne2[0]] == 0:
                        return True
                    elif coord == e1 and e2 and board[e2[1]][e2[0]] == 0:
                        return True
                    elif coord == se1 and se2 and board[se2[1]][se2[0]] == 0:
                        return True
                    elif coord == s1 and s2 and board[s2[1]][s2[0]] == 0:
                        return True
                    elif coord == so1 and so2 and board[so2[1]][so2[0]] == 0:
                        return True
                    elif coord == o1 and o2 and board[o2[1]][o2[0]] == 0:
                        return True
                    elif coord == no1 and no2 and board[no2[1]][no2[0]] == 0:
                        return True
        return False

    def can_make_movement(self, board, from_, to):
        cardinals = self.cardinals_points(from_)
        n1, ne1, e1, se1, s1, so1, o1, no1 = cardinals[0], cardinals[1], cardinals[2], cardinals[3], cardinals[4], cardinals[5], cardinals[6], cardinals[7]
        n2, ne2, e2, se2, s2, so2, o2, no2 = cardinals[8], cardinals[9], cardinals[10], cardinals[11], cardinals[12], cardinals[13], cardinals[14], cardinals[15]


        if board[to[1]][to[0]] != 0:
            return False, 0

        if to in [n1, ne1, e1, se1, s1, so1, o1, no1]:
            return True, 1
        elif to in [n2, ne2, e2, se2, s2, so2, o2, no2]:
            if to == n2 and board[n1[1]][n1[0]] != 0:
                return True, 2
            elif to == ne2 and board[ne1[1]][ne1[0]] != 0:
                return True, 2
            elif to == e2 and board[e1[1]][e1[0]] != 0:
                return True, 2
            elif to == se2 and board[se1[1]][se1[0]] != 0:
                return True, 2
            elif to == s2 and board[s1[1]][s1[0]] != 0:
                return True, 2
            elif to == so2 and board[so1[1]][so1[0]] != 0:
                return True, 2
            elif to == o2 and board[o1[1]][o1[0]] != 0:
                return True, 2
            elif to == no2 and board[no1[1]][no1[0]] != 0:
                return True, 2
            else:
                return False, 0

        return False, 0

    def all_moves(self, board, player_turn, all_moves = []):
        moves = []
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x] == player_turn:
                    actual_position = (x, y)
                    cardinals = self.cardinals_points(actual_position)

                    for cardinal in cardinals:
                        if cardinal:
                            booln, n = self.can_make_movement(board, actual_position, cardinal)
                            if booln:
                                moves.append((actual_position, cardinal, n, [actual_position, cardinal]))

        for move in moves:
            if move not in all_moves:
                all_moves.append(move)
                board[move[0][1]][move[0][0]] = 0
                board[move[1][1]][move[1][0]] = player_turn

                if n == 2 and self.jumps(board, move[1]):
                    next_moves = self.all_moves(board, player_turn, all_moves)
                    for next_move in next_moves:
                        if next_move not in moves:
                            if move[0] != next_move[1]:
                                if next_move[2] == 2 and move[2] == 2:
                                    # print("----------PATH DE 3------------")
                                    # print(move[0], next_move[1], 0, [move[0], next_move[0], next_move[1]])
                                    moves.append((move[0], next_move[1], 0, [move[0], next_move[0], next_move[1]]))

                board[move[0][1]][move[0][0]] = player_turn
                board[move[1][1]][move[1][0]] = 0

        return moves

    def minimax(self, board, depth, player_turn, alfa=float("-inf"), beta=float("inf")):
        if self.check_if_there_is_winner(board) or depth == 0:
            return self.heuristic(board, self.player_turn), None

        if player_turn == self.player_turn:
            best_value = float("-inf")
        else:
            best_value = float("inf")

        if self.player_turn == 1:
            opponent = 2
        else:
            opponent = 1

        if player_turn == self.player_turn:
            eval_player = self.player_turn
        else:
            eval_player = opponent

        moves = self.all_moves(board, eval_player)
        for move in moves:
            piece = board[move[0][1]][move[0][0]]
            board[move[0][1]][move[0][0]] = 0
            board[move[1][1]][move[1][0]] = piece
            movement_value, _ = self.minimax(board, depth - 1, opponent, alfa, beta)
            board[move[0][1]][move[0][0]] = piece
            board[move[1][1]][move[1][0]] = 0

            if player_turn == self.player_turn:
                if movement_value > best_value:
                    best_move = move
                    best_value = movement_value
                    alfa = max(alfa, best_value)

            if not player_turn == self.player_turn:
                if movement_value < best_value:
                    best_move = move
                    best_value = movement_value
                    beta = min(beta, best_value)

            if (player_turn == self.player_turn and alfa > beta) or (not player_turn == self.player_turn and alfa < beta):
                return best_value, best_move

        return best_value, best_move

    def playAIBot(self, moveXML):
        if (self.player_turn == self.playerOne):
            botLevel = self.bot1Level
        else:
            botLevel = self.bot2Level

        if (moveXML):
            move = json.loads(json.dumps(dict(xmltodict.parse(moveXML, process_namespaces=True))))
            x_ppm = move['move']['from']['@row']
            y_ppm = move['move']['from']['@col']
            player_piece_move = "" + x_ppm + "," + y_ppm

            x_pcm = move['move']['to']['@row']
            y_pcm = move['move']['to']['@col']
            player_coords_move = "" + x_pcm + "," + y_pcm

            if (player_piece_move and player_coords_move):
                if (self.player_turn == 1):
                    rival = 2
                else:
                    rival = 1
                self.move_piece(player_piece_move, player_coords_move, rival)
                self.lastMovePiece = None
                self.lastMoveCoords = None

        _, best_move = self.minimax(self.current_state, botLevel, self.player_turn)

        move_from = "{x},{y}".format(x=best_move[0][0], y=best_move[0][1])
        move_to = "{x},{y}".format(x=best_move[1][0], y=best_move[1][1])

        self.move_piece(move_from, move_to, self.player_turn)

        paths = []
        for position in best_move[3]:
            paths.append({
                '@row': position[0],
                '@col': position[1]
            })

        xml = {
            'move': {
                'from': {
                    '@row': best_move[0][0],
                    '@col': best_move[0][1]
                },
                'to': {
                    '@row': best_move[1][0],
                    '@col': best_move[1][1]
                },
                'path': {
                    'pos': paths
                }
            }
        }
        print(xmltodict.unparse(xml, pretty = True, short_empty_elements=True))
        return xmltodict.unparse(xml, pretty = True)
