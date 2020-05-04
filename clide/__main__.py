from tooler import Tooler

from .update import update as run_update

tooler = Tooler()


@tooler.command
def update():
    run_update()


if __name__ == "__main__":
    tooler.main()
