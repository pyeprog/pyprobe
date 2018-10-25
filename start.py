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

from utils.local_utils import list_files_recursively, get_project_type
from config.local_config import *

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

