from functools import lru_cache
from MDP import MDP

size = 5
squareA = (0,1)
squareAp = (4,1)
squareB = (0,3)
squareBp = (2,3)
num_epochs = 100
squares = [[0 for _ in range(size)] for _ in range(size)]

@lru_cache(maxsize = None)
def run_trial(cur_sq, epoch, cur_total) :

    if epoch > num_epochs :
        return

    if cur_sq == squareA :
        avg_reward = 10
        squares[cur_sq[0]][cur_sq[1]] += avg_reward
        run_trial(squareAp, epoch+1)
    elif cur_sq == squareB :
        avg_reward = 5
        squares[cur_sq[0]][cur_sq[1]] += avg_reward
        run_trial(squareBp, epoch+1)
    else :
        r_left = 0 if cur_sq[1] - 1 >= 0 else -1
        r_right = 0 if cur_sq[1] + 1 < size else -1
        r_up = 0 if cur_sq[0] - 1 >= 0 else -1
        r_down = 0 if cur_sq[0] + 1 < size else -1
        avg_reward = (r_left + r_right + r_up + r_down) / 4
        squares[cur_sq[0]][cur_sq[1]] += avg_reward
        if cur_sq[1] - 1 >= 0 :
            run_trial((cur_sq[0],cur_sq[1]-1), epoch+1)
        if cur_sq[1] + 1 < size :
            run_trial((cur_sq[0],cur_sq[1]+1), epoch+1)
        if cur_sq[0] - 1 >= 0 :
            run_trial((cur_sq[0]-1,cur_sq[1]), epoch+1)
        if cur_sq[0] + 1 < size :
            run_trial((cur_sq[0]+1,cur_sq[1]), epoch+1)

def run_experiment() :
    start_sq = (0,0)
    run_trial(start_sq, 0)
    for i in range(size) :
        for j in range(size) :
            print('%5s\t' % (str('%.1f' % (squares[i][j]))), end = '')
        print('')

if __name__ == "__main__" :
    run_experiment()



