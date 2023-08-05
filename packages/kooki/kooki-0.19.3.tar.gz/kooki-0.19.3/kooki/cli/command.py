import argparse
import sys

from karamel.command import (Command, InstallCommand, ListCommand,
                             SearchCommand, UninstallCommand, UpdateCommand)
from kooki.cli import BakeCommand
from kooki.config import get_kooki_dir_jars, get_kooki_jar_manager
from kooki.version import __version__

__program__ = "kooki"
__description__ = "Generate any kind of documents."

class KookiCommand(Command):
    def __init__(self):
        super(KookiCommand, self).__init__(__program__, __description__)
        self.add_argument(
            "-v",
            "--version",
            help="Show program's version number and exit.",
            action="store_true",
        )
        self.add_argument(
            "-h",
            "--help",
            action="help",
            default=argparse.SUPPRESS,
            help="Show this help message and exit.",
        )

        self.add_command(BakeCommand())

        package_manager_url = get_kooki_jar_manager()
        package_install_dir = get_kooki_dir_jars()

        self.add_command(SearchCommand(package_manager_url))
        self.add_command(InstallCommand(package_manager_url, package_install_dir))
        self.add_command(UninstallCommand(package_manager_url, package_install_dir))
        self.add_command(UpdateCommand(package_manager_url, package_install_dir))
        self.add_command(ListCommand(package_manager_url, package_install_dir))

    def callback(self, args):
        show_version(args)


def show_version(args):
    if args.version:
        print("{0} {1}\nPython {2}".format(__program__, __version__, sys.version))
        raise SystemExit(0)


def run():
    try:
        command = KookiCommand()
        command.run()

    except (KeyboardInterrupt, SystemExit):
        pass
