import gym
import numpy as np
from abc import ABCMeta, abstractmethod

class BaseEnvironment(metaclass=ABCMeta):
    """
    Implements the environment for an RLearner experiment.
    Required methods: env_start, env_step.
    """
    def __init__(self):
        """
        Initialize the first reward, observation, terminal triple:
        reward (float), state observation (numpy array), terminal (boolean).
        """
        reward = None
        observation = None
        terminal = None
        self.reward_obs_terminal = (reward, observation, terminal)

    @abstractmethod
    def env_start(self):
        """The first method called when the experiment starts (called before
        the agent starts). Returns the first state observation.
        """

    @abstractmethod
    def env_step(self, action):
        """
        Step taken by the environment based on action from agent. The argument
        is the action taken by the agent. Returns a triple:
        reward (float), state observation (numpy array), terminal (boolean).
        """

class TenArmEnvironment(BaseEnvironment):
    def __init__(self, env_dict={}):
        super().__init__()

        # get random seed for numpy
        self.seed = env_dict.get("random_seed", None)
        np.random.seed(self.seed)

        # mean values for the ten arms are random draws from a standard Normal
        self.arms = np.random.randn(10)
        # alternative, but equivalent, code:
        # self.arms = [np.random.normal(0.0, 1.0) for _ in range(10)]

        local_observation = np.array([0])
        self.reward_obs_terminal = (0.0, local_observation, False)

    def env_start(self):
        return self.reward_obs_terminal[1]

    def env_step(self, action):
        # rewards from an arm are noisy versions of its mean value
        # the noise is standard Normal
        reward = self.arms[action] + np.random.randn()
        # alternative, but equivalent, code:
        # reward = np.random.normal(self.arms[action], 1.0)

        # we can experiment with other ways of specifying rewards for arms:
        # if action == 0: # arm 0
        #     if np.random.random() < 0.2:
        #         reward = 10
        #     else:
        #         reward = -1
        # if action == 1: # arm 1
        #     reward = np.random.choice(range(10, 15))
        # if action == 2: # arm 2
        #     if np.random.random() < 0.85:
        #         reward = 100
        #     else:
        #         reward = 5

        obs = self.reward_obs_terminal[1]
        self.reward_obs_terminal = (reward, obs, False)

        return self.reward_obs_terminal

class CliffWalkEnvironment(BaseEnvironment):
    def __init__(self, env_dict={}):
        super().__init__()
        # default height 4 (rows), default width 12 (columns)
        self.grid_h = env_dict.get("grid_height", 4)
        self.grid_w = env_dict.get("grid_width", 12)

        # Positive x goes down (top row = 0, next row down = 1 etc.)
        # Positive y goes right (leftmost column = 0, next column to the right = 1 etc.)
        # Arrays are 0-indexed, so max x value is grid_h - 1 and max y value is grid_w - 1
        # Starting location of agent is the bottom-left corner: (max x, min y)
        self.start_loc = (self.grid_h - 1, 0)
        # Goal location is bottom-right corner: (max x, max y)
        self.goal_loc = (self.grid_h - 1, self.grid_w - 1)

        # The cliff will contain all the cells between the start_loc and goal_loc.
        self.cliff = [(self.grid_h - 1, i) for i in range(1, (self.grid_w - 1))]

    def env_start(self):
        reward = 0
        # agent_loc will hold the current location of the agent
        self.agent_loc = self.start_loc
        # state is the one dimensional state representation of the agent location.
        state = self.state(self.agent_loc)
        terminal = False
        self.reward_state_term = (reward, state, terminal)

        return self.reward_state_term[1]

    def env_step(self, action):
        if action == 0: # UP
            possible_next_loc = (self.agent_loc[0] - 1, self.agent_loc[1])
            if possible_next_loc[0] >= 0: # Within Bounds?
                self.agent_loc = possible_next_loc
            else:
                pass # Stay.
        elif action == 1: # LEFT
            possible_next_loc = (self.agent_loc[0], self.agent_loc[1] - 1)
            if possible_next_loc[1] >= 0: # Within Bounds?
                self.agent_loc = possible_next_loc
            else:
                pass # Stay.
        elif action == 2: # DOWN
            possible_next_loc = (self.agent_loc[0] + 1, self.agent_loc[1])
            if possible_next_loc[0] < self.grid_h: # Within Bounds?
                self.agent_loc = possible_next_loc
            else:
                pass # Stay.
        elif action == 3: # RIGHT
            possible_next_loc = (self.agent_loc[0], self.agent_loc[1] + 1)
            if possible_next_loc[1] < self.grid_w: # Within Bounds?
                self.agent_loc = possible_next_loc
            else:
                pass # Stay.
        else:
            raise Exception(str(action) + " not in recognized actions [0: Up, 1: Left, 2: Down, 3: Right]!")

        reward = -1
        terminal = False

        if self.agent_loc == self.goal_loc: # Reached Goal!
            terminal = True
        elif self.agent_loc in self.cliff: # Fell into the cliff!
            reward = -100
            self.agent_loc = self.start_loc
        else:
            pass

        self.reward_state_term = (reward, self.state(self.agent_loc), terminal)
        return self.reward_state_term

    def state(self, loc):
        h, w = loc
        single_index = h * self.grid_w + w
        assert single_index in range(self.grid_w * self.grid_h)
        return single_index



class LunarLanderEnvironment(BaseEnvironment):
    def __init__(self, env_dict={}):
        self._inner_env = gym.make("LunarLander-v2")
        self._inner_env.seed(env_dict.get("seed", 0))

    def env_start(self):
        reward = 0.0
        observation = self._inner_env.reset()
        terminal = False

        self.reward_obs_terminal = (reward, observation, terminal)
        return self.reward_obs_terminal[1]

    def env_step(self, action):
        last_state = self.reward_obs_terminal[1]
        current_state, reward, terminal, _ = self._inner_env.step(action)

        self.reward_obs_terminal = (reward, current_state, terminal)
        return self.reward_obs_terminal
