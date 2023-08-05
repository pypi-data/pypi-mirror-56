import numpy as np
from abc import ABCMeta, abstractmethod
from .utils import argmax

class BaseAgent(metaclass=ABCMeta):
    """
    Implements the agent for an RLearner experiment.
    Required methods: agent_start, agent_step, agent_end.
    """
    def __init__(self, agent_dict={}):
        """
        Initializes agent on RLearner experiment start.
        """

    @abstractmethod
    def agent_start(self, observation):
        """
        Called when experiment starts, immediately after environment starts.
        Takes state observation (numpy array) from the environment's env_start
        function and returns the first action the agent takes.
        """

    @abstractmethod
    def agent_step(self, reward, observation):
        """
        Takes the reward (float) and the state observation (numpy array)
        received after taking the last action and returns the new action
        the agent is taking.
        Takes the last reward (float) the agent received for taking the last
        action, and the state observation (numpy array) the agent received
        from the environment after taking the last action, and returns the new
        action the agent is taking.
        """

    @abstractmethod
    def agent_end(self, reward):
        """
        Final step taken by agent. Takes the reward (float) received after
        taking the last action, which led to a terminal state. Has to return
        None, since no new action is taken by the agent.
        """

class BaseBanditAgent(BaseAgent):
    def __init__(self, agent_dict={}):
        self.num_actions = agent_dict.get("num_actions", 2)

        # self.q_values: array with the agent's value estimates for each action
        self.initial_value = agent_dict.get("initial_value", 0.0)
        default_q_values = np.ones(agent_dict.get("num_actions", 2)) * self.initial_value
        self.q_values = agent_dict.get("state_array", default_q_values)

        self.step_size = agent_dict.get("step_size", 0.1)
        # probability (ranges between 0 and 1) that an epsilon-greedy agent will explore
        self.epsilon = agent_dict.get("epsilon", 0.0)

        # keeps track of the number of times each arm has been pulled
        self.arm_count = [0.0 for _ in range(self.num_actions)]

        # action taken by agent on the previous time step
        self.last_action = 0

    def agent_start(self, observation):
        self.last_action = np.random.choice(self.num_actions)
        return self.last_action

    def agent_step(self, reward, observation):
        self.last_action = np.random.choice(self.num_actions)
        return self.last_action

    def agent_end(self, reward):
        return None

class GreedyAgent(BaseBanditAgent):
    def agent_step(self, reward, observation):
        # Increment counter for the action taken on the previous step
        self.arm_count[self.last_action] += 1
        # Update step size: inversely proportional to how often the action was
        # selected in the past
        alpha = 1/self.arm_count[self.last_action]

        # Update action values as in section 2.4 of the Sutton & Barto textbook
        target = reward
        delta = target - self.q_values[self.last_action]
        self.q_values[self.last_action] += alpha * delta

        current_action = argmax(self.q_values)
        self.last_action = current_action

        return current_action

class EpsilonGreedyAgent(BaseBanditAgent):
    def agent_step(self, reward, observation):
        # Update action-values: same update as the greedy agent
        self.arm_count[self.last_action] += 1
        alpha = 1/self.arm_count[self.last_action]
        target = reward
        delta = target - self.q_values[self.last_action]
        self.q_values[self.last_action] += alpha * delta

        # Choose action using epsilon-greedy policy
        # Randomly choose a number between 0 and 1 and check if <self.epsilon:
        # -- if it is, set current_action to a random action
        # -- if it isn't, choose current_action greedily (as the greedy agent)
        current_action = np.random.randint(len(self.q_values)) \
                             if np.random.random() < self.epsilon \
                         else argmax(self.q_values)
        self.last_action = current_action

        return current_action

class EpsilonGreedyAgentConstantStepsize(BaseBanditAgent):
    def agent_step(self, reward, observation):
        self.arm_count[self.last_action] += 1
        # Update action values in the same way as the epsilon-greedy agent
        # except we use self.step_size instead of self.arm_count
        target = reward
        delta = target - self.q_values[self.last_action]
        self.q_values[self.last_action] += self.step_size * delta

        # Choose action using epsilon-greedy policy
        current_action = np.random.randint(len(self.q_values)) \
                             if np.random.random() < self.epsilon \
                         else argmax(self.q_values)
        self.last_action = current_action

        return current_action

class TDAgent(BaseAgent):
    def __init__(self, agent_dict={}):
        # Create a random number generator with provided seed for reproducibility
        self.rand_generator = np.random.RandomState(agent_dict.get(seed))

        # Policy is given; the goal is to accurately estimate its value function
        self.policy = agent_dict.get("policy")
        # Discount factor gamma
        self.discount = agent_dict.get("discount")
        # The learning rate / step size parameter alpha
        self.step_size = agent_dict.get("step_size")

        # Initialize an array of zeros that will hold the values.
        # The policy is a (# States, # Actions) array, so we use the first
        # dimension of the policy to initialize the values
        self.values = np.zeros((self.policy.shape[0],))

    def agent_start(self, state):
        # The policy is a (# States, # Actions) array, so we use the second
        # dimension when choosing an action
        action = self.rand_generator.choice(range(self.policy.shape[1]),
                                            p=self.policy[state])
        self.last_state = state

        return action

    def agent_step(self, reward, state):
        # Update last_state value given the reward and current state
        target = reward + self.discount * self.values[state]
        delta = target - self.values[self.last_state]
        self.values[self.last_state] += self.step_size * delta

        # Select action based on current state
        action = self.rand_generator.choice(range(self.policy.shape[1]),
                                            p=self.policy[state])
        # Update last_state
        self.last_state = state

        return action

    def agent_end(self, reward):
        # Same update as in agent_step except the target is only the reward
        # since the current state is terminal and the value of terminal states
        # is always 0
        target = reward
        delta = target - self.values[self.last_state]
        self.values[self.last_state] += self.step_size * delta

        # return None since there is no action in terminal states
        return None
