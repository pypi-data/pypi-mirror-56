from setuptools import setup

setup(
    name='shell-commands',
    version='0.0.4',
    packages=['shell_commands'],
    package_dir={
        'shell_commands': 'src/shell_commands',
    },
    url='https://gitlab.com/Mussche/shell-commands',
    license='MIT',
    author='Klaas Mussche',
    author_email='klaasmussche@gmail.com',
    description='Command DataBase',
    install_requires=[
        'click',
        'click-log',
        'tabulate',
        'spur',
        'sqlalchemy',
    ],
    entry_points={
        'console_scripts': [
            'commands = shell_commands.__main__:main',
        ]
    },
)
