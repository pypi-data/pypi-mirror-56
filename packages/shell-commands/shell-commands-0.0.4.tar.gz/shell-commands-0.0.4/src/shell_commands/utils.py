import base64
import csv
import io
import json
import os
import pwd
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional, BinaryIO, NamedTuple

import spur
import sys

from sqlalchemy import TypeDecorator, CHAR, VARCHAR
from sqlalchemy.dialects.postgresql import UUID

from tabulate import tabulate
from spur.results import ExecutionResult


class Tee(object):
    def __init__(self, *bufs: BinaryIO):
        super(Tee, self).__init__()
        self.bufs = bufs

    def write(self, data):
        for buf in self.bufs:
            buf.write(data)
            if data == b'\n':
                buf.flush()


class OutputLineData(NamedTuple):
    name: str
    line_start_time: datetime
    line_end_time: datetime
    data: bytes


class OutputData(object):
    def __init__(self):
        super(OutputData, self).__init__()
        self.lines: List[OutputLineData] = list()

    def add_line(self, line: OutputLineData):
        self.lines.append(line)

    def print_table(self):
        headers = ['name', 'start_time', 'duration', 'data']
        data = [(line.name, line.line_start_time, line.line_end_time - line.line_start_time, line.data.decode('utf-8').rstrip()) for line in self.lines]
        print(tabulate(data, headers=headers))

    def print_raw(self):
        for line in self.lines:
            sys.stdout.write_to_history(line.data.decode('utf-8'))

    @staticmethod
    def combine(*data: 'OutputData') -> 'OutputData':
        result = OutputData()
        for buffer in data:
            result.lines.extend(buffer.lines)
        result.lines.sort(key=lambda x: x.line_start_time)
        return result

    def to_csv(self, path: Path):
        with path.open('w') as fp:
            fieldnames = ['name', 'start_time', 'end_time', 'line_data']
            writer = csv.DictWriter(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, fieldnames=fieldnames)
            writer.writeheader()
            for line in self.lines:
                writer.writerow({
                    'name': line.name,
                    'start_time': str(serialize_datetime(line.line_start_time)),
                    'end_time': str(serialize_datetime(line.line_end_time)),
                    'line_data': serialize_bytes(line.data),
                })

    @staticmethod
    def from_csv(path: Path) -> 'OutputData':
        result = OutputData()
        with path.open('r') as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                result.add_line(OutputLineData(
                    name=row['name'],
                    line_start_time=deserialize_datetime(float(row['start_time'])),
                    line_end_time=deserialize_datetime(float(row['end_time'])),
                    data=deserialize_bytes(row['line_data']),
                ))
        return result


class OutputCollector(object):
    def __init__(self, std_buffer: BinaryIO, name: str):
        super(OutputCollector, self).__init__()
        self.std = std_buffer
        self.buffer = OutputData()
        self.cache = io.BytesIO()
        self.t0 = datetime.now()
        self.name = name

    def write(self, data):
        self.std.write(data)
        self.cache.write(data)
        if data == b'\n':
            self.std.flush()
            self.finish_line()

    def finish_line(self):
        t1 = datetime.now()
        self.buffer.add_line(OutputLineData(self.name, self.t0, t1, self.cache.getvalue()))
        self.t0 = t1
        self.cache = io.BytesIO()

    def __enter__(self):
        self.t0 = datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cache.getvalue():
            self.finish_line()


class RunCommandOutput(NamedTuple):
    return_code: int
    stdout: OutputData
    stderr: OutputData

def run_command(command: List[str], user: str, cwd: Optional[str]=None) -> RunCommandOutput:
    current_user = pwd.getpwuid(os.getuid()).pw_name
    actual_command = []
    if user != current_user:
        actual_command.extend(['sudo', '-u', user])
    actual_command.extend(command)
    shell = spur.LocalShell()
    stdout = OutputCollector(sys.stdout.buffer, 'stdout')
    stderr = OutputCollector(sys.stderr.buffer, 'stderr')
    with stdout, stderr:
        execution_result: ExecutionResult = shell.run(actual_command, cwd=cwd, allow_error=True, stdout=stdout, stderr=stderr)
    return RunCommandOutput(execution_result.return_code, stdout.buffer, stderr.buffer)


def serialize_datetime(dt: datetime) -> float:
    return dt.timestamp()


def deserialize_datetime(timestamp: float) -> datetime:
    return datetime.fromtimestamp(timestamp)


def serialize_bytes(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')


def deserialize_bytes(data: str) -> bytes:
    return base64.b64decode(data.encode('utf-8'))


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class JSONType(TypeDecorator):
    impl = VARCHAR

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(VARCHAR())

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)