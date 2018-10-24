import os
import sys
from time import time
from enum import Enum, auto
from shutil import copytree, rmtree
from collections import Counter
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler 

PROBE_RESULT_DIR = os.path.join(__file__, "probe_result")

class ProjectType(Enum):
    PYTHON = auto()
    JAVA = auto()
    TEST = auto()

postfix_project_type_mapping = {
        "py"        :   ProjectType.PYTHON,
        "pyc"       :   ProjectType.PYTHON,
        "java"      :   ProjectType.JAVA,
        }

project_type_injector_mapping = {
        ProjectType.PYTHON  :   os.path.join(__file__, "injector", "pyprobe"),
        ProjectType.JAVA    :   os.path.join(__file__, "injector", "javaprobe"),
        }


def list_files_recursively(path):
    if not os.path.isdir(path):
        return []
    res = []
    for file_path in os.listdir(path):
        if os.path.isfile(file_path):
            res.append(file_path)
        elif os.path.isdir(file_path):
            cur_dir = os.path.dirname(path)
            res.extend(list_files_recursively(os.path.join(cur_dir, file_path)))

    return res

def get_project_type(path):
    file_list = list_files_recursively(path)
    counter = Counter()
    for filename in file_list:
        file_postfix = filename.split(".")[-1]
        counter[file_postfix] += 1

    most_common_postfix = counter.most_common()[0][0].lower()
    project_type = postfix_project_type_mapping.get(most_common_postfix, ProjectType.TEST)
    return project_type


class FileHandler(PatternMatchingEventHandler):
    patterns = ["*.pkl"]

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        raise ValueError("injection path is not specified")

    inject_target_path = sys.argv[1]
    if not os.path.isdir(inject_target_path):
        raise ValueError("Invalid injection path")

    project_type = get_project_type(inject_target_path)
    injector_path = project_type_injector_mapping.get(project_type, "")

    if injector_path == "":
        raise ValueError("No injector matches")

    copytree(injector_path, inject_target_path)

    # begin watching
    observer = Observer()
    observer.schedule(FileHandler(), path=PROBE_RESULT_DIR)
    observer.start()
    
    prev_time = time()

    try:
        while True:
            time.sleep(1)
            now_time = time()
            print("watching for {}s ...".format(now_time - prev_time))
            prev_time = now_time
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


