from cleo import Command

from flubber import __version__


class VersionCommand(Command):

    name = "version"
    description = "Get flubber version"

    def handle(self) -> None:
        self.line(f"Flubber <error>v{__version__}</>")
