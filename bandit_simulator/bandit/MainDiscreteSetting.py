# This file is the main starting point of simulation
# Here we assume each arm has bernouli distribution as we have two kind of reward 0 or 1. **** very important ****


from environmentDiscrete import *
from ajax_response_producer import *
import numpy as np
import pickle
from softmax import *
from thompson_sampling import *
from ucb1 import *
from epsilon_greedy_algorithm import *
from besa import *


class main_program():
    log_file_name = "log.txt"  # The file we are going to store the log information
    pickle_file_name = "dictionary.pickle"  # This file stores the pickled version of objects

    # number_of_iteration=100     #determines the number of time eacheach experimnet is going to be repeated
    # number_of_steps=1000   #determines the number of steps each experiments takes until the convergence
    # epsilon=0.01     #determines the epsilon value for the epsilon_greedy_algorithm
    # number_of_arms=6    #determines the number of alternative arms in the bandit problem(# of options we have to choose ate each step)
    # bernouli_distribution_arms=[0.3,0.1,0.2,0.8,0.6,0.7]    #This detrmines the expected reward of each arm. Arms are: [0, 1, ..., len(bernouli_distribution_arms)-1]
    # bandit_environment=environment(bernouli_distribution_arms)  #creating the instance of environment used in the simulation

    def __init__(self, bool, form_data_dictionary):
        self.number_of_iteration = form_data_dictionary['number_of_experiment']
        self.number_of_steps = form_data_dictionary['patient_number']
        self.number_of_arms = len(form_data_dictionary['mean_value_range'])
        self.epsilon = form_data_dictionary['epsilon_value']
        self.alpha = form_data_dictionary['alpha_value']
        self.reward_tensor_is_uploaded_by_client = False
        self.beta = form_data_dictionary['beta_value']
        self.tau_value = form_data_dictionary['tau_value']
        self.c_value = form_data_dictionary['c_value']
        self.initial_value = form_data_dictionary['initial_value']
        self.bernouli_distribution_arms = form_data_dictionary['mean_value_range']
        self.bandit_environment = environment(self.bernouli_distribution_arms, self.number_of_arms,
                                              self.number_of_steps)
        self.reward_tensor = self.build_reward_tensor(form_data_dictionary[
                                                          "reward_tensor"])  # This tensor contains the rewards generated before each iteration for arms. It has three indices:[iteration_number, arm_number, step_number]. This array is used for saving and loading option in form [Audrey suggestion]. It is first initilized by the form input if the user has uploaded a file for the reward tensor
        if (bool == True):
            self.run_program()

    # The whole program starts from here:
    def run_program(self):
        self.initial_value = [self.initial_value] * self.number_of_arms
        self.reset_static_field_algorithms(
            [epsilon_greedy_algorithm, ucb1_algorithm, softmax_algorithm, thompson_sampling_algorithm, besa_algorithm])
        for i in range(self.number_of_iteration):
            print(i)
            reward_matrix = self.check_reward_tensor_is_uploaded(
                i)  # for making the environment deterministic and reducing noise
            epsilon_greedy_alg = epsilon_greedy_algorithm(self.number_of_arms, self.initial_value, self.epsilon,
                                                          reward_matrix)
            ucb1_alg = ucb1_algorithm(self.number_of_arms, self.initial_value, self.c_value, reward_matrix)
            softmax_alg = softmax_algorithm(self.number_of_arms, self.initial_value, self.tau_value,
                                            reward_matrix)
            thompson_sampling_alg = thompson_sampling_algorithm(self.number_of_arms, self.alpha, self.beta,
                                                                reward_matrix)
            besa_alg = besa_algorithm(self.number_of_arms, reward_matrix)
            algorithm_instances_list = [epsilon_greedy_alg, ucb1_alg, softmax_alg, thompson_sampling_alg, besa_alg]
            for j in range(self.number_of_steps):
                for algorithm_instance in algorithm_instances_list:
                    algorithm_instance.run()
            self.compute_overal_quality(algorithm_instances_list)
        response = ajax_response_producer([alg.algorithm_name for alg in algorithm_instances_list],
                                          algorithm_instances_list,
                                          self.reward_tensor,
                                          self.bernouli_distribution_arms)  # algorithm_instances_list algorithms should be in the same order of their list name provided in the first argument
        self.ajax_response = response.dictionary_container

    # This function computes the regret,accumulated regret, cumulative reward, percentage of time optimal and worst arm play after the completion of one iteration. This function also calls other functions to update static fields of algorithm like regret, ...
    def compute_overal_quality(self, algorithm_instances_list):
        for algorithm_instance in algorithm_instances_list:
            regret_per_step = self.computing_regret_per_step(algorithm_instance.chosen_arm_history)
            self.update_static_regret_per_step(algorithm_instance, regret_per_step)
            accumulated_regret = self.computing__accumulated_regret(algorithm_instance.chosen_arm_history)
            self.update_static_accumulated_regret(algorithm_instance, accumulated_regret)
            cumulative_reward = self.computing_cumulative_reward(algorithm_instance.reward_history)
            self.update_static_cumulative_reward(algorithm_instance, cumulative_reward)
            percentage_optimal_arm = self.compute_percentage_optimal_arm(algorithm_instance.chosen_arm_history)
            self.update_static_percentage_optimal_arm(algorithm_instance, percentage_optimal_arm)
            pecentage_worst_arm = self.compute_percentage_worst_arm(algorithm_instance.chosen_arm_history)
            self.update_static_percentage_worst_arm(algorithm_instance, pecentage_worst_arm)
            algorithm_instance.arm_selection_history_iteration.append(algorithm_instance.chosen_arm_history)

    # This initilizes the static fields of algorithms in the begining of run to transfer [] -> [[],[],[],....] len=number_of_step.
    def initilize_static_field_algorithm(self, algorithm_instance):
        for i in range(self.number_of_steps):
            algorithm_instance.regret_history_per_time_step.append([])
            algorithm_instance.cumulative_reward_history_per_time_step.append([])
            algorithm_instance.optimal_arm_history_per_time_step.append([])
            algorithm_instance.worst_arm_selection_history.append([])
            algorithm_instance.accumulated_regret_history.append([])

    # This function will update the static value of regret per time step of a given algorithm
    def update_static_regret_per_step(self, algorithm_instance, regret):
        for i in range(self.number_of_steps):
            algorithm_instance.regret_history_per_time_step[i].append(regret[i])

    # This function will update the static value of accumulated regret of a given algorithm
    def update_static_accumulated_regret(self, algorithm_instance, regret):
        for i in range(self.number_of_steps):
            algorithm_instance.accumulated_regret_history[i].append(regret[i])

    # This function will update the static value of cumulative_reward of a given algorithm
    def update_static_cumulative_reward(self, algorithm_instance, cumulative_reward):
        for i in range(self.number_of_steps):
            algorithm_instance.cumulative_reward_history_per_time_step[i].append(cumulative_reward[i])

    # This function will update the static value of percentage_optimal_arm of a given algorithm
    def update_static_percentage_optimal_arm(self, algorithm_instance, percentage_optimal_arm):
        for i in range(self.number_of_steps):
            algorithm_instance.optimal_arm_history_per_time_step[i].append(percentage_optimal_arm[i])

    # This function will update the static value of percentage_optimal_arm of a given algorithm
    def update_static_percentage_worst_arm(self, algorithm_instance, percentage_worst_arm):
        for i in range(self.number_of_steps):
            algorithm_instance.worst_arm_selection_history[i].append(percentage_worst_arm[i])

    # This function will keep the records of the details of every experiment in a file
    def log(self, algorithm, algorithm_name):
        with open(self.log_file_name, 'a') as the_file:
            the_file.write(
                '\n\n\n\n ****** The information about the performance of ' + algorithm_name + ' is as follows:\n')
            the_file.write('The total regret history per time step over all iteration is:\n' + str(
                algorithm.regret_history_per_time_step))
            the_file.write('\nThe total cumulative reward history per time step  over all iteration is:\n' + str(
                algorithm.cumulative_reward_history_per_time_step))
            the_file.write('\nThe total optimal arm history per time step over all iteration is:\n' + str(
                algorithm.optimal_arm_history_per_time_step))
            the_file.write('\nThe total each arm history per time step over all iteration is:\n' + str(
                algorithm.arm_selection_history_iteration))

    # This function computes regret per step
    def computing_regret_per_step(self, chosen_arm_history):
        regret = 0
        regret_Array = []
        maximum_mean = max(self.bernouli_distribution_arms)
        for i in range(len(chosen_arm_history)):
            chosen_arm_mean = self.bernouli_distribution_arms[chosen_arm_history[i]]
            regret_Array.append(maximum_mean - chosen_arm_mean + regret)
        return regret_Array

    # This function computes accumulated regret
    def computing__accumulated_regret(self, chosen_arm_history):
        accumulated_regret = 0
        regret_Array = []
        maximum_mean = max(self.bernouli_distribution_arms)
        for i in range(len(chosen_arm_history)):
            chosen_arm_mean = self.bernouli_distribution_arms[chosen_arm_history[i]]
            accumulated_regret = maximum_mean - chosen_arm_mean + accumulated_regret
            regret_Array.append(accumulated_regret)
        return regret_Array

    # This function computes cumulative rewards
    def computing_cumulative_reward(self, reward_history):
        cumulative_reward = 0
        cumulative_reward_Array = []
        for reward in reward_history:
            cumulative_reward += reward
            cumulative_reward_Array.append(cumulative_reward)
        return cumulative_reward_Array

    # This function computes percentage of time optimal arm is chosen during the experiment
    def compute_percentage_optimal_arm(self, chosen_arm_history):
        numerator = 0
        denominator = 0
        maximum_mean = max(self.bernouli_distribution_arms)
        optimal_action_ratio = []
        for chosen_arm in chosen_arm_history:
            denominator += 1
            if self.bernouli_distribution_arms[chosen_arm] == maximum_mean:
                numerator += 1
            optimal_action_ratio.append((numerator * 100) / denominator)
        return optimal_action_ratio

    # This function computes percentage of time worst arm is chosen during the experiment
    def compute_percentage_worst_arm(self, chosen_arm_history):
        numerator = 0
        denominator = 0
        minimum_mean = min(self.bernouli_distribution_arms)
        optimal_action_ratio = []
        for chosen_arm in chosen_arm_history:
            denominator += 1
            if self.bernouli_distribution_arms[chosen_arm] == minimum_mean:
                numerator += 1
            optimal_action_ratio.append((numerator * 100) / denominator)
        return optimal_action_ratio

    # Based on the value of epsilon, this function returns flag 0 or 1:
    # flag 0 represents that any arm with equal probability should be chosen
    # flag 1 represents only the maximum value arm should be chosen
    @staticmethod
    def epsilon_greedy_policy(epsilon):
        index = np.random.uniform(0, 1)
        if (index <= epsilon):
            return 0
        else:
            return 1

    # This function resets the static fields of algorithms(It is necessary we want to start main program when new request is made by user on the same page)
    def reset_static_field_algorithms(self, Array_algorithms):
        for algorithm in Array_algorithms:
            algorithm.arm_selection_history_iteration = []
            algorithm.regret_history_per_time_step = []
            algorithm.cumulative_reward_history_per_time_step = []
            algorithm.optimal_arm_history_per_time_step = []
            algorithm.worst_arm_selection_history = []
            algorithm.accumulated_regret_history = []
            self.initilize_static_field_algorithm(algorithm)

    # This function is used to intilize the tensor reward aprior.
    def check_reward_tensor_is_uploaded(self, iteration_index):
        if (
                self.reward_tensor_is_uploaded_by_client):  # for the case when the reward tensor is alrteady uploaded by user
            return self.reward_tensor[iteration_index]
        else:
            reward_matrix = self.bandit_environment.create_deterministic_rewrad_matrix()
            self.reward_tensor.append(reward_matrix)
            return reward_matrix

    # This function build reward tensor based on the whether a file containing reward tensor has been uploaded by user or not. It also  update class variable if the reward tensor is uploaded
    def build_reward_tensor(self, form_reward_tensor_string):
        if (form_reward_tensor_string == ""):  # for the case user has not uploaded the file for the reward tensor.
            return []
        else:
            self.reward_tensor_is_uploaded_by_client = True
            reward_tensor_in_array = form_reward_tensor_string.split(',')
            self.reinitilize_class_variable_for_reward_tensor(reward_tensor_in_array)
            reward_tensor = self.generate_original_reward_tensor(reward_tensor_in_array)
            return reward_tensor

    # This function initilizes  number_of_iteration,number_of_arms,number_of_steps, bandit_environment based on uploaded reward_tensor_in_array
    def reinitilize_class_variable_for_reward_tensor(self, reward_tensor_in_array):
        self.number_of_iteration = int(reward_tensor_in_array[0])
        self.number_of_arms = int(reward_tensor_in_array[1])
        self.number_of_steps = int(reward_tensor_in_array[2])
        self.bernouli_distribution_arms = []
        for arm_number in range(self.number_of_arms):
            self.bernouli_distribution_arms.append(float(reward_tensor_in_array[3 + arm_number]))
        self.bandit_environment = environment(self.bernouli_distribution_arms, self.number_of_arms,
                                              self.number_of_steps)

    # This function builds the reward tensor
    def generate_original_reward_tensor(self, reward_tensor_in_array):
        reward_tensor = []
        reward_tensor_raw = reward_tensor_in_array[3 + self.number_of_arms:]
        for iteration_number in range(self.number_of_iteration):
            iteration_reward = []
            for arm_number in range(self.number_of_arms):
                arm_reward = []
                for step_number in range(self.number_of_steps):
                    iteration_index = iteration_number * self.number_of_steps * self.number_of_arms
                    arm_index = arm_number * self.number_of_steps
                    append_index = iteration_index + arm_index + step_number
                    arm_reward.append(float(reward_tensor_raw[append_index]))
                iteration_reward.append(arm_reward)
            reward_tensor.append(iteration_reward)
        return reward_tensor


def main(form_data_dictionary):
    main_response = main_program(True, form_data_dictionary)
    return main_response.ajax_response

# if __name__ == '__main__':
#     main()
