from enum import Enum, unique, auto

@unique
class InjectionType(Enum):
    PYTHON      = auto()
    JAVA        = auto()
    JAVASCRIPT  = auto()


file_to_injection_type = {
        "py"   :   InjectionType.PYTHON,
        "pyc"  :   InjectionType.PYTHON,
        "js"   :   InjectionType.JAVASCRIPT,
        "java" :   InjectionType.JAVA
        }
