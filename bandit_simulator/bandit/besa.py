# This class implements the BESA algorithm
# for alpha here we have used the expected reward estimate
# For more information please refer to the paper "Sub-sampling for Multi-armed Bandits" by Akram Baransi1

import numpy as np
import math
from bandit_simulator.bandit.MainDiscreteSetting import *
import random


class besa_algorithm():
    default_initial_value = 0  # determines the default initial number for the value of each arms
    arm_selection_history_iteration = []  # This array stores the chosen arm for each iteration ordered by time step
    regret_history_per_time_step = []  # This array stores the regret over all iterations for each time step (The size of the array equals the number of time steps) ***static*** format:[[],[],[],....,] len=number_of_time_step
    cumulative_reward_history_per_time_step = []  # This array stores the  cumulative reward over all iterations  for each time step (The size of the array equals the number of time steps)***static*** format:[[],[],[],....,] len=number_of_time_step
    optimal_arm_history_per_time_step = []  # This array stores the number of times  optimal arm chosen over all iterations  for each time step (The size of the array equals the number of time steps)***static*** format:[[],[],[],....,] len=number_of_time_step
    worst_arm_selection_history = []  # This array stores the number of times  worst arm chosen over all iterations  for each time step (The size of the array equals the number of time steps)***static*** format:[[],[],[],....,] len=number_of_time_step
    accumulated_regret_history = []  # This array stores the accumulated regret over all iterations for each time step (The size of the array equals the number of time steps) ***static*** format:[[],[],[],....,] len=number_of_time_step

    def __init__(self, number_of_arms, reward_matrix):
        self.number_of_arms = number_of_arms
        self.chosen_arm_history = []  # This array records the history of action chosen by algorithm
        self.reward_history = []  # This array records the history of rewards obtained by the algorithm
        self.arms_rewards_history = [[] for i in range(self.number_of_arms)] # This list, contains the history of each arm reward.
        self.each_arm_play_counter = [0 for i in range(self.number_of_arms)]  # This list saves number of time each arm has been played. It is used with reward_matrix to get the correspondong reward
        self.reward_matrix = reward_matrix
        self.algorithm_name = "BESA"

    # This function puts together the components of BESA (choose_arm,update_value) and runs the whole algorithm
    def run(self):
        chosen_arm = self.choose_arm()
        counter_chosen_arm = self.each_arm_play_counter[chosen_arm]
        reward = self.reward_matrix[chosen_arm][counter_chosen_arm]
        self.each_arm_play_counter[chosen_arm] = counter_chosen_arm + 1
        self.update_value(chosen_arm, reward)
        self.chosen_arm_history.append(chosen_arm)
        self.reward_history.append(reward)
        return chosen_arm

    # This function choose arms based on the BESA algorithm. It first creates a tornoment and then decide who is the winner as the output arm.
    def choose_arm(self):
        arm_shuffeled_list = self.shuffle_arms_indices()
        chossen_arm = self.choose_arm_by_tournement(arm_shuffeled_list)
        return chossen_arm

    # This function runs tournoment among arms to detrmine the winner
    def choose_arm_by_tournement(self, list_arms_indeices):
        if (len(list_arms_indeices) == 1):
            return list_arms_indeices[0]
        elif (len(list_arms_indeices) == 2):
            winner_arm = self.two_arms_competition(list_arms_indeices[0], list_arms_indeices[1])
            return winner_arm
        else:
            half_len_list_arms = math.floor(len(list_arms_indeices) / 2)
            finalist_1 = self.choose_arm_by_tournement(list_arms_indeices[:half_len_list_arms])
            finalist_2 = self.choose_arm_by_tournement(list_arms_indeices[half_len_list_arms:])
            return self.two_arms_competition(finalist_1, finalist_2)

    # This function determines the winner among two arms based on BESA criteria
    def two_arms_competition(self, arm_1_index, arm_2_index):
        not_previously_chosen_arm = self.check_if_any_arm_has_not_chosen(arm_1_index, arm_2_index)
        if (not_previously_chosen_arm != -1):
            return not_previously_chosen_arm
        if (len(self.arms_rewards_history[arm_1_index]) > len(self.arms_rewards_history[arm_2_index])):
            return self.detrmine_winner_of_two_arms(arm_1_index, arm_2_index)
        elif (len(self.arms_rewards_history[arm_1_index]) < len(self.arms_rewards_history[arm_2_index])):
            return self.detrmine_winner_of_two_arms(arm_2_index, arm_1_index)
        else:
            arm_list = [arm_2_index, arm_1_index]
            return self.detrmine_winner_of_two_arms(arm_list[0], arm_list[1])

    # in this function it is assumed that arm_1_index has chosen more time than arm_2_index
    def detrmine_winner_of_two_arms(self, arm_1_index, arm_2_index):
        sample_size = len(self.arms_rewards_history[arm_2_index])
        sample_list_arm_1 = np.random.choice(self.arms_rewards_history[arm_1_index], sample_size, replace=False)
        sum_sample_arm_1 = sum(sample_list_arm_1)
        sum_sample_arm_2 = sum(self.arms_rewards_history[arm_2_index])
        if (sum_sample_arm_1 <= sum_sample_arm_2):
            return arm_2_index
        else:
            return arm_1_index

    # This function check to see if any arm has been selected or not.
    def check_if_any_arm_has_not_chosen(self, arm_1_index, arm_2_index):
        if (len(self.arms_rewards_history[arm_1_index]) == 0 and len(self.arms_rewards_history[arm_2_index]) == 0):
            return self.choose_uniformely_between_two_arms(arm_1_index, arm_2_index)
        elif (len(self.arms_rewards_history[arm_1_index]) == 0):
            return arm_1_index
        elif (len(self.arms_rewards_history[arm_2_index]) == 0):
            return arm_2_index
        else:
            return -1  # for the case when both arms has already been chosen

    # This function selects uniformely one arm among two arms
    def choose_uniformely_between_two_arms(self, arm_1_index, arm_2_index):
        random_number = random.uniform(0, 1)
        if (random_number < 0.5):
            return arm_1_index
        else:
            return arm_2_index

    # This function shuffles the indices of arms
    def shuffle_arms_indices(self):
        new_arm_number_indices = [i for i in range(self.number_of_arms)]
        random.shuffle(new_arm_number_indices)
        return new_arm_number_indices

    # This function update the value corresponding to the chosen arm and the reward signal of environment
    def update_value(self, chosen_arm, reward):
        self.arms_rewards_history[chosen_arm].append(reward)
