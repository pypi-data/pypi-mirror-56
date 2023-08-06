from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, \
    Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from shell_commands.utils import GUID, JSONType

Base = declarative_base()


class DatabaseRevision(Base):
    __tablename__ = '_revisions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(Integer, unique=True)


class Command(Base):
    __tablename__ = 'commands'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    cwd = Column(String, nullable=False)
    user = Column(String, nullable=False)
    command = Column(JSONType, nullable=False)
    history = relationship('LogEntry', backref='command')
    unique_name = Index('unique_name', name,
                unique=True,
                sqlite_where=(active))

    def __str__(self):
        return f'Command<id={self.id}, name={self.name}, active={self.active}, cwd={self.cwd}, user={self.user}, command={self.command}>'


class LogEntry(Base):
    __tablename__ = 'log_entry'
    id = Column(Integer, primary_key=True)
    uuid = Column(GUID, unique=True, nullable=False)
    command_id = Column(Integer, ForeignKey('commands.id'))
    datetime = Column(DateTime, nullable=False)
    return_code = Column(Integer, nullable=False)

    def __str__(self):
        return f'LogEntry<id={self.id}, uuid={self.uuid}, datetime={self.datetime}, return_code={self.return_code}>'


class RequiredPackage(Base):
    __tablename__ = 'required_package'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    def __str__(self):
        return f'RequiredPackage<id={self.id}, name={self.name}>'


