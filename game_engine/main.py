from os import makedirs
from src.Game import StandardGame

def main() :
    game = StandardGame()
    makedirs('out_files', exist_ok = True)
    game.print_game_state('white', out_file = 'out_files/move_000.jpg')
    for i in range(1,201) :
        game.tick()
        game.print_game_state('white', out_file = str('out_files/move_%03d.jpg' % (i)))

if __name__ == "__main__" :
    main()

