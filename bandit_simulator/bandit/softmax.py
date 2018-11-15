# This class implements the softmax algorithm
# for alpha here we have used the expected reward estimate

from bandit_simulator.bandit.MainDiscreteSetting import *
import copy
import numpy as np
import math


class softmax_algorithm():
    default_initial_value = 5  # determines the default initial number for the value of each arms
    arm_selection_history_iteration = []  # This array stores the chosen arm for each iteration ordered by time step
    regret_history_per_time_step = []  # This array stores the regret over all iterations for each time step (The size of the array equals the number of time steps) ***static***  format:[[],[],[],....,] len=number_of_time_step
    cumulative_reward_history_per_time_step = []  # This array stores the  cumulative reward over all iterations  for each time step (The size of the array equals the number of time steps)***static***  format:[[],[],[],....,] len=number_of_time_step
    optimal_arm_history_per_time_step = []  # This array stores the  optimal arm chosen over all iterations  for each time step (The size of the array equals the number of time steps)***static***  format:[[],[],[],....,] len=number_of_time_step
    worst_arm_selection_history=[] # This array stores the number of times  worst arm chosen over all iterations  for each time step (The size of the array equals the number of time steps)***static*** format:[[],[],[],....,] len=number_of_time_step
    accumulated_regret_history = []  # This array stores the accumulated regret over all iterations for each time step (The size of the array equals the number of time steps) ***static*** format:[[],[],[],....,] len=number_of_time_step

    def __init__(self, number_of_arms, initial_values, tau_value, reward_matrix):
        self.number_of_arms = number_of_arms
        self.value_arms = []  # determines the value of arms at each step
        self.chosen_arm_history = []  # This array records the history of action chosen by algorithm
        self.reward_history = []  # This array records the history of rewards obtained by the algorithm
        self.setup_initial_value(initial_values)
        self.each_arm_play_counter = [0 for i in range(
        self.number_of_arms)]  # This list saves number of time each arm has been played. It is used with reward_matrix to get the correspondong reward
        self.reward_matrix = reward_matrix
        self.tau_value = tau_value
        self.algorithm_name="Softmax"

    # sets the initial value of the value_arms[] and number_of_times_arm_chosen[]
    def setup_initial_value(self, initial_values):
        self.number_of_times_arm_chosen = [0 for i in range(self.number_of_arms)]
        if (len(initial_values) == 0):
            self.set_defualt_initial_value()
        else:
            self.value_arms = copy.deepcopy(initial_values)

    def set_defualt_initial_value(self):
        for i in range(self.number_of_arms):
            self.value_arms.append(self.default_initial_value)

    # This function puts together the components of softmax_algorithm (choose_arm,update_value) and runs the whole algorithm
    def run(self):
        chosen_arm = self.choose_arm()
        counter_chosen_arm = self.each_arm_play_counter[chosen_arm]
        reward = self.reward_matrix[chosen_arm][counter_chosen_arm]
        self.each_arm_play_counter[chosen_arm] = counter_chosen_arm + 1
        self.update_value(chosen_arm, reward)
        self.chosen_arm_history.append(chosen_arm)
        self.reward_history.append(reward)
        return chosen_arm

    # This function choose arms based on the softmax algorithm by considering the variance
    def choose_arm(self):
        chosen_arm = self.softmax_policy_value()  # before choosing an arm, we modify mean value to consider variances according to softmax
        return chosen_arm

    # This function modifies the average value according to softmax algorithm so as to consider variance
    def softmax_policy_value(self):
        new_value = self.assign_probability_to_arm()
        chosen_arm = self.random_arm_based_on_softmax_prob(new_value)
        return chosen_arm

    # This function assign probability to arms based on softmax algorithm
    def assign_probability_to_arm(self):
        new_value = []
        sum = 0
        for mean in self.value_arms:
            sum += math.exp(mean / self.tau_value)
        for mean in self.value_arms:
            new_value.append(math.exp(mean / self.tau_value) / sum)
        return new_value

    # This function returns an arm with probability according to the probability given by softmax to each arm based on their value
    def random_arm_based_on_softmax_prob(self, new_value):
        random_number = np.random.uniform(0, 1)
        previous_probability = 0
        arm_number = 0
        for probability in new_value:
            if (previous_probability <= random_number < probability):
                return arm_number
            arm_number += 1
            previous_probability = probability
        return len(new_value) - 1

    # This function update the value corresponding to the chosen arm and the reward signal of environment
    def update_value(self, chosen_arm, reward):
        self.number_of_times_arm_chosen[chosen_arm] = self.number_of_times_arm_chosen[chosen_arm] + 1
        self.value_arms[chosen_arm] = self.value_arms[chosen_arm] + (
                    1 / self.number_of_times_arm_chosen[chosen_arm]) * (reward - self.value_arms[chosen_arm])
