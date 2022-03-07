
from os.path import isfile, isdir

# checks whether the indicated file is a gexf file
def out_file_gexf(string):
    if string.endswith(".gexf"):
        return string
    raise ValueError(string)

# checks whether the indicated file is a json file
def out_file_json(string):
    if string.endswith(".json"):
        return string
    raise ValueError(string)
    
# checks whether the indicated file exists or not,
# and is a json file
def in_file_json(string):
    if isfile(string):
        return out_file_json(string)
    raise FileNotFoundError(string)

# Checks whether the indicated path exists or not
def directory(string):
    if isdir(string):
        return string
    raise NotADirectoryError(string)
