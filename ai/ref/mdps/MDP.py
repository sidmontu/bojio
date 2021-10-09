from abc import ABC, abstractmethod


class MDP(ABC):
    @abstractmethod
    def getStates(self):
        pass

    @abstractmethod
    def getStartState(self):
        pass

    @abstractmethod
    def getTransitionStatesAndProbs(self, state, action):
        pass

    @abstractmethod
    def getReward(self, state, action, nextState):
        pass

    @abstractmethod
    def isTerminal(self, state):
        pass

    @abstractmethod
    def getPossibleActions(self, state):
        pass
