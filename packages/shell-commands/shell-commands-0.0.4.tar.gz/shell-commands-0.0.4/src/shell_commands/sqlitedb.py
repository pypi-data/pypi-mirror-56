from contextlib import contextmanager
from typing import List, Iterator

from sqlalchemy import create_engine, func
from sqlalchemy.engine import Engine, RowProxy
from sqlalchemy.orm import Session, sessionmaker

from shell_commands.commands import CommandRepository, CommandData
from shell_commands.history import HistoryRepository, HistoryEntry
from shell_commands.model import Command, LogEntry, RequiredPackage, DatabaseRevision, Base
from shell_commands.packages import PackageRepository


class Database(object):
    CURRENT_VERSION = 1

    def __init__(self, sqlalchemy_url: str):
        super(Database, self).__init__()
        self.engine: Engine = create_engine(sqlalchemy_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

        revision_table_exists = self.engine.dialect.has_table(self.engine, DatabaseRevision.__tablename__)

        if not revision_table_exists:
            # New, empty database: just create all the tables and set this to be the current version
            Base.metadata.bind = self.engine
            Base.metadata.create_all()
            with self as session:
                session.add(DatabaseRevision(version = self.CURRENT_VERSION))

        # And ensure we have the correct version
        with self as session:
            current_version = session.query(func.max(DatabaseRevision.version)).scalar()
            assert current_version == self.CURRENT_VERSION


    def __enter__(self) -> Session:
        assert self.session is None
        self.session = self.Session()
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()
        self.session = None


class RDBMSCommandRepository(CommandRepository):
    def __init__(self, db: Database):
        super(RDBMSCommandRepository, self).__init__()
        self.db = db

    def save_command(self, name: str, user: str, cwd: str, command: List[str]):
        with self.db as session:
            cmd = Command(
                name = name,
                active = True,
                cwd = cwd,
                user = user,
                command = command,
            )
            session.add(cmd)

    @staticmethod
    def _row_to_data(row: RowProxy) -> CommandData:
        return CommandData(name=row.name,
                           user=row.user,
                           cwd=row.cwd,
                           command=row.command)

    def get_command(self, name: str) -> CommandData:
        with self.db as session:
            assert isinstance(name, str)
            row = session.query(Command).filter(Command.name == name).one()
            return self._row_to_data(row)

    def get_all_commands(self) -> List[CommandData]:
        with self.db as session:
            results = session.query(Command).filter(Command.active == True)
            return [self._row_to_data(row) for row in results]

    def delete_command(self, name: str):
        with self.db as session:
            assert isinstance(name, str)
            row = session.query(Command).filter(Command.name == name).one()
            row.active = False



class RDBMSHistoryRepository(HistoryRepository):
    def __init__(self, db: Database):
        super(RDBMSHistoryRepository, self).__init__()
        self.db = db

    def iterate_history(self) -> Iterator[HistoryEntry]:
        with self.db as session:
            for row in session.query(LogEntry):
                yield HistoryEntry(id = row.uuid,
                                   timestamp = row.datetime,
                                   command_name = row.command.name,
                                   command = row.command.command,
                                   cwd = row.command.cwd,
                                   user = row.command.user,
                                   return_code = row.return_code)

    def write_to_history(self, entry: HistoryEntry):
        with self.db as session:
            session.add(LogEntry(
                uuid = entry.id,
                command_id = session.query(Command).filter(Command.name == entry.command_name).one().id,
                datetime = entry.timestamp,
                return_code = entry.return_code,
            ))


class RDBMSPackageRepository(PackageRepository):
    def __init__(self, db: Database):
        super(RDBMSPackageRepository, self).__init__()
        self.db = db

    def require_package(self, name: str):
        with self.db as session:
            session.add(RequiredPackage(name=name))

    def get_required_packages(self) -> List[str]:
        with self.db as session:
            return [row.name for row in session.query(RequiredPackage).all()]

    def unrequire_package(self, name: str):
        with self.db as session:
            pkg = session.query(RequiredPackage).filter(RequiredPackage.name == name).one()
            session.delete(pkg)
