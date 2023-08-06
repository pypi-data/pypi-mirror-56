from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import NamedTuple, List, Iterator, Optional
from uuid import UUID, uuid4

from shell_commands.commands import CommandData
from shell_commands.utils import RunCommandOutput


class HistoryEntry(NamedTuple):
    id: UUID
    timestamp: datetime
    command_name: str
    command: List[str]
    cwd: str
    user: str
    return_code: int


class HistoryRepository(metaclass=ABCMeta):
    def log_run(self, command_data: CommandData, result_data: RunCommandOutput) -> UUID:
        run_id = uuid4()
        entry = HistoryEntry(
            id = run_id,
            timestamp=datetime.now(),
            command_name=command_data.name,
            command=command_data.command,
            cwd=command_data.cwd,
            user=command_data.user,
            return_code=result_data.return_code,
        )
        self.write_to_history(entry)
        return run_id

    @abstractmethod
    def iterate_history(self) -> Iterator[HistoryEntry]:
        pass

    @abstractmethod
    def write_to_history(self, entry: HistoryEntry):
        pass

    def copy_from(self, from_repository: 'HistoryRepository'):
        for entry in from_repository.iterate_history():
            self.write_to_history(entry)

