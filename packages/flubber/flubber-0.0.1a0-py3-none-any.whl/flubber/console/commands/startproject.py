from pathlib import Path

from cleo import argument
from cleo import Command
from cleo import option


class StartProjectCommand(Command):

    name = "startproject"
    description = "Create a new flubber project"

    arguments = [argument("name", "The flubber project name.")]

    options = [option("path", None, "The path to create the project at.", flag=False)]

    def handle(self) -> None:
        from .utils import get_flubber_path

        if self.option("path"):
            path = Path(self.option("path")) / Path(self.argument("name"))
        else:
            path = Path.cwd() / Path(self.argument("name"))

        name = self.argument("name")

        if path.exists():
            if list(path.glob("*")):
                # Directory is not empty. Aborting.
                raise RuntimeError(
                    "Destination <fg=yellow>{}</> "
                    "exists and is not empty".format(path)
                )

        self.copy_project_folder(src=get_flubber_path(), dst=path)

        self.line(
            "Created flubber project <info>{}</> in <fg=blue>{}</>".format(
                name, path.relative_to(Path.cwd())
            )
        )

    def copy_project_folder(self, src: str, dst: str) -> None:
        import shutil

        self.line("<info>Creating project ...</>")

        template_project_path = Path(src) / Path("conf/project_template")

        dst_path = Path(dst)
        shutil.copytree(template_project_path, dst_path)
        return
