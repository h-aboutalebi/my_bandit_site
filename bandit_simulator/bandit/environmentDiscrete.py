# This is the environment class for discrete reward of bandit problem

import numpy as np


class environment():
    bernouli_distribution_arms = []  # This detrmines the expected reward of each arm. Arms are: [0, 1, ..., len(bernouli_distribution_arms)-1]

    def __init__(self, bernouli_distribution_arms, number_of_arms, number_of_steps):
        self.bernouli_distribution_arms = bernouli_distribution_arms
        self.number_of_arms = number_of_arms
        self.number_of_steps = number_of_steps

    # This function simulate the behaviour of the environment(the signal we get from arms by choosing them). Reward is either 0 or 1
    def environment_response(self, chosen_arm):
        index = np.random.uniform(0, 1)
        if (index <= self.bernouli_distribution_arms[chosen_arm]):
            return 1
        else:
            return 0

    # This function creates the corresponding matrix to make the rewards for a given environment at specific iteration. It has two indices [ arm_number,step_number].
    # This function is used to reduce the noise and lower the variance. It also makes the whole experiment more fair.
    def create_deterministic_rewrad_matrix(self):
        iteration_rewards = []
        for arm in range(self.number_of_arms):
            arm_rewards = []
            for step in range(self.number_of_steps):
                reward = self.environment_response(arm)
                arm_rewards.append(reward)
            iteration_rewards.append(arm_rewards)
        return iteration_rewards
