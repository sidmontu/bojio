import random, math
from math import sqrt, log

'''
Page 70 (R. Sutton Reinforcement Learning book)

Exercise 2.11: Make a figure analogous to Figure 2.6 for the nonstationary case
outlined in Exercise 2.5. Include the constant-step-size epsilon-greedy
algorithm with alpha = 0.1. Use runs of 200,000 steps and, as a performance
measure for each algorithm and parameter setting, use the average reward over
the last 100,000 steps.

'''

class StationaryEnvironmentModel :
    def __init__(self, k = 10) :
        self.qstar = [random.gauss(0,1) for _ in range(k)]
    def reward(self, action_idx) :
        return random.gauss(self.qstar[action_idx],1)

class NonstationaryEnvironmentModel :
    def __init__(self) :
        return

class EpsilonGreedy: 
    def __init__(self, epsilon = 0.1, k = 10, init_value = 0) :
        self.epsilon = epsilon
        self.k = k
        self.num_sel = [0] * k
        self.t = 0
        self.rewards = [init_value] * k
        self.rewards_total = [0] * k
        self.last_action = -1

    def get_action(self) :
        r = random.random()
        if self.t == 0 or r <= self.epsilon :
            self.last_action = random.randint(0,self.k-1) # return random action
        else :
            maxval = max(self.rewards)
            possible_actions = [idx for idx, val in enumerate(self.rewards) if val == maxval]
            self.last_action = random.sample(possible_actions, k = 1)[0]

        return self.last_action

    def register_reward(self, action_idx, reward) :
        self.rewards_total[action_idx] += reward
        self.num_sel[action_idx] += 1
        self.rewards[action_idx] = self.rewards_total[action_idx] / self.num_sel[action_idx]
        self.t += 1

class GradientBandit: 
    def __init__(self, alpha = 0.1, k = 10) :
        self.alpha = alpha
        self.k = k
        self.t = 0
        self.rewards_total = 0.
        self.h = [0.] * k
        self.pi_t = [1./k] * k

    def get_action(self) :
        return random.choices(list(range(self.k)), weights = self.pi_t)[0]

    def register_reward(self, action_idx, reward) :
        self.rewards_total += reward
        self.t += 1
        self.softmax()
        for i in range(self.k) :
            if i == action_idx :
                self.h[i] += self.alpha * (reward - (self.rewards_total/self.t)) * (1 - self.pi_t[i])
            else :
                self.h[i] -= self.alpha * (reward - (self.rewards_total/self.t)) * self.pi_t[i]
    def softmax(self) :
        denominator = sum([math.e**self.h[i] for i in range(self.k)])
        for idx in range(self.k) :
            numerator = math.e ** self.h[idx]
            self.pi_t[idx] = numerator / denominator

class UCB: 
    '''
    Q_(n+1) = Q_n + 1/N(A) * (R_n - Q_n)
    '''
    def __init__(self, c, init_value = 0, k = 10) :
        '''
        c > 0, controls degree of exploration
        '''
        self.last_action = -1
        self.k = k
        self.c = c
        self.t = 0
        self.rewards = [init_value] * k
        self.num_sel = [0] * k
        self.A = [100000] * k # arbitrarily large

    def get_action(self) :
        maxval = max(self.A)
        idxes = [x for x, val in enumerate(self.A) if val == maxval]
        self.last_action = random.sample(idxes, k = 1)[0]

        return self.last_action

    def register_reward(self, action_idx, reward) :
        self.num_sel[action_idx] += 1
        qnp1 = self.rewards[action_idx] + 1/self.num_sel[action_idx] * (reward - self.rewards[action_idx])
        self.rewards[action_idx] = qnp1
        self.t += 1

        self.A[action_idx] = self.rewards[action_idx] + self.c * sqrt(log(self.t)/self.num_sel[action_idx])

class Greedy: 
    def __init__(self, alpha = 0.1, init_value = 5, k = 10) :
        self.alpha = alpha
        self.last_action = -1
        self.k = k
        self.t = 0
        self.rewards = [init_value] * k

    def get_action(self) :
        if self.t == 0 :
            self.last_action = random.randint(0, self.k - 1)
        else :
            maxval = max(self.rewards)
            possible_actions = [idx for idx, val in enumerate(self.rewards) if val == maxval]
            self.last_action = random.sample(possible_actions, k = 1)[0]

        return self.last_action

    def register_reward(self, action_idx, reward) :
        qnp1 = self.rewards[action_idx] + self.alpha * (reward - self.rewards[action_idx])
        self.rewards[action_idx] = qnp1
        self.t += 1

def run_trial(Model, Agent, *args, num_trials = 2000, num_timesteps = 1000, avg_from = 0, avg_to = 1000) :

    avg_rewards = []

    for n in range(num_trials) :

        model = Model()
        agent = Agent(*args)

        rewards = []

        for i in range(num_timesteps) :

            action = agent.get_action()
            reward = model.reward(action)
            agent.register_reward(action, reward)
            rewards.append(reward)

        rewards = rewards[avg_from : avg_to]
        avg_reward = sum(rewards) / len(rewards)
        avg_rewards.append(avg_reward)

    return sum(avg_rewards)/num_trials

def main(k = 10, num_trials = 2000, num_timesteps = 1000) :

    s = 'method,power,value\n'
    # run 'epsilon-greedy' experiments
    for power in range(-7, -1, 1) :
        epsilon = 2**power
        v = run_trial(StationaryEnvironmentModel, EpsilonGreedy, epsilon, k, 0)
        print('[1/%d] q = %.3f' % (2**(abs(power)), v))
        s += str('epsilon-greedy,%d,%.3f\n' % (power,v))
            
    # run 'greedy' experiments
    for power in range(-2, 3, 1) :
        initialization = 2**power
        v = run_trial(StationaryEnvironmentModel, Greedy, 0.1, initialization, k)
        print('[%.3f] q = %.3f' % (2**(power), v))
        s += str('opt-greedy,%d,%.3f\n' % (power,v))

    # run 'UCB' experiments
    for power in range(-4, 3, 1) :
        c = 2**power
        v = run_trial(StationaryEnvironmentModel, UCB, c, 0, k)
        print('[%.3f] q = %.3f' % (2**(power), v))
        s += str('ucb,%d,%.3f\n' % (power,v))

    # run 'GradientBandit' experiments
    for power in range(-5, 3, 1) :
        alpha = 2**power
        v = run_trial(StationaryEnvironmentModel, GradientBandit, alpha, k)
        print('[%.3f] q = %.3f' % (2**(power), v))
        s += str('gradient-bandit,%d,%.3f\n' % (power,v))

    with open('stationary_results.csv', 'w') as fp :
        fp.write(s)

if __name__ == "__main__" :

    main(num_trials = 2)

