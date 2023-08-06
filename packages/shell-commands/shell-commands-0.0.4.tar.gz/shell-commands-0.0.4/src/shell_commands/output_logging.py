from abc import ABCMeta, abstractmethod
from pathlib import Path
from uuid import UUID

from shell_commands.utils import RunCommandOutput


class OutputRepository(metaclass=ABCMeta):
    @abstractmethod
    def store_output(self, result_data: RunCommandOutput, run_id: UUID):
        pass


class DefaultOutputRepository(OutputRepository):
    def __init__(self, output_directory:  Path):
        super(DefaultOutputRepository, self).__init__()
        self.output_directory = output_directory

    def store_output(self, result_data: RunCommandOutput, run_id: UUID):
        result_data.stdout.to_csv(self.output_directory / f'{run_id.hex}.stdout.csv')
        result_data.stderr.to_csv(self.output_directory / f'{run_id.hex}.stderr.csv')
