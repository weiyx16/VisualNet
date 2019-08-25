import os
import sys
def mkdir_safe(paths):
    if isinstance(paths, list):
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)
    else:
        if not os.path.exists(paths):
            os.makedirs(paths)

# def merge_dict_3(dict1, dict2):
#     res = {**dict1, **dict2}
#     return res

def merge_dict_2(dict1, dict2):
    z = dict1.copy()  # start with x's keys and values
    z.update(dict2)  # modifies z with y's keys and values & returns None
    return z