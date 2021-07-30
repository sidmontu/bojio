################################################################################
#################### DEPRECATED CODE (Incorrect interpretation) ################
################################################################################

from functools import lru_cache

size = 5
squareA = (0, 1)
squareAp = (4, 1)
squareB = (0, 3)
squareBp = (2, 3)
num_epochs = 100
squares = [[0 for _ in range(size)] for _ in range(size)]


@lru_cache(maxsize=None)
def run_trial(cur_sq, epoch, cur_total):

    if epoch > num_epochs:
        return

    if cur_sq == squareA:
        avg_reward = 10
        squares[cur_sq[0]][cur_sq[1]] += avg_reward
        run_trial(squareAp, epoch + 1)
    elif cur_sq == squareB:
        avg_reward = 5
        squares[cur_sq[0]][cur_sq[1]] += avg_reward
        run_trial(squareBp, epoch + 1)
    else:
        r_left = 0 if cur_sq[1] - 1 >= 0 else -1
        r_right = 0 if cur_sq[1] + 1 < size else -1
        r_up = 0 if cur_sq[0] - 1 >= 0 else -1
        r_down = 0 if cur_sq[0] + 1 < size else -1
        avg_reward = (r_left + r_right + r_up + r_down) / 4
        squares[cur_sq[0]][cur_sq[1]] += avg_reward
        if cur_sq[1] - 1 >= 0:
            run_trial((cur_sq[0], cur_sq[1] - 1), epoch + 1)
        if cur_sq[1] + 1 < size:
            run_trial((cur_sq[0], cur_sq[1] + 1), epoch + 1)
        if cur_sq[0] - 1 >= 0:
            run_trial((cur_sq[0] - 1, cur_sq[1]), epoch + 1)
        if cur_sq[0] + 1 < size:
            run_trial((cur_sq[0] + 1, cur_sq[1]), epoch + 1)


def run_experiment():
    start_sq = (0, 0)
    run_trial(start_sq, 0)
    for i in range(size):
        for j in range(size):
            print("%5s\t" % (str("%.1f" % (squares[i][j]))), end="")
        print("")


################################################################################
################################################################################
################################################################################

from MDP import MDP
from collections import defaultdict


class GridWorld(MDP):
    def __init__(self, n: int, s0: tuple[int, int], rules: dict):
        self.n = n
        self.s0 = s0
        self.states = [(x, y) for x in range(n) for y in range(n)]
        self.rules = rules

    def getStates(self):
        return self.states

    def getStartState(self):
        return self.s0

    def getTransitionStatesAndProbs(self, state, action):
        x, y = state
        p = 1 / 4  # can go in any of 4 directions with equal probability
        if action == "west":
            to_x, to_y = x - 1, y
        elif action == "east":
            to_x, to_y = x + 1, y
        elif action == "north":
            to_x, to_y = x, y - 1
        elif action == "south":
            to_x, to_y = x, y + 1
        elif action == "jump":
            to_x, to_y = self.rules[state]["moveTo"]
            p = 1.0

        if to_x < 0 or to_x >= self.n or to_y < 0 or to_y >= self.n:  # illegal move
            if self.rules["illegal"]["moveTo"]:
                to_x, to_y = self.rules["illegal"]["moveTo"]
            else:
                to_x, to_y = state  # stay in current state

        return [(to_x, to_y), p]

    def getReward(self, state, action, nextState):
        if state in self.rules:
            assert (
                nextState == self.rules[state]["moveTo"]
            ), "Error: Rule violated from state {} to {} (expected {})".format(
                state, nextState, self.rules[state]["moveTo"]
            )
            return self.rules[state]["reward"]

        if state == nextState:  # must have been an illegal move
            return self.rules["illegal"]["reward"]

        return self.rules["legal"]["reward"]

    def isTerminal(self, state):
        return False  # no end state

    def getPossibleActions(self, state):
        if state in self.rules:
            return ["jump"]

        # in current state, there are only 4 possible actions at most
        return ["west", "east", "north", "south"]


if __name__ == "__main__":

    rules = {
        "(0,1)": {"moveTo": (4, 1), "reward": 10},  # A
        "(0,3)": {"moveTo": (2, 3), "reward": 5},  # B
        "legal": {"moveTo": None, "reward": 0},  # remaining legal moves
        "illegal": {  # illegal moves (e.g. moving out of the grid)
            "moveTo": None,
            "reward": -1,
        },
    }

    n = 5  # 5x5 gridworld
    gw = GridWorld(n=n, s0=(0, 0), rules=rules)

    # calculate values for gridworld
    iterations = 1000
    discount = 0.9
    values = dict(zip(gw.getStates(), [0.0] * (n * n)))
    for i in range(iterations):
        v = values.copy()
        for state in gw.getStates():
            action_values = defaultdict(float)
            for action in gw.getPossibleActions(state):
                for next_state, prob in gw.getTransitionStatesAndProbs(state, action):
                    print("state = {}, next_state = {}".format(state, next_state))
                    action_values[action] += prob * (
                        gw.getReward(state, action, next_state)
                        + discount * v[next_state]
                    )
            values[state] = action_values[action_values.argMax()]

    print(values)
