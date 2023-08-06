#!/usr/bin/env python3
import os
import subprocess
import tempfile
import venv
from contextlib import contextmanager
from pathlib import Path
from typing import Optional


def verify_equal(output: str, expected_output: str):
    if output != expected_output:
        print(f'Output: {output}')
        print(f'Expected: {expected_output}')
        raise AssertionError('Output not as expected')


def main():
    with tempfile.TemporaryDirectory() as dir:
        root = Path(dir)
        home_dir = root / 'home'
        home_dir.mkdir()
        os.environ['HOME'] = str(home_dir)
        venv_dir = root / 'venv'
        venv.create(venv_dir, with_pip=True)
        pip_executable = venv_dir / 'bin' / 'pip'
        commands_executable = venv_dir / 'bin' / 'commands'
        assert pip_executable.exists()

        def pip_install(package: str, version: Optional[str]=None, staging: bool = False, quiet: bool = True, upgrade: bool = False):
            args = [pip_executable, 'install']
            if quiet:
                args.append('--quiet')
            if upgrade:
                args.append('--upgrade')
            if staging:
                args.extend(['--extra-index-url', 'http://aorus.lan:3120/packages/staging/+simple/', '--trusted-host', 'aorus.lan'])
            if version is not None:
                args.append(f'{package}=={version}')
            else:
                args.append(package)
            subprocess.check_call(args)

        @contextmanager
        def test_version(version: str, staging: bool=False):
            pip_install('shell-commands', version, staging=staging)
            yield
            print(f'Test version {version} done')

        pip_install('pip', upgrade=True)

        with test_version('0.0.1'):
            assert commands_executable.exists()
            output = subprocess.check_output([commands_executable, 'list'])
            verify_equal(output, b'name    user    cwd    command\n------  ------  -----  ---------\n')
            subprocess.check_call([commands_executable, 'save', '--cwd', '/home', '--user', 'user', 'test', 'ls'], stderr=subprocess.PIPE)
            output = subprocess.check_output([commands_executable, 'list'])
            verify_equal(output, b'name    user    cwd    command\n------  ------  -----  ---------\ntest    user    /home  ls\n')

        with test_version('0.0.2'):
            assert commands_executable.exists()
            output = subprocess.check_output([commands_executable, 'list'])
            verify_equal(output, b'name    user    cwd    command\n------  ------  -----  ---------\ntest    user    /home  ls\n')
            subprocess.check_call([commands_executable, 'apt', 'require', 'python3-dev'])
            subprocess.check_call([commands_executable, 'apt', 'require', 'python3-venv'])
            output = subprocess.check_output([commands_executable, 'apt', 'list'])
            verify_equal(output, b'python3-dev\npython3-venv\n')

        with test_version('0.0.3'):
            assert commands_executable.exists()
            output = subprocess.check_output([commands_executable, 'list'])
            verify_equal(output, b'name    user    cwd    command\n------  ------  -----  ---------\ntest    user    /home  ls\n')
            output = subprocess.check_output([commands_executable, 'apt', 'list'])
            verify_equal(output, b'python3-dev\npython3-venv\n')

        with test_version('0.0.4', staging=True):
            assert commands_executable.exists()
            output = subprocess.check_output([commands_executable, 'list'])
            verify_equal(output, b'name    user    cwd    command\n------  ------  -----  ---------\ntest    user    /home  ls\n')
            output = subprocess.check_output([commands_executable, 'apt', 'list'])
            verify_equal(output, b'python3-dev\npython3-venv\n')


if __name__ == '__main__':
    main()