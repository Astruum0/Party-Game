from Class import Board, Player
from IA import IA
from random import randint

player = Player()
bot = IA(Player())
finished = False
while not(finished):
    print("======Player Turn======")
    player.SendHit(int(input("x ? "))-1, int(input("y ? "))-1, bot)
    print(player.attack_board.board)
    print("\n\n======Bot Turn======")
    coo = bot.seach_best_move()
    win = bot.Player.SendHit(coo[0], coo[1], player)
    print(bot.Player.attack_board.board)
    if win:
        finished = True

