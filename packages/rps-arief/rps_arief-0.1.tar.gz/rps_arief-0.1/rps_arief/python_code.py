import random

moves = ["rock", "paper", "scissors"]

class Player():
    def __init__(self):
        self.count = 0
        self.score = 0

    def play(self):
        return moves[0]

    def learn(self, last_opponent_move):
        pass


class RandomPlayer(Player):
    def play(self):
        i = random.randint(0, 2)
        return moves[i]


class CyclePlayer(Player):
    def play(self):
        i = self.count % 3
        self.count += 1
        return moves[i]


class ReflectPlayer(Player):
    def __init__(self):
        Player.__init__(self)
        self.last_opponent_move = None

    def play(self):
        if self.last_opponent_move is None:
            return Player.play(self)
        return self.last_opponent_move

    def learn(self, last_opponent_move):
        self.last_opponent_move = last_opponent_move


class HumanPlayer(Player):
    def play(self):
        player_move = input("Rock, paper, scissors? ")
        player_move = player_move.lower()
        while player_move not in moves:
            player_move = input("Invalid move, check your spelling! "
                                + "Try again. ")
        return player_move


class Game():
    def __init__(self):
        self.player1 = HumanPlayer()
        self.player2 = RandomPlayer()

    def play_round(self):
        player1_move = self.player1.play()
        player2_move = self.player2.play()

        self.player2.learn(player1_move)
        self.player1.learn(player2_move)

        print("Player 1 plays '" + player1_move + "' and Player 2 plays '" +
              player2_move + "'")

        if player1_move == player2_move:
            print("It's a Tie!")
        elif player1_move == "rock":
            if player2_move == "paper":
                print("Player 2 wins!!")
                self.player2.score += 1
            else:
                print("Player 1 wins!!")
                self.player1.score += 1
        elif player1_move == "paper":
            if player2_move == "scissors":
                print("Player 2 wins!!")
                self.player2.score += 1
            else:
                print("Player 1 wins!!")
                self.player1.score += 1
        else:
            if player2_move == "rock":
                print("Player 2 wins!!")
                self.player2.score += 1
            else:
                print("Player 1 wins!!")
                self.player1.score += 1

    def play_game(self):
        while True:
            no_round = 0
            self.player1.score = 0
            self.player2.score = 0
            option = input("Play a game? Press enter to continue." +
                           " Enter q to quit ")
            option = option.lower()
            print("")
            if option == "q":
                print("Goodbye!!!")
                break
            else:
                for round in range(3):
                    no_round += 1
                    print("ROUND " + str(no_round))
                    self.play_round()
                    print("Player 1: " + str(self.player1.score))
                    print("Player 2: " + str(self.player2.score))
                    print("")
                print("** FINAL SCORE **")
                print("Player 1: " + str(self.player1.score))
                print("Player 2: " + str(self.player2.score))
                if self.player1.score > self.player2.score:
                    print("** PLAYER 1 WINS THE GAME! **")
                elif self.player1.score < self.player2.score:
                    print("** PLAYER 2 WINS THE GAME! **")
                else:
                    print("** THE GAME IS A DRAW! **")
                print("")

        input("Press Enter to Exit")


if __name__ == "__main__":
    game = Game()
    game.play_game()
