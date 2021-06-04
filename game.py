from hoppers import *

# AI vs Jugador
# hoppers = Hoppers(True, False, 3, None)
# hoppers.game()

# AI vs AI
hoppers = Hoppers(True, True, 1, None)
hoppers2 = Hoppers(True, True, None, 2)

hoppers.board()

playerTurn = 1
move = None
while not hoppers.check_if_there_is_winner(hoppers.current_state):
    if playerTurn == 1:
        print("Jugador 1: ")
        move = hoppers.playAIBot(move)
        # move2 = hoppers2.playAIBot(move)
        playerTurn = 2
    else:
        print("Jugador 2: ")
        # move = hoppers.playAIBot(move)
        move = hoppers2.playAIBot(move)
        playerTurn = 1

    hoppers.next_turn()
    hoppers2.next_turn()
    hoppers.board()
print(hoppers.winner)
