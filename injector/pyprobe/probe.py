import os
import json
import _pickle as pkl
from random import random

config = {}
with open(os.path.join(os.path.realpath("./pyprobe"), "config.json"), "r") as fp:
    config = json.loads(fp.read())

def dump(obj):
    uid = str(random())[2:12]
    filename = uid + '.pkl'
    try:
        with open(os.path.join(config["probe_result_dir"], filename), "wb") as fp:
            pkl.dump(obj, fp)
        return True
    except:
        return False
