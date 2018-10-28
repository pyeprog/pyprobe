import os

from config.local_config import *
from collections import Counter


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

