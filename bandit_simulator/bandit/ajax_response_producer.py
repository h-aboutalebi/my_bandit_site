# This class implements the graphical representation of bandit problem

import numpy as np
import pickle
import math
from random import shuffle


class ajax_response_producer:

    def __init__(self, list_Algorithms_name, list_algorithms_instances, reward_tensor, bernouli_distribution_arms, initial_value):
        self.list_Algorithms_name = list_Algorithms_name
        self.bernouli_distribution_arms = bernouli_distribution_arms
        self.regret_algorithms_list = [element.regret_history_per_time_step for element in list_algorithms_instances]
        self.accumulated_regret_algorithms_list = [element.accumulated_regret_history for element in
                                                   list_algorithms_instances]
        self.number_of_algorithms = len(self.regret_algorithms_list)
        self.cumulative_reward_algorithms_list = [element.cumulative_reward_history_per_time_step for element in
                                                  list_algorithms_instances]
        self.optimal_arm_percentage_algorithms_list = [element.optimal_arm_history_per_time_step for element in
                                                       list_algorithms_instances]
        self.worst_arm_selection_history_algorithms_list = [element.worst_arm_selection_history for element in
                                                            list_algorithms_instances]
        self.arm_selection_history_algorithms_list = [element.arm_selection_history_iteration for element in
                                                      list_algorithms_instances]
        self.number_of_steps = len(self.regret_algorithms_list[0])
        self.reward_tensor = reward_tensor
        self.number_of_iterations = len(self.regret_algorithms_list[0][0])
        self.number_of_arms = list_algorithms_instances[0].number_of_arms
        self.initial_value = initial_value
        self.start(list_algorithms_instances)

    # This function put together all the components of graphic class
    def start(self, list_algorithms_instances):
        self.set_answer_dictionary_ajax(list_algorithms_instances)  # initializes the response query to ajax request
        self.assign_ajax_dictionary_response()

    # This function produces the ajax response
    def assign_ajax_dictionary_response(self):
        self.dictionary_container['regret_figure'] = self.assign_ROA_ajax_values(self.regret_algorithms_list)
        self.dictionary_container['cumulative_reward'] = self.assign_ROA_ajax_values(
            self.cumulative_reward_algorithms_list)
        self.dictionary_container['optimal_arm_percentage'] = self.assign_ROA_ajax_values(
            self.optimal_arm_percentage_algorithms_list)
        self.dictionary_container['worst_arm_percentage'] = self.assign_ROA_ajax_values(
            self.worst_arm_selection_history_algorithms_list)
        self.dictionary_container['accumulated_regret'] = self.assign_ROA_ajax_values(
            self.accumulated_regret_algorithms_list)
        self.assign_arm_selection_ajax_values()

    # This function will assign the  values corresponding to the way the each algorithm choose arms during runtime for the ajax response
    def assign_arm_selection_ajax_values(self):
        for algorithm_number in range(self.number_of_algorithms):
            self.produce_ajax_response_arm_selection_history_algorithm(
                algorithm_number)  # 'i' represents the number of corresponding algorithm we want to draw

    # This function will draw action selection corresponding to the given algorithm. Each algorithm are already assigned a number
    def produce_ajax_response_arm_selection_history_algorithm(self, algorithm_number):
        mean, std = self.retrieve_mean_std_of_arm_selection(self.arm_selection_history_algorithms_list[
                                                                algorithm_number])  # this is an array containing subarray which each of them has the mean and std of the corresponding arm per time step
        self.dictionary_container['arm_selection_history_all_algorithm_list'][algorithm_number] = [mean, std]
        mean, std = self.create_confidence_interval_of_arms(self.arm_selection_history_algorithms_list[
                                                                algorithm_number], self.cumulative_reward_algorithms_list[
                                                                algorithm_number])  # this is an array containing subarray which each of them has the mean and std of the corresponding arm per time step
        self.dictionary_container['arm_confidence_all_algorithm_list'][algorithm_number] = [mean, std]

    # This function will assign the  values corresponding to Regret, Optimal action percentage, Accumulated rewards (ROA), accumuluted regret, worst action percentage for the ajax response
    def assign_ROA_ajax_values(self, list_algorithms_ROA_results):
        mean_std = [self.retrieve_mean_std(element) for element in list_algorithms_ROA_results]
        mean = [element[0] for element in mean_std]
        std = [element[1] for element in mean_std]
        return [mean, std]

    # given the array of subarray, it returns the average and std of each subarray. The input format is: [[],[],[],[],...]
    def retrieve_mean_std(self, array):
        mean = np.mean(array, axis=1)
        std = np.std(array, axis=1)
        return [mean.tolist(), std.tolist()]

    # This calculates the std corresponding to each arm during the runtime of a given algorithm. *** we needed a different function other than retrieve_mean_std for this ***  ;-(
    def retrieve_mean_std_of_arm_selection(self, array_arm_selection_history):
        array_mean_of_arm_selection = []
        array_std_of_arm_selection = []
        for arm in range(self.number_of_arms):
            array_mean_std_specifc_arm = [[], []]  # first sublist is for mean. Second sublist is for std
            for step in range(self.number_of_steps):
                sum = 0
                for experiment in range(self.number_of_iterations):
                    if (arm == array_arm_selection_history[experiment][step]):
                        sum += 1
                mean = (sum * 100) / self.number_of_iterations  # product of 100 in numenator is for percentage
                std = math.sqrt((sum * (100 - mean) ** 2) / self.number_of_iterations)
                array_mean_std_specifc_arm[0].append(mean)
                array_mean_std_specifc_arm[1].append(std)
            array_mean_of_arm_selection.append(array_mean_std_specifc_arm[0])
            array_std_of_arm_selection.append(array_mean_std_specifc_arm[1])
        return array_mean_of_arm_selection, array_std_of_arm_selection

    # This function creates the confidence interval for all arms corresponding to each bandit algorithm (The formula given by Tibor)
    def create_confidence_interval_of_arms(self, array_arm_selection_history, cumulative_reward_history_per_time_step):
        array_mean_of_arm_reward = []
        array_std_of_arm_reward = []
        for arm in range(self.number_of_arms):
            array_mean_std_specifc_arm = [[], []]  # first sublist is for mean. Second sublist is for std
            array_average_est_reward_of_arm = [1 for experiment in range(self.number_of_iterations)]
            initial_std_estimate = 0
            array_std_est_reward_of_arm = [initial_std_estimate for experiment in range(self.number_of_iterations)]
            array_number_times_arm_chosen = [1 for experiment in range(self.number_of_iterations)]
            for step in range(self.number_of_steps):
                for experiment in range(self.number_of_iterations):
                    if (arm == array_arm_selection_history[experiment][step]):
                        old_average = array_average_est_reward_of_arm[experiment]
                        old_counter_arm = array_number_times_arm_chosen[experiment]
                        array_number_times_arm_chosen[experiment] += 1
                        reward = self.compute_reward_confidence_interval(step, experiment, cumulative_reward_history_per_time_step)
                        new_average = (old_average * old_counter_arm + reward) / (old_counter_arm + 1)
                        array_average_est_reward_of_arm[experiment] = new_average
                        array_std_est_reward_of_arm[experiment] = 1.96 * np.sqrt(np.abs((1 - new_average) * new_average) / (old_counter_arm + 1))
                mean = np.mean(array_average_est_reward_of_arm)
                std = np.mean(array_std_est_reward_of_arm)
                array_mean_std_specifc_arm[0].append(mean)
                array_mean_std_specifc_arm[1].append(std)
            array_mean_of_arm_reward.append(array_mean_std_specifc_arm[0])
            array_std_of_arm_reward.append(array_mean_std_specifc_arm[1])
        return array_mean_of_arm_reward, array_std_of_arm_reward

    # This function computes the reward
    def compute_reward_confidence_interval(self, step, experiment, cumulative_reward_history_per_time_step):
        if (step == 0):
            return cumulative_reward_history_per_time_step[step][experiment]
        else:
            old_reward = cumulative_reward_history_per_time_step[step - 1][experiment]
            new_reward = cumulative_reward_history_per_time_step[step][experiment]
            return new_reward-old_reward

    # This initilizes the response for the ajax request
    def set_answer_dictionary_ajax(self, list_algorithms_instances):
        self.dictionary_container = {
            'reward_tensor': self.reward_tensor,  # reward matrix for loading option of form
            'bernouli_distribution_arms': self.bernouli_distribution_arms,  # arm_distribution_list for loading option of form
            'regret_figure': [[], []],
            # it stores regret_figure data. The first sublist is for mean, the second sublist is for std
            'cumulative_reward': [[], []],
            # it stores accumulateive reward data. The first sublist is for mean, the second sublist is for std
            'optimal_arm_percentage': [[], []],
            # it stores optimal arm percentage play. The first sublist is for mean, the second sublist is for std
            'worst_arm_percentage': [[], []],
            # it stores worst arm percentage play. The first sublist is for mean, the second sublist is for std
            'accumulated_regret': [[], []],
            # it stores accumulated_regret data. The first sublist is for mean, the second sublist is for std
            'number_of_arms': self.number_of_arms,
            'number_of_steps': self.number_of_steps,
            'number_of_iterations': self.number_of_iterations,
            'list_Algorithms_name': self.list_Algorithms_name,
            'arm_selection_history_all_algorithm_list': [[[], []] for i in range(len(self.list_Algorithms_name))],
            # This contains the mean std sets corresponding to each algorithm. each sublist corresponds to one algorithm where later we will use the corresponding list_Algorithms_name to find the algorithm name for display on client-side
            'arm_confidence_all_algorithm_list': [[[], []] for i in range(len(self.list_Algorithms_name))],
            # This contains the mean std sets corresponding to each algorithm. each sublist corresponds to one algorithm where later we will use the corresponding list_Algorithms_name to find the algorithm name for display on client-side
            'x_list': [i for i in range(len(self.regret_algorithms_list[0]))]
        }

# def main():
#     plot_my_graph=my_graphics(["Epsilon Greedy","UCB1","Softmax"])
#
#
#
# if __name__ == '__main__':
#     main()
