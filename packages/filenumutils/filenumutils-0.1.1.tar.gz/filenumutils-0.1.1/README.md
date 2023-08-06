# filenumutils

![Pypi version](https://img.shields.io/pypi/v/filenumutils)
![Wheel Status](https://img.shields.io/pypi/wheel/filenumutils)
![Pypi Licence](https://img.shields.io/pypi/l/filenumutils)

Python tools for finding last file or folder number in a directory based on extension, prefix or suffix.

## Installation

Simply install using `pip`

```sh
pip install filenumutils
```

## Usage

If your current directory has the following files and folders

- folders: [`train_00`, `train_01`, `train_02`, `train_03`, `train_04`]
- files: [`model_00.py`, `model_01.py`, `model_02.py`]

### Get Last Folder / File Number

```python
from filenumutils import get_last_folder_number, get_last_file_number
get_last_folder_number(prefix="model_")       # Output: 4
get_last_file_number(prefix="train_")         # Output: 2
```

If no such file/folder with given prefix exists, it outputs -1

### Get Next Folder / File Name

```python
from filenumutils import get_next_file, get_next_folder
get_next_file(prefix="model_")                      # Output: model_03.py
get_next_folder(prefix="train_", create=True)       # Output: train_05 (Folder is created)
get_next_folder(prefix="test_", create=True)        # Output: test_00 (Folder is created)
```

If no such folder with given prefix exists, it outputs `prefix_00`. 

Also, it will automatically stick to the existing numbering pattern. 
For eg, if the folders were [`train_0000`, `train_0001`], 
```python
get_next_folder(prefix="train_", create=True)       # Output: train_0000 (Folder is created)
``` 

### More Options

| Attribute | Default | Description |
| --- | --- | --- |
| `path` | Current Directory | Do operations in the given directory |
| `prefix` | "" | Match only files with given prefix |
| `suffix` | "" | Match only files with given extension/suffix |
| `default_number_width` | 2 | When no numbering pattern is found, output number will be `default_number_width` digits |
| `return_with_path` | True | By default, return `path/new_folder_name`. If false, return only `new_folder_name`.  |

## Contributing

Pull requests are very welcome.

1. Fork the repo
1. Create new branch with feature name as branch name
1. Check if things work with a jupyter notebook
1. Raise a pull request

## Licence

Please see attached [Licence](LICENCE) 