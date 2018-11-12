# This class implements the Thompson Sampling algorithm
# for alpha here we have used the expected reward estimate
# for more information please refer to the paper "An Empirical Evaluation of Thompson Sampling by Olivier Chapelle"


import numpy as np
import math
from bandit_simulator.bandit.MainDiscreteSetting import *


class thompson_sampling_algorithm():
    default_initial_value = 0  # determines the default initial number for the value of each arms
    arm_selection_history_iteration = []  # This array stores the chosen arm for each iteration ordered by time step
    regret_history_per_time_step = []  # This array stores the regret over all iterations for each time step (The size of the array equals the number of time steps) ***static*** format:[[],[],[],....,] len=number_of_time_step
    cumulative_reward_history_per_time_step = []  # This array stores the  cumulative reward over all iterations  for each time step (The size of the array equals the number of time steps)***static*** format:[[],[],[],....,] len=number_of_time_step
    optimal_arm_history_per_time_step = []  # This array stores the number of times  optimal arm chosen over all iterations  for each time step (The size of the array equals the number of time steps)***static*** format:[[],[],[],....,] len=number_of_time_step
    worst_arm_selection_history = []  # This array stores the number of times  worst arm chosen over all iterations  for each time step (The size of the array equals the number of time steps)***static*** format:[[],[],[],....,] len=number_of_time_step
    accumulated_regret_history = []  # This array stores the accumulated regret over all iterations for each time step (The size of the array equals the number of time steps) ***static*** format:[[],[],[],....,] len=number_of_time_step

    def __init__(self, number_of_arms, alpha, beta,reward_matrix):
        self.number_of_arms = number_of_arms
        self.value_arms = []  # determines the value of arms at each step
        self.chosen_arm_history = []  # This array records the history of action chosen by algorithm
        self.reward_history = []  # This array records the history of rewards obtained by the algorithm
        self.arms_failure_counter_list = [0 for i in range(self.number_of_arms)]  # This list, counts the number of time each arm has failled during the iteration. The list is sorted by according to arms indices.
        self.arms_success_counter_list = [0 for i in range(self.number_of_arms)]  # This list, counts the number of time each arm has succeeded during the iteration. The list is sorted by according to arms indices.
        self.each_arm_play_counter=[0 for i in range(self.number_of_arms)] #This list saves number of time each arm has been played. It is used with reward_matrix to get the correspondong reward
        self.reward_matrix = reward_matrix
        self.alpha = alpha
        self.beta = beta
        self.algorithm_name = "Thompson Sampling"

    # This function puts together the components of Thompson Sampling (choose_arm,update_value) and runs the whole algorithm
    def run(self):
        chosen_arm = self.choose_arm()
        counter_chosen_arm=self.each_arm_play_counter[chosen_arm]
        reward = self.reward_matrix[chosen_arm][counter_chosen_arm]
        self.each_arm_play_counter[chosen_arm]=counter_chosen_arm+1
        self.update_value(chosen_arm, reward)
        self.chosen_arm_history.append(chosen_arm)
        self.reward_history.append(reward)
        return chosen_arm

    # This function choose arms based on the Thompson sampling with beta prior for bernouli distribution algorithm by considering the variance
    def choose_arm(self):
        new_value = self.policy_value()  # before choosing an arm, we use beta distribution as a prior to select arm according to Thompson sampling
        return np.random.choice(np.flatnonzero(np.array(new_value) == np.array(
            new_value).max()))  # in order to break the tie randomly we used this statement

    #This function assigns values to different arms
    def policy_value(self):
        new_value = []
        for arm_number  in range(self.number_of_arms):
            beta_sample = self.beta_distribution_sample_given_arm(arm_number)
            new_value.append(beta_sample)
        self.value_arms=new_value
        return new_value

    # given the arm number, this function samples the beta distribution
    def beta_distribution_sample_given_arm(self, arm_number):
        posterior_alpha = self.alpha + self.arms_success_counter_list[arm_number]
        posterior_beta = self.beta + self.arms_failure_counter_list[arm_number]
        return np.random.beta(posterior_alpha,posterior_beta)

    # This function update the value corresponding to the chosen arm and the reward signal of environment
    def update_value(self, chosen_arm, reward):
        if(reward==0):
            self.arms_failure_counter_list[chosen_arm]+=1
        else:
            self.arms_success_counter_list[chosen_arm]+=1