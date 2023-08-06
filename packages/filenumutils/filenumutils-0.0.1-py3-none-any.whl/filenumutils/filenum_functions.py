import os
import re


# All directories are files, but not all files are directories
def get_last_file_number(path=None, prefix='', extension='', folder=False):

    if path is None:
        path = os.getcwd()

    index = 1 if folder else 2
    fs_objects = next(os.walk(path))[index]

    r = re.compile(prefix + '([0-9]+)' + '.*' + extension + '$')
    matches = list(map(r.match, fs_objects))
    matches = list(filter(lambda x: x is not None, matches))

    numbers_list = [int(match.group(1)) for match in matches]
    return max(numbers_list) if len(numbers_list) > 0 else -1


# For those files that are directories
# suffix untested
def get_last_folder_number(path=None, prefix='', suffix=''):
    return get_last_file_number(path=path, prefix=prefix, extension=suffix, folder=True)
