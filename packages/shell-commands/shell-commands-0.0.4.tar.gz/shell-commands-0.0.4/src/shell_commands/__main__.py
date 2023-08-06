import os
from collections import OrderedDict
from pathlib import Path
from typing import List, Optional
from uuid import UUID

import click
import logging

import pwd

import click_log
from tabulate import tabulate

from shell_commands.jsondb import JSONRepository
from shell_commands.output_logging import DefaultOutputRepository
from shell_commands.sqlitedb import RDBMSCommandRepository, RDBMSHistoryRepository, RDBMSPackageRepository, Database
from shell_commands.utils import run_command, OutputData

logger = logging.getLogger('commands')
click_log.basic_config(logger)


class App(object):
    def __init__(self, config_dir: Path):
        super(App, self).__init__()
        self.config_dir = config_dir
        if not config_dir.exists():
            self.config_dir.mkdir(mode=0o755, parents=True)
        self.output_directory = self.config_dir / 'output'
        if not self.output_directory.exists():
            self.output_directory.mkdir(mode=0o755, parents=True)
        self.output_logger = DefaultOutputRepository(self.output_directory)
        sqlitedb = self.config_dir / 'db.sqlite'
        sqlalchemy_url = f'sqlite:///{sqlitedb}'
        self.db = Database(sqlalchemy_url)
        self.command_repository = RDBMSCommandRepository(self.db)
        self.history_repository = RDBMSHistoryRepository(self.db)
        self.package_repository = RDBMSPackageRepository(self.db)
        dbfile = self.config_dir / 'db.json'
        if dbfile.exists():
            jsondb = JSONRepository(dbfile)
            self.command_repository.copy_data(jsondb)
            self.history_repository.copy_from(jsondb)
            self.package_repository.copy_from(jsondb)
            logger.info('Imported data from JSON into SQLite')
            dbfile.rename(self.config_dir / 'db.json.old')


@click.group(help='Utility for maintaining and using a carefully curated list of personal commands')
@click_log.simple_verbosity_option(logger)
@click.pass_context
def main(ctx: click.Context):
    config_dir = Path(click.get_app_dir('commands'))
    ctx.obj = App(config_dir)


@main.command(help='Save a command with given name', context_settings=dict(
    ignore_unknown_options=True,
))
@click.pass_obj
@click.option('--user', '-u', help='User as which this command should be run, defaults to current user', default=None)
@click.option('--cwd', '-c', type=click.Path(dir_okay=True, exists=True), help='Working directory for this command, defaults to current directory')
@click.argument('name', type=click.STRING, nargs=1)
@click.argument('command', type=click.UNPROCESSED, nargs=-1)
def save(app: App, user: Optional[str], cwd: Optional[str], name: str, command: List[str]):
    if user is None:
        user = pwd.getpwuid(os.getuid()).pw_name
    if cwd is None:
        cwd = os.getcwd()
    logger.info('Saving a command:')
    logger.info('Name:    {}'.format(name))
    logger.info('Cwd:     {}'.format(cwd))
    logger.info('User:    {}'.format(user))
    logger.info('Command: {!r}'.format(command))
    app.command_repository.save_command(name=name, user=user, cwd=cwd, command=command)


@main.command(help='Run a command')
@click.pass_obj
@click.argument('name', type=click.STRING)
def run(app: App, name: str):
    data = app.command_repository.get_command(name)
    result = run_command(data.command, data.user, data.cwd)
    run_id = app.history_repository.log_run(data, result)
    app.output_logger.store_output(result, run_id)


@main.command('list', help='List all commands')
@click.pass_obj
def list_commands(app: App):
    header = ['name', 'user', 'cwd', 'command']
    data = [(d.name, d.user, d.cwd, ' '.join(d.command)) for d in app.command_repository.get_all_commands()]
    print(tabulate(data, headers=header))


@main.command(help='Show details of a command')
@click.pass_obj
@click.argument('name', type=click.STRING)
def show(app: App, name: str):
    data = app.command_repository.get_command(name)
    click.echo('name:    {}'.format(name))
    click.echo('user:    {}'.format(data.user))
    click.echo('cwd:     {}'.format(data.cwd))
    click.echo('command: {}'.format(' '.join(data.command)))


@main.command(help='Delete a command')
@click.pass_obj
@click.argument('name', type=click.STRING)
def delete(app: App, name: str):
    app.command_repository.delete_command(name)


@main.group(help='APT Package management')
def apt():
    pass


@apt.command('require', help='Mark a package as required')
@click.argument('name', type=click.STRING)
@click.pass_obj
def apt_require(app: App, name: str):
    app.package_repository.require_package(name)


@apt.command('unrequire', help='Unmark a package as required')
@click.argument('name', type=click.STRING)
@click.pass_obj
def apt_unrequire(app: App, name: str):
    app.package_repository.unrequire_package(name)


@apt.command('list', help='List all required packages')
@click.pass_obj
def apt_list(app: App):
    for name in app.package_repository.get_required_packages():
        click.echo(name)


@apt.command('apply', help='Install all required packages')
@click.pass_obj
def apt_apply(app: App):
    names = app.package_repository.get_required_packages()
    command = ['apt', 'install', '-y', *names]
    run_command(command, 'root')


@main.command('history', help='Show run history')
@click.pass_obj
@click.option('--simple', is_flag=True)
def history(app: App, simple: bool):
    data = OrderedDict()
    if not simple:
        data['ID'] = list()
        data['Date'] = list()
    data['Name'] = list()
    data['Command'] = list()
    data['Directory'] = list()
    data['User'] = list()
    data['Return code'] = list()
    for row in app.history_repository.iterate_history():
        if not simple:
            data['ID'].append(row.id)
            data['Date'].append(row.timestamp)
        data['Name'].append(row.command_name)
        data['Command'].append(repr(' '.join(row.command)))
        data['Directory'].append(row.cwd)
        data['User'].append(row.user)
        data['Return code'].append(row.return_code)
    print(tabulate(data, headers=data.keys()))


@main.command('logs', help='Show logged output')
@click.pass_obj
@click.option('--stdout', '-o', is_flag=True)
@click.option('--stderr', '-e', is_flag=True)
@click.option('--annotated', '-a', is_flag=True)
@click.argument('id', type=click.UUID)
def logs(app: App, id: UUID, stdout: bool, stderr: bool, annotated: bool):
    if not stdout and not stderr:
        stdout = True
        stderr = True
    data = OutputData()
    if stdout:
        data = OutputData.combine(data, OutputData.from_csv(app.output_directory / f'{id.hex}.stdout.csv'))
    if stderr:
        data = OutputData.combine(data, OutputData.from_csv(app.output_directory / f'{id.hex}.stderr.csv'))
    if annotated:
        data.print_table()
    else:
        data.print_raw()

if __name__ == '__main__':
    main()