# Shell Commands
This package provides the `commands` command, a utility for saving frequently-used Linux shell commands in a personal database.

## Installation

    pip install shell-commands


## Usage
See the integrated help function:

    commands --help
    
# Status
This package is still under development. 
    
# Description
Features marked with [TODO] still have to be implemented.

* Easy save, list and run frequently used shell commands
  * Each command has a unique name
  * For each command it is stored as which user it need to execute, and from which directory
* A history of command runs is kept, and output of all runs is stored.
* It is possible to specify packages that have to be installed on the system, and also possible
  to easily ensure that all required packages are installed.
  * For now, supports only APT packages.
  * Should be extended to other package managers, but most notably pip packages.
* [TODO] Supports managing multiple hosts from a single management machine.
* [TODO] Supports data generation commands
* [TODO] Supports tracking and management of git repositories.
* [TODO] Supports for a 'managed' mode where it will only emit commands that the system believes to be necessary.

