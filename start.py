import atexit
import time
import sys

# import click
from config.types import InjectionType
from utils.project_utils import get_project_type


class Server():
    def __init__(self, path):
        self.inject_path = path
        self.project_type = get_project_type(path)

    def start(self):
        self.inject()
        atexit.register(self.end)
        while True:
            time.sleep(1)
            print("heart beat")

    def inject(self):
        if len(self.inject_path) == 0:
            raise ValueError("Invalid injection path given")

        print("project type is {}".format(self.project_type))
        print("injection done")


    def end(self):
        print("it's a exit handler")


# @click.command()
# @click.option("-p", "--path", "string", default="")
# def main(path):
#     server = Server(path)
#     server.start()

if __name__ == '__main__':
    path = "." if len(sys.argv) < 2 else sys.argv[1]
    server = Server(path)
    server.start()
