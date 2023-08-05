# picorg
[![Build Status](https://img.shields.io/pypi/v/picorg.svg?style=flat)](https://img.shields.io/pypi/v/picorg.svg?style=flat)
[![Build Status](https://travis-ci.com/frangiz/picorg.svg?branch=master)](https://travis-ci.com/frangiz/picorg)
[![Build Status](https://img.shields.io/github/license/frangiz/picorg.svg)](https://img.shields.io/github/license/frangiz/picorg.svg)

A set of scripts to organize pictures. It is ideal if you save your images in different locations on your hard drives and manually backup your images from your phone.

## Installation
```python
pip install picorg
```

## Usage
```python
# Renames all images in the current working directory and its subdirectories. It tries to use the timestamp of when the image was taken from the EXIF data. If the script cannot find a suitable name for a file, it will be moved to a **NOK** folder and the filename will be printed to the console.
picorg -a rename

# Checks all files in current working dir for files with the same content. If two files has the same content,
# the one with the "biggest" name is moved to a *duplicates* folder. It then traverses all the files in
# all the directories listed in pic_paths (in the settings file). If a file matches by name and content,
# the file in current working dir will be moved to the *duplicates* folder.
picorg -a duplicates
```

## Configuration
A settings file is created in <USER_HOME>/.picorg that stores the users settings.

## Developing
Install dependencies from the requirements-dev.txt file
```python
pip install -r requirements-dev.txt
```

Create a package and install with
```python
python setup.py bdist_wheel sdist
pip install -e .
```

Run tests with
```python
pytest --cov=src --cov-report html .
```
or using tox
```
tox
```

### Before commit
Run the script `pre-commit.sh` before any commits on order to be consistent with formatting and having sorted imports.

## Creating a new version.
* Create a new version by bumping the version in setup.py.
* Commit and push.
* Wait for Travis CI to build.
* Create a tag in git and push.
* Wait for Travis CI to build the tag.
* Push the new package to pypi using `twine upload dist/*`