import random, math, time
from math import sqrt, log


class StationaryEnvironmentModel:
    def __init__(self, k=10):
        self.qstar = [random.gauss(0, 1) for _ in range(k)]

    def reward(self, action_idx):
        return random.gauss(self.qstar[action_idx], 1)


class NonStationaryEnvironmentModel:
    def __init__(self, k=10):
        random_init = random.gauss(0, 1)
        self.qstar = [random_init] * k

    def reward(self, action_idx):

        # return reward with current qstars, mean qstar[action_idx] and variance 1
        return_reward = random.gauss(self.qstar[action_idx], 1)

        # update each qstar with a random walk, mean 0 sd 0.01
        self.qstar = [v + random.gauss(0, 0.01) for v in self.qstar]

        return return_reward

    def return_qstars(self):
        """
        Return qstars at current timestep (for debugging purposes)
        """
        return self.qstar


class EpsilonGreedy:
    def __init__(self, epsilon=0.1, k=10, init_value=0):
        self.t0 = True
        self.epsilon = epsilon
        self.k = k
        self.qn = [init_value] * k
        self.num_sel = [0] * k
        self.rewards_total = [0] * k

    def get_action(self):
        r = random.random()
        if self.t0 or r <= self.epsilon:
            action = random.randint(0, self.k - 1)  # return random action
            self.t0 = False
        else:
            maxval = max(self.qn)
            possible_actions = [idx for idx, val in enumerate(self.qn) if val == maxval]
            action = random.sample(possible_actions, k=1)[0]

        return action

    def register_reward(self, action_idx, reward):
        self.rewards_total[action_idx] += reward
        self.num_sel[action_idx] += 1
        self.qn[action_idx] = self.rewards_total[action_idx] / self.num_sel[action_idx]


class GreedyNonStationary:
    def __init__(self, alpha=0.1, init_value=5, k=10):
        self.alpha = alpha
        self.k = k
        self.t0 = True
        self.qn = [init_value] * k

    def get_action(self):
        if self.t0:
            action = random.randint(0, self.k - 1)
            self.t0 = False
        else:
            maxval = max(self.qn)
            possible_actions = [idx for idx, val in enumerate(self.qn) if val == maxval]
            action = random.sample(possible_actions, k=1)[0]

        return action

    def register_reward(self, action_idx, reward):
        self.qn[action_idx] = self.qn[action_idx] + self.alpha * (
            reward - self.qn[action_idx]
        )


class GradientBandit:
    def __init__(self, alpha=0.1, k=10):
        self.alpha = alpha
        self.k = k
        self.t = 0
        self.rewards_total = 0.0
        self.h = [0.0] * k
        self.pi_t = [1.0 / k] * k

    def get_action(self):
        return random.choices(list(range(self.k)), weights=self.pi_t)[0]

    def register_reward(self, action_idx, reward):
        self.rewards_total += reward
        self.t += 1
        self.softmax()
        average_reward = self.rewards_total / self.t
        for i in range(self.k):
            if i == action_idx:
                self.h[i] += self.alpha * (reward - average_reward) * (1 - self.pi_t[i])
            else:
                self.h[i] -= self.alpha * (reward - average_reward) * self.pi_t[i]

    def softmax(self):
        denominator = sum([math.e ** self.h[i] for i in range(self.k)])
        for idx in range(self.k):
            numerator = math.e ** self.h[idx]
            self.pi_t[idx] = numerator / denominator


class UCB:
    """ """

    def __init__(self, c, init_value=0, k=10):
        """
        c is > 0, and controls degree of exploration
        """
        self.k = k
        self.c = c
        self.t = 0
        self.last_reward = [init_value] * k
        self.num_sel = [0] * k
        self.A = [
            100000
        ] * k  # arbitrarily large action optimality estimate, encourages exploration

    def get_action(self):

        # find max value in action optimality array
        maxval = max(self.A)

        # in case there are multiple actions with same maxval, choose randomly among them
        idxes = [x for x, val in enumerate(self.A) if val == maxval]
        return random.sample(idxes, k=1)[0]

    def register_reward(self, action_idx, reward):

        # update counters
        self.num_sel[action_idx] += 1
        self.t += 1

        # compute Q_(n+1) = Q_n + 1/N(A) * (R_n - Q_n)
        qnp1 = self.last_reward[action_idx] + 1 / self.num_sel[action_idx] * (
            reward - self.last_reward[action_idx]
        )
        self.last_reward[action_idx] = qnp1

        # update action optimality estimates
        self.A[action_idx] = qnp1 + self.c * sqrt(
            log(self.t) / self.num_sel[action_idx]
        )


def run_trial(
    Model, Agent, *args, num_trials=2000, num_timesteps=1000, avg_from=0, avg_to=1000
):

    avg_rewards = []

    start = time.time()
    for n in range(num_trials):

        model = Model()
        agent = Agent(*args)

        rewards = []

        for i in range(num_timesteps):

            action = agent.get_action()
            reward = model.reward(action)
            agent.register_reward(action, reward)
            rewards.append(reward)

        rewards = rewards[avg_from:avg_to]
        avg_reward = sum(rewards) / len(rewards)
        avg_rewards.append(avg_reward)

        if n > 0 and n % 10 == 0:
            rtime = time.time() - start
            remaining = (num_trials - n) * rtime / 10 / 60
            print(
                "\t--> Completed %d trials, runtime = %.3f, estimated remaining time = %.3f mins"
                % (n, rtime, remaining)
            )
            start = time.time()

    return sum(avg_rewards) / num_trials


def test_stationary_cases(k=10):
    """
    K-armed bandit tested on the stationary environment case

    This re-creates the Figure 2.6 found on page 42 of Richard Sutton's
    Reinforcement Learning (2nd edition) textbook.
    """

    s = "method,power,value\n"
    # run 'epsilon-greedy' experiments
    for power in range(-7, -1, 1):
        epsilon = 2 ** power
        v = run_trial(StationaryEnvironmentModel, EpsilonGreedy, epsilon, k, 0)
        print(
            "[Episilon-Greedy, epsilon = 1/%d] Average Reward = %.3f"
            % (2 ** (abs(power)), v)
        )
        s += str("epsilon-greedy,%d,%.3f\n" % (power, v))

    # run 'optimistic-greedy' experiments
    for power in range(-2, 3, 1):
        initialization = 2 ** power
        v = run_trial(
            StationaryEnvironmentModel, GreedyNonStationary, 0.1, initialization, k
        )
        print(
            "[Optimistic-Greedy, initialization = %.5f] Average Reward = %.3f"
            % (initialization, v)
        )
        s += str("opt-greedy,%d,%.3f\n" % (power, v))

    # run 'UCB' experiments
    for power in range(-4, 3, 1):
        c = 2 ** power
        v = run_trial(StationaryEnvironmentModel, UCB, c, 0, k)
        print("[UCB, c = %.5f] Average Reward = %.3f" % (c, v))
        s += str("ucb,%d,%.3f\n" % (power, v))

    # run 'GradientBandit' experiments
    for power in range(-5, 3, 1):
        alpha = 2 ** power
        v = run_trial(StationaryEnvironmentModel, GradientBandit, alpha, k)
        print("[Gradient Bandit, alpha = %.5f] Average Reward = %.3f" % (alpha, v))
        s += str("gradient-bandit,%d,%.3f\n" % (power, v))

    with open("stationary_results.csv", "w") as fp:
        fp.write(s)


def test_nonstationary_cases(k=10):
    """
    K-armed bandit tested on the non-stationary environment case

    This is Exercise 2.11 on page 44 of R. Sutton Reinforcement Learning (2nd
    Edition) book.

    Exercise 2.11: Make a figure analogous to Figure 2.6 for the nonstationary case
    outlined in Exercise 2.5. Include the constant-step-size epsilon-greedy
    algorithm with alpha = 0.1. Use runs of 200,000 steps and, as a performance
    measure for each algorithm and parameter setting, use the average reward over
    the last 100,000 steps.
    """

    s = "method,power,value\n"
    # run 'epsilon-greedy' experiments
    for power in range(-7, -1, 1):
        epsilon = 2 ** power
        v = run_trial(
            NonStationaryEnvironmentModel,
            EpsilonGreedy,
            epsilon,
            k,
            0,
            num_trials=100,
            num_timesteps=200000,
            avg_from=100000,
            avg_to=200000,
        )
        print(
            "[Episilon-Greedy, epsilon = 1/%d] Average Reward = %.3f"
            % (2 ** (abs(power)), v)
        )
        s += str("epsilon-greedy,%d,%.3f\n" % (power, v))

    # run 'optimistic-greedy' experiments
    for power in range(-2, 3, 1):
        initialization = 2 ** power
        v = run_trial(
            NonStationaryEnvironmentModel,
            GreedyNonStationary,
            0.1,
            initialization,
            k,
            num_trials=100,
            num_timesteps=200000,
            avg_from=100000,
            avg_to=200000,
        )
        print(
            "[Optimistic-Greedy, initialization = %.5f] Average Reward = %.3f"
            % (initialization, v)
        )
        s += str("opt-greedy,%d,%.3f\n" % (power, v))

    # run 'UCB' experiments
    for power in range(-4, 3, 1):
        c = 2 ** power
        v = run_trial(
            NonStationaryEnvironmentModel,
            UCB,
            c,
            0,
            k,
            num_trials=100,
            num_timesteps=200000,
            avg_from=100000,
            avg_to=200000,
        )
        print("[UCB, c = %.5f] Average Reward = %.3f" % (c, v))
        s += str("ucb,%d,%.3f\n" % (power, v))

    # run 'GradientBandit' experiments
    for power in range(-5, 3, 1):
        alpha = 2 ** power
        v = run_trial(
            NonStationaryEnvironmentModel,
            GradientBandit,
            alpha,
            k,
            num_trials=100,
            num_timesteps=200000,
            avg_from=100000,
            avg_to=200000,
        )
        print("[Gradient Bandit, alpha = %.5f] Average Reward = %.3f" % (alpha, v))
        s += str("gradient-bandit,%d,%.3f\n" % (power, v))

    with open("nonstationary_results.csv", "w") as fp:
        fp.write(s)


def main():
    test_stationary_cases()
    test_nonstationary_cases()


if __name__ == "__main__":
    main()
