#This class implements the epsilon_greedy algorithm
# for alpha here we have used the expected reward estimate


from MainDiscreteSetting import main_program
import numpy as np



class epsilon_greedy_algorithm():

    default_initial_value = 5 #determines the default initial number for the value of each arms
    arm_selection_history_iteration = []  #This array stores the chosen arm for each iteration ordered by time step.
    regret_history_per_time_step = []  # This array stores the regret over all iterations for each time step (The size of the array equals the number of time steps) ***static***  format:[[],[],[],....,] len=number_of_time_step
    cumulative_reward_history_per_time_step = []  # This array stores the  cumulative reward over all iterations  for each time step (The size of the array equals the number of time steps)***static*** format:[[],[],[],....,] len=number_of_time_step
    optimal_arm_history_per_time_step = []  # This array stores the  optimal arm chosen over all iterations  for each time step (The size of the array equals the number of time steps)***static*** format:[[],[],[],....,] len=number_of_time_step
    worst_arm_selection_history=[] # This array stores the number of times  worst arm chosen over all iterations  for each time step (The size of the array equals the number of time steps)***static*** format:[[],[],[],....,] len=number_of_time_step
    accumulated_regret_history = []  # This array stores the accumulated regret over all iterations for each time step (The size of the array equals the number of time steps) ***static*** format:[[],[],[],....,] len=number_of_time_step

    def __init__(self, number_of_arms, initial_values, epsilon, reward_matrix):
        self.number_of_arms=number_of_arms
        self.value_arms = []  # determines the value of arms at each step
        self.chosen_arm_history = []  # This array records the history of action chosen by algorithm
        self.reward_history = []  # This array records the history of rewards obtained by the algorithm
        self.setup_initial_value(initial_values)
        self.epsilon=epsilon
        self.each_arm_play_counter = [0 for i in range(self.number_of_arms)]  # This list saves number of time each arm has been played. It is used with reward_matrix to get the correspondong reward
        self.reward_matrix = reward_matrix
        self.algorithm_name="Epsilon Greedy"

    #sets the initial value of the value_arms[] and number_of_times_arm_chosen[]
    def setup_initial_value(self, initial_values):
        self.number_of_times_arm_chosen=[0 for i in range(self.number_of_arms)]
        if(len(initial_values)==0):
            self.set_defualt_initial_value()
        else:
            self.value_arms=initial_values

    def set_defualt_initial_value(self):
        for i in range(self.number_of_arms):
            self.value_arms.append(self.default_initial_value)

#This function puts together the components of epsilon_greedy_algorithm (choose_arm,update_value) and runs the whole algorithm
    def run(self):
        chosen_arm=self.choose_arm()
        counter_chosen_arm = self.each_arm_play_counter[chosen_arm]
        reward = self.reward_matrix[chosen_arm][counter_chosen_arm]
        self.each_arm_play_counter[chosen_arm] = counter_chosen_arm + 1
        self.update_value(chosen_arm,reward)
        self.chosen_arm_history.append(chosen_arm)
        self.reward_history.append(reward)
        return chosen_arm

#This function choose arms based on the epsilon_greedy algorithm (index=0 <> any arm with equal probability. index=1 <> maximum value arm returned)
    def choose_arm(self):
        index=main_program.epsilon_greedy_policy(self.epsilon)
        if(index==0):
            return np.random.randint(0,self.number_of_arms)
        else:
            return np.random.choice(np.flatnonzero(np.array(self.value_arms) == np.array(self.value_arms).max())) #in order to break the tie randomly we used this statement

#This function update the value corresponding to the chosen arm and the reward signal of environment
    def update_value(self,chosen_arm, reward):
        self.number_of_times_arm_chosen[chosen_arm]=self.number_of_times_arm_chosen[chosen_arm]+1
        self.value_arms[chosen_arm]= self.value_arms[chosen_arm]+(1/self.number_of_times_arm_chosen[chosen_arm])*(reward-self.value_arms[chosen_arm])

