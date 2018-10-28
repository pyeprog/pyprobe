import os
from enum import Enum, unique


PYTHON_PROBE = "pyprobe"
JAVA_PROBE = "javaprobe"
PROBE_RESULT_DIR = os.path.join(os.path.realpath("."), "probe_result")

@unique
class ProjectType(Enum):
    PYTHON = 1
    JAVA = 2
    NONE = 3

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


