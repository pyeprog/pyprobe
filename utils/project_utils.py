import os
from collections import Counter
from config.types import InjectionType, file_to_injection_type

def get_filename_list_recursively(path: str) -> list:
    if not os.path.isdir(path):
        return []
    dir_list = os.listdir(path)
    res = []
    for name in dir_list:
        if os.path.isfile(name):
            res.append(name)
        elif os.path.isdir(name):
            res.extend(get_filename_list_recursively(name))
    return res

def get_project_type(path: str):
    filename_list = get_filename_list_recursively(path)
    file_type_count = {}
    counter = Counter()
    for filename in filename_list:
        print(filename.lower().split(".")[-1])
        cur_type = file_to_injection_type.get(filename.lower().split(".")[-1])
        counter[cur_type] += 1

    print(counter)
    return counter.most_common()[0][0]
