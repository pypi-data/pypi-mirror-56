import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Iterator
from uuid import UUID

from shell_commands.commands import CommandRepository, CommandData
from shell_commands.history import HistoryRepository, HistoryEntry
from shell_commands.packages import PackageRepository
from shell_commands.utils import RunCommandOutput, serialize_datetime, deserialize_datetime


class JSONRepository(CommandRepository, PackageRepository, HistoryRepository):
    SCHEMA_VERSION = 3

    def __init__(self, dbfile: Path):
        super(JSONRepository, self).__init__()
        self.dbfile = dbfile
        if not self.dbfile.exists():
            self._write({
                'schemaVersion': self.SCHEMA_VERSION,
                'commands': {},
                'packages': [],
                'history': [],
            })

    def _load(self) -> dict:
        with self.dbfile.open('r') as fp:
            data = json.load(fp)
        assert 'schemaVersion' in data
        if data['schemaVersion'] != self.SCHEMA_VERSION:
            if data['schemaVersion'] == 1:
                # Upgrade from schema 1 to 2
                data['packages'] = []
                data['schemaVersion'] = 2
            if data['schemaVersion'] == 2:
                data['history'] = []
                data['schemaVersion'] = 3
            assert data['schemaVersion'] == self.SCHEMA_VERSION
            self._write(data)
        return data

    def _write(self, data: dict):
        with self.dbfile.open('w') as fp:
            json.dump(data, fp, indent=2)

    def save_command(self, name: str, user: str, cwd: str, command: List[str]):
        data = self._load()
        assert name not in data['commands'], 'Command with this name already exists'
        data['commands'][name] = {
            'user': user,
            'cwd': cwd,
            'command': command,
        }
        self._write(data)

    def get_command(self, name: str) -> CommandData:
        data = self._load()
        assert name in data['commands'], 'Command with this name does not exist'
        user = data['commands'][name]['user']
        cwd = data['commands'][name]['cwd']
        command = data['commands'][name]['command']
        return CommandData(name=name, user=user, cwd=cwd, command=command)

    def get_all_commands(self) -> List[CommandData]:
        return [self.get_command(name) for name in self._load()['commands'].keys()]

    def delete_command(self, name: str):
        data = self._load()
        assert name in data['commands'], 'Command with this name does not exist'
        del data['commands'][name]
        self._write(data)

    def require_package(self, name: str):
        data = self._load()
        assert name not in data['packages'], 'Package is already required so cannot require again'
        data['packages'].append(name)
        self._write(data)

    def get_required_packages(self) -> List[str]:
        data = self._load()
        return data['packages']

    def unrequire_package(self, name: str):
        data = self._load()
        assert name in data['packages'], 'Package is not required so cannot unrequire'
        data['packages'].remove(name)
        self._write(data)

    def write_to_history(self, entry: HistoryEntry):
        data = self._load()
        data['history'].append({
            'id': entry.id.hex,
            'timestamp': serialize_datetime(entry.timestamp),
            'command_name': entry.command_name,
            'command': entry.command,
            'cwd': entry.cwd,
            'user': entry.user,
            'return_code': entry.return_code,
        })
        self._write(data)


    def iterate_history(self) -> Iterator[HistoryEntry]:
        for entry in self._load()['history']:
            yield HistoryEntry(
                id=UUID(hex=entry['id']),
                timestamp=deserialize_datetime(entry['timestamp']),
                command_name=entry['command_name'],
                command=entry['command'],
                cwd=entry['cwd'],
                user=entry['user'],
                return_code=entry['return_code'],
            )