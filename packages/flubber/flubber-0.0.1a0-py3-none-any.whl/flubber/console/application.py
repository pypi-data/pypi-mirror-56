from cleo import Application as BaseApplication

from flubber.console.commands.startproject import StartProjectCommand
from flubber.console.commands.version import VersionCommand


class Application(BaseApplication):
    def __init__(self):
        super(Application, self).__init__()
        commands = [StartProjectCommand(), VersionCommand()]
        self.add_commands(*commands)


if __name__ == "__main__":
    Application().run()
