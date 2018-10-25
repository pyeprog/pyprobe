import os
import sys
import _pickle as pkl
import matplotlib.pyplot as plt
from time import time, sleep
from enum import Enum, auto
from shutil import copytree, rmtree
from collections import Counter
from watchgod import watch, Change
from geopandas import GeoSeries


PROBE_RESULT_DIR = os.path.join(os.path.realpath("."), "probe_result")
PYTHON_PROBE = "pyprobe"
JAVA_PROBE = "javaprobe"

class ProjectType(Enum):
    PYTHON = auto()
    JAVA = auto()
    NONE = auto()

postfix_project_type_mapping = {
        "py"        :   ProjectType.PYTHON,
        "pyc"       :   ProjectType.PYTHON,
        "java"      :   ProjectType.JAVA,
        }

project_type_injector_name_mapping = {
        ProjectType.PYTHON  :   PYTHON_PROBE,
        ProjectType.JAVA    :   JAVA_PROBE,
        }

project_type_injector_mapping = {
        ProjectType.PYTHON  :   os.path.join(os.path.realpath("."), "injector", PYTHON_PROBE),
        ProjectType.JAVA    :   os.path.join(os.path.realpath("."), "injector", JAVA_PROBE),
        }


def list_files_recursively(path):
    if not os.path.isdir(path):
        return []
    res = []
    for name in os.listdir(path):
        file_path = os.path.join(path, name)
        if os.path.isfile(file_path):
            res.append(file_path)
        elif os.path.isdir(file_path):
            res.extend(list_files_recursively(file_path))

    return res

def get_project_type(path):
    file_list = list_files_recursively(path)
    counter = Counter()
    for filename in file_list:
        file_postfix = filename.split(".")[-1]
        counter[file_postfix] += 1

    common_postfixes = counter.most_common()
    if len(common_postfixes) > 0:
        most_common_postfix = counter.most_common()[0][0].lower()
        project_type = postfix_project_type_mapping.get(most_common_postfix, ProjectType.NONE)
    else:
        project_type = ProjectType.NONE
    return project_type

def process(filepath):
    if os.path.getsize(filepath) > 0:
        with open(filepath, 'rb') as fp:
            data_content = pkl.load(fp)
            render_one_by_one(data_content)

def render(data_content):
    GeoSeries(data_content).plot(ax=plt.gca())
    plt.show()

def render_one_by_one(data_content):
    if hasattr(data_content, "__iter__"):
        for data in data_content:
            GeoSeries(data).plot(ax=plt.gca())
            plt.show()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        raise ValueError("injection path is not specified")

    inject_target_dir = os.path.expanduser(sys.argv[1])
    if not os.path.isdir(inject_target_dir):
        raise ValueError("Invalid injection path")

    project_type = get_project_type(inject_target_dir)
    injector_path = project_type_injector_mapping.get(project_type, "")

    if injector_path == "":
        raise ValueError("No injector matches")

    inject_target_path = os.path.join(inject_target_dir, project_type_injector_name_mapping[project_type])
    if os.path.isdir(inject_target_path):
        rmtree(inject_target_path)
    copytree(injector_path, inject_target_path)

    print("watching file changing")

    try:
        while True:
            sleep(1)
            for changes in watch(PROBE_RESULT_DIR):
                changes = list(changes)
                for change in changes:
                    op_type = change[0]
                    filename = change[1]
                    if op_type == Change.added or op_type == Change.modified:
                        process(filename)
    except KeyboardInterrupt:
        try:
            rmtree(inject_target_path)
            print("The probe is removed from {}".format(inject_target_dir))
        except:
            print("The probe is not removed, please remove it manually")

