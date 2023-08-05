import abc

from starling.types import ScrapperData, TaskData


class BlueprintScrapper(abc.ABC):
    def __init__(self, data: ScrapperData, deny_actions=None):
        if deny_actions is None:
            deny_actions = []
        self.data = data
        self.deny_actions = deny_actions

        for action in [item for item in self.actions if item not in self.deny_actions]:
            self.data.tasks += self.tasks(action)

    def tasks(self, action):
        return [TaskData(action=action)]

    @property
    @abc.abstractmethod
    def actions(self):
        return []

    @abc.abstractmethod
    def authenticate(self):
        pass
