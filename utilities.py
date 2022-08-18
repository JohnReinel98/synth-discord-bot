import os
import json

# general functions
def loadJsonFile(filename, mode):
    if os.path.exists(filename):
        f = open(filename, mode, encoding="utf8")
        return json.load(f)
    return FileExistsError

def loadConfig():
    return loadJsonFile("configs/config.json", "r")
