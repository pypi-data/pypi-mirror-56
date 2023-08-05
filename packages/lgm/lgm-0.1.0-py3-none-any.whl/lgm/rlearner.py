import numpy as np
import matplotlib.pyplot as plt
import pickle
from tqdm import tqdm # basic progress bar; TO DO: replace with ProgressCallback

class RLearner():
    """
    Puts together an agent and an environment, and runs an experiment.
    """
    def __init__(self, agent, env):
        """
        Initialize RL experiment.

        TO DO: The 3 stats for returns, cumulative_rewards and
        average_rewards, as well as associated code keeping track of these
        stats per episode, should move to AvgStatsCallback.
        """
        self.agent = agent
        self.env = env

        # returns / total rewards for each episode
        self.returns = []
        # cumulative rewards for each step of each episode
        self.cumulative_rewards = []
        # average rewards (current cumulative reward / current number of steps)
        # for each step of each episode
        self.average_rewards = []
        self.actions = []

    def __getattr__(self, attr_name):
        """
        Percolates attributes from self.agent and self.env:
        agent_start, agent_step, agent_end, env_start, env_step
        """
        if hasattr(self.agent, attr_name):
            return getattr(self.agent, attr_name)
        elif hasattr(self.env, attr_name):
            return getattr(self.env, attr_name)
        else:
            raise AttributeError

    def episode_start(self):
        """
        Start RLearner experiment. Returns a (state, action) pair.
        """
        # initialize stats for the current episode
        self.current_return = 0.0
        self.current_step = 1
        self.current_cumulative_rewards = [self.current_return]
        self.current_average_rewards = [self.current_return/self.current_step]

        # initial step through the environment
        last_state = self.env.env_start()
        # the agent takes initial step based on the env step
        self.last_action = self.agent.agent_start(last_state)

        self.current_actions = [self.last_action]

        # package everything and return the package
        state_action = (last_state, self.last_action)
        return state_action

    def step(self):
        """
        Step in the experiment taken by RLearner, consisting of env_step and agent_step/agent_end. Returns a quadruple:
        reward (float), last state observation, last action, terminal (boolean)
        """
        # one step through the environment
        (reward, last_state, terminal) = self.env_step(self.last_action)

        # update current episode stats with the new env step
        self.current_return += reward
        self.current_step += 1
        self.current_cumulative_rewards.append(self.current_return)
        self.current_average_rewards.append(self.current_return/self.current_step)

        # the agent takes one step based on the env step
        if terminal:
            self.last_action = self.agent_end(reward)
        else:
            self.last_action = self.agent_step(reward, last_state)


        self.current_actions.append(self.last_action)

        # package everything and return the package
        reward_observation_action_terminal = (reward, last_state, self.last_action, terminal)
        return reward_observation_action_terminal

    def run_episode(self, total_steps):
        """
        Runs an episode. Takes the maximum number of total_steps (int) per
        episode and returns a boolean indicating the episode terminated.
        The total_steps=0 default enforces no step limit.
        """
        # initialize episode
        terminal = False
        self.episode_start()

        # run episode
        while (not terminal) and (total_steps == 0 or \
                                  self.current_step < total_steps):
            reward_observation_action_terminal = self.step()
            terminal = reward_observation_action_terminal[3]

        # add the episode stats to the overall RLearner experiment stats
        self.returns.append(self.current_return)
        self.cumulative_rewards.append(self.current_cumulative_rewards)
        self.average_rewards.append(self.current_average_rewards)
        self.actions.append(self.current_actions)
        self.current_episode += 1

        return terminal

    def run_episodes(self, total_episodes, total_steps=0):
        # store experimental specs
        self.total_episodes = total_episodes
        self.total_steps = total_steps

        # initialize experiment
        self.current_episode = 0

        # run experiment
        # for _ in tqdm(range(self.total_episodes)):
        for _ in range(self.total_episodes):
            self.run_episode(self.total_steps)

        return self.current_episode
