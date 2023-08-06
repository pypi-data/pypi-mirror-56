from abc import ABCMeta, abstractmethod
from typing import List, NamedTuple


class CommandData(NamedTuple):
    name: str
    user: str
    cwd: str
    command: List[str]


class CommandRepository(metaclass=ABCMeta):
    @abstractmethod
    def save_command(self, name: str, user: str, cwd: str, command: List[str]):
        pass

    @abstractmethod
    def get_command(self, name: str) -> CommandData:
        pass

    @abstractmethod
    def get_all_commands(self) -> List[CommandData]:
        pass

    @abstractmethod
    def delete_command(self, name: str):
        pass

    def copy_data(self, from_repository: 'CommandRepository'):
        for command in from_repository.get_all_commands():
            self.save_command(command.name, command.user, command.cwd, command.command)

