from hoppers import *

hoppers = Hoppers(True, True, 1, 2)
hoppers2 = Hoppers(True, True, 1, 2)

hoppers.board()

playerTurn = 1
move = None
while not hoppers.check_if_there_is_winner(hoppers.current_state):
    if playerTurn == 1:
        print("Jugador 1: ")
        move = hoppers.playAIbot(move)
        playerTurn = 2
    else:
        print("Jugador 2: ")
        move = hoppers2.playAIbot(move)
        playerTurn = 1

    hoppers.next_turn()
    hoppers2.next_turn()
    hoppers.board()