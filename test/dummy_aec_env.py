from pettingzoo import AECEnv
import copy
from pettingzoo.utils.agent_selector import agent_selector


class DummyEnv(AECEnv):
    metadata = {"render.modes": ["human"]}

    def __init__(self, observations, observation_spaces, action_spaces):
        super().__init__()
        self._observations = observations
        self.observation_spaces = observation_spaces

        self.agents = [x for x in observation_spaces.keys()]
        self.possible_agents = self.agents[:]
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.reset()
        self.action_spaces = action_spaces

        self.rewards = {a: 1 for a in self.agents}
        self.dones = {a: False for a in self.agents}
        self.infos = {a: {} for a in self.agents}
        self.steps = 0

    def seed(self, seed=None):
        pass

    def observe(self, agent):
        return self._observations[agent]

    def step(self, action, observe=True):
        if self.dones[self.agent_selection]:
            self._was_done_step(action)
        self.agent_selection = self._agent_selector.next()
        self.steps += 1
        if self.steps > 10:
            self.dones = {a: True for a in self.agents}

        self._dones_step_first()

    def reset(self, observe=True):
        self.agents = self.possible_agents[:]
        self.agent_selection = self._agent_selector.reset()

    def close(self):
        pass
