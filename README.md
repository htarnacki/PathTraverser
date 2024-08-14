# PathTraverser

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Because traversing through files and directories in Python should be as easy and fun as in Groovy.


## Installation

```bash
$ pip install --user --upgrade PathTraverser
```

## Usage

### Basic example of recursively getting a list of all files and directories starting from current working directory
```python
>>> from PathTraverser import Traverser
>>>
>>> paths = list(Traverser())
```
or
```python
>>> from PathTraverser import Traverser
>>>
>>> paths = Traverser().get()
```

### Basic example of recursively iterating through a list of all files and directories, starting from the current working directory and printing their paths
```python
>>> from PathTraverser import Traverser
>>>
>>> for path in Traverser():
>>>     print(str(path))
```
or
```python
>>> from PathTraverser import Traverser
>>>
>>> Traverser().on_each(lambda _: print(str(_))).get()
```

### Advanced example of recursively iterating through a filtered list of all files and directories, starting from the current working directory
```python
>>> from PathTraverser import Traverser
>>>
>>> for path in Traverser(
>>>     0 < depth() < 4,
>>>     files,
>>>     -name('abc.jpg'),
>>>     readonly + hidden,
>>>     ext.jpg + ext.png,
>>>     size() < '1MB'
>>> ):
>>>     print(str(path))
```

### Input arguments
Two main input arguments for Traverser initialization are:
- root directory where iteration should start. This argument is optional and defaults to Path.cwd()
- list of filters which should be applied during iteration. This argument is optional and defaults to empty list of filters
```python
>>> Traverser(root, filter1, filter2, filter3, ...)
```
An iterated path is accepted and returned from the Traverser object only if it satisfies all the given filters.
So in the given example the path is accepted only if it meets the condition: filter1 and filter2 and filter3 and ...

Filters can also be combined in an "or" condition using the sum operation:
```python
>>> Traverser(root, filter1 + filter2 + filter3, filter4, filter5, ...)
```
In the given example the path is accepted only if it meets the condition: (filter1 or filter2 or filter3) and filter4 and filter5...

Filters can also be negated by the minus operator. If a filter is negative, it acts as the opposite filter to its positive counterpart:
```python
>>> Traverser(root, -(filter1 + filter2 + filter3), -filter4, filter5, ...)
```
In the given example the path is accepted only if it meets the condition: not(filter1 or filter2 or filter3) and not(filter4) and filter5...

### List of built in filters
- **files**: accepts only paths that are files or symlinks to files
- **dirs**: accepts only paths that are directories or symlinks to directories
- **symlinks**: accepts only paths that are symlinks
- **ext**: accepts only paths with the specified extensions
- **name**: accepts only paths whose names are equal to any of the given strings or match the given regular expressions or glob patterns
- **path**: accepts only paths that are equal to any of the given strings or match the given regular expressions or glob patterns
- **depth**: accepts only paths that are at the appropriate level of the root directory structure
- **hidden**: accepts only hidden paths
- **executable**: accepts only exacutable paths
- **writeable**: accepts only writeable paths
- **readonly**: accepts only readonly paths
- **owner**: accepts only paths that are owned by the specified person
- **size**: accepts only files whose size falls within the specified range
- **call**: custom callable filter

### Examples of "files" filter
```python
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import files, ext, readonly
>>>
>>> # recursively print all files
>>> for file in Traverser(files):
>>>     print(str(file))
>>>
>>> # recursively print all paths but no files
>>> for path in Traverser(-files):
>>>     print(str(path))
>>>
>>> # recursively print all files
>>> for file in Traverser().files:
>>>     print(str(file))
>>>
>>> # recursively print all files with extension '.txt' and readonly
>>> for file in Traverser().files(ext.txt, readonly):
>>>     print(str(file))
>>>
>>> # recursively get list of all files
>>> files = Traverser().files.get()
```

### Examples of "dirs" filter
```python
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import dirs, name, readonly
>>>
>>> # recursively print all directories
>>> for dir in Traverser(dirs):
>>>     print(str(dir))
>>>
>>> # recursively print all paths but no directories
>>> for path in Traverser(-dirs):
>>>     print(str(path))
>>>
>>> # recursively print all directories
>>> for dir in Traverser().dirs:
>>>     print(str(dir))
>>>
>>> # recursively print all directories with name like given regex and readonly
>>> for dir in Traverser().dirs(name.regex(r'pictures_\d+'), readonly):
>>>     print(str(dir))
>>>
>>> # recursively get list of all directories
>>> dirs = Traverser().dirs.get()
```


### Examples of "symlinks" filter
```python
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import symlinks, name, readonly
>>>
>>> # recursively print all symlinks
>>> for symlink in Traverser(symlinks):
>>>     print(str(symlink))
>>>
>>> # recursively print all paths but no symlinks
>>> for path in Traverser(-symlinks):
>>>     print(str(path))
>>>
>>> # recursively print all symlinks
>>> for symlink in Traverser().symlinks:
>>>     print(str(symlink))
>>>
>>> # recursively print all symlinks with name like given regex and readonly
>>> for symlink in Traverser().symlinks(name.regex(r'.+\.symlink'), readonly):
>>>     print(str(symlink))
>>>
>>> # recursively get list of all symlinks
>>> symlinks = Traverser().symlinks.get()
```


### Examples of "ext" filter
```python
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import ext
>>>
>>> # recursively print all files with extension '.jpg'
>>> for file in Traverser(ext('jpg')):
>>>     print(str(file))
>>>
>>> # recursively print all files with extension '.jpg'
>>> for file in Traverser(ext.jpg):
>>>     print(str(file))
>>>
>>> # recursively print all paths but no files with extension '.jpg' or '.png'
>>> for path in Traverser(-ext('jpg'), -ext.png):
>>>     print(str(path))
>>>
>>> # recursively print all files with extension '.jpg' or '.png' or '.gif'
>>> for file in Traverser(ext('jpg', 'png', 'gif')):
>>>     print(str(file))
>>>
>>> # recursively print all files with extension '.jpg' or '.png' or '.gif'
>>> for file in Traverser(ext.jpg + ext.png + ext.gif):
>>>     print(str(file))
```


### Examples of "name" filter
```python
>>> import re
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import name
>>>
>>> # recursively print all files named 'picture.jpg'
>>> for file in Traverser(name('picture.jpg')):
>>>     print(str(file))
>>>
>>> # recursively print all files named 'picture.jpg'
>>> for file in Traverser(name == 'picture.jpg'):
>>>     print(str(file))
>>>
>>> # recursively print all files named 'picture.jpg' or 'other.jpg'
>>> for file in Traverser(name('picture.jpg', 'other.jpg')):
>>>     print(str(file))
>>>
>>> # recursively print all files named 'picture.jpg' or 'other.jpg'
>>> for file in Traverser(name == ['picture.jpg', 'other.png']):
>>>     print(str(file))
>>>
>>> # recursively print all files named 'picture.jpg' or whose names match the regular expression pattern '.+\.png'
>>> # note: here regex patterns must be of type: re.Pattern. If not, they are treated as normal strings
>>> for file in Traverser(name('picture.jpg', re.compile(r'.+\.png'))):
>>>     print(str(file))
>>>
>>> # recursively print all files named 'picture.jpg' or whose names match the regular expression pattern '.+\.png'
>>> # note: here regex patterns must be of type: re.Pattern. If not, they are treated as normal strings
>>> for file in Traverser(name == ['picture.jpg', re.compile(r'.+\.png')]):
>>>     print(str(file))
>>>
>>> # recursively print all files whose names match the regular expression patterns '.+\.jpg' or '.+\.png' or '.+\.svg'
>>> # note: here regex patterns can be of type: string or re.Pattern. String values ​​are automatically compiled to re.Pattern
>>> for file in Traverser(name.regex(r'.+\.jpg', r'.+\.png', re.compile(r'.+\.svg'))):
>>>     print(str(file))
>>>
>>> # recursively print all files whose names match the glob patterns '*.jpg' or '*.png'
>>> for file in Traverser(name.glob('*.jpg', '*.png')):
>>>     print(str(file))
```


### Examples of "path" filter
```python
>>> import re
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import path
>>>
>>> # recursively print all files that have path '/etc/config.json'
>>> # of course the usefulness of this form of invocation is questionable
>>> for file in Traverser(path('/etc/config.json')):
>>>     print(str(file))
>>>
>>> # recursively print all files that have path '/etc/config.json'
>>> # of course the usefulness of this form of invocation is questionable
>>> for file in Traverser(path == '/etc/config.json'):
>>>     print(str(file))
>>>
>>> # recursively print all files that have path '/etc/config.json' or '/etc/config.yaml'
>>> # of course the usefulness of this form of invocation is questionable
>>> for file in Traverser(path('/etc/config.json', '/etc/config.yaml')):
>>>     print(str(file))
>>>
>>> # recursively print all files that have path '/etc/config.json' or '/etc/config.yaml'
>>> # of course the usefulness of this form of invocation is questionable
>>> for file in Traverser(path == ['/etc/config.json', '/etc/config.yaml']):
>>>     print(str(file))
>>>
>>> # recursively print all files that have path '/etc/config.json' or whose paths match the regular expression pattern '/etc/.*/config\.yaml'
>>> # note: here regex patterns must be of type: re.Pattern. If not, they are treated as normal strings
>>> for file in Traverser(path('/etc/config.json', re.compile(r'/etc/.*/config\.yaml'))):
>>>     print(str(file))
>>>
>>> # recursively print all files that have path '/etc/config.json' or whose paths match the regular expression pattern '/etc/.*/config\.yaml'
>>> # note: here regex patterns must be of type: re.Pattern. If not, they are treated as normal strings
>>> for file in Traverser(path == ['/etc/config.json', re.compile(r'/etc/.*/config\.yaml')]):
>>>     print(str(file))
>>>
>>> # recursively print all files whose paths match the regular expression patterns '/etc/.*/config\.json' or '/etc/.*/config\.yaml' or '/etc/.*/config\.xml'
>>> # note: here regex patterns can be of type: string or re.Pattern. String values ​​are automatically compiled to re.Pattern
>>> for file in Traverser(path.regex(r'/etc/.*/config\.json', r'/etc/.*/config\.yaml', re.compile(r'/etc/.*/config\.xml'))):
>>>     print(str(file))
>>>
>>> # recursively print all files whose paths match the glob patterns '**/*.jpg' or '**/*.png'
>>> for file in Traverser(path.glob('**/*.jpg', '**/*.png')):
>>>     print(str(file))
```


### Examples of "depth" filter
```python
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import depth
>>>
>>> # recursively print all files located in range <1, 4> of levels of the root directory subtree hierarchy
>>> for file in Traverser(depth(1, 4)):
>>>     print(str(file))
>>>
>>> # recursively print all files located in range (1, ∞) of levels of the root directory subtree hierarchy
>>> for file in Traverser(1 < depth()):
>>>     print(str(file))
>>>
>>> # recursively print all files located in range <0, 2) of levels of the root directory subtree hierarchy
>>> for file in Traverser(depth() < 2):
>>>     print(str(file))
>>>
>>> # recursively print all files located in range (1, 4> of levels of the root directory subtree hierarchy
>>> for file in Traverser(1 < depth() <= 4):
>>>     print(str(file))
>>>
>>> # recursively print all files located at level 2 of the root directory subtree hierarchy
>>> for file in Traverser(depth() == 2):
>>>     print(str(file))
>>>
>>> # recursively print all files located at any level but no 2 of the root directory subtree hierarchy
>>> for file in Traverser(-(depth() == 2)):
>>>     print(str(file))
```


### Examples of "hidden" filter
```python
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import hidden
>>>
>>> # recursively print all paths with hidden attribute
>>> for path in Traverser(hidden):
>>>     print(str(path))
>>>
>>> # recursively print all files with hidden attribute
>>> for file in Traverser(hidden).files(hidden):
>>>     print(str(file))
>>>
>>> # recursively print all dirs with hidden attribute
>>> for dir in Traverser(hidden).dirs(hidden):
>>>     print(str(dir))
```


### Examples of "executable" filter
```python
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import executable
>>>
>>> # recursively print all paths with executable attribute
>>> for path in Traverser(executable):
>>>     print(str(path))
>>>
>>> # recursively print all files with executable attribute
>>> for file in Traverser(executable).files(executable):
>>>     print(str(file))
>>>
>>> # recursively print all dirs with executable attribute
>>> for dir in Traverser(executable).dirs(executable):
>>>     print(str(dir))
```


### Examples of "writeable" filter
```python
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import writeable
>>>
>>> # recursively print all paths with writeable attribute
>>> for path in Traverser(writeable):
>>>     print(str(path))
>>>
>>> # recursively print all files with writeable attribute
>>> for file in Traverser(writeable).files(writeable):
>>>     print(str(file))
>>>
>>> # recursively print all dirs with writeable attribute
>>> for dir in Traverser(writeable).dirs(writeable):
>>>     print(str(dir))
``` 


### Examples of "readonly" filter
```python
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import readonly
>>>
>>> # recursively print all paths with readonly attribute
>>> for path in Traverser(readonly):
>>>     print(str(path))
>>>
>>> # recursively print all files with readonly attribute
>>> for file in Traverser(readonly).files(readonly):
>>>     print(str(file))
>>>
>>> # recursively print all dirs with readonly attribute
>>> for dir in Traverser(readonly).dirs(readonly):
>>>     print(str(dir))
```


### Examples of "owner" filter
```python
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import owner
>>>
>>> # recursively print all paths owned by user 'htarnacki'
>>> for path in Traverser(owner('htarnacki')):
>>>     print(str(path))
>>>
>>> # recursively print all paths owned by user 'htarnacki'
>>> for path in Traverser(owner == 'htarnacki'):
>>>     print(str(path))
>>>
>>> # recursively print all paths owned by user 'root' or 'htarnacki'
>>> for path in Traverser(owner('root', 'htarnacki')):
>>>     print(str(path))
>>>
>>> # recursively print all paths owned by user 'root' or 'htarnacki'
>>> for path in Traverser(owner == ['root', 'htarnacki']):
>>>     print(str(path))
```


### Examples of "size" filter
```python
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import size
>>>
>>> # recursively print all files whose size is less than 2 MB
>>> for path in Traverser(size() < '2MB'):
>>>     print(str(path))
>>>
>>> # recursively print all files whose size is less than 2 MB and greater or equal to 100 KB
>>> for path in Traverser('100KB' <= size() < '2MB'):
>>>     print(str(path))
```
Supported units are: 'B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'


### Examples of "call" filter
```python
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import call
>>> from PathTraverser.utils.Path import starts_with
>>>
>>> # recursively print all paths named 'a.mp4'
>>> for path in Traverser(call(lambda _: _.name == 'a.mp4')):
>>>     print(str(path))
>>>
>>> # recursively print all paths named 'a.mp4' and located at level 0 of the root directory subtree hierarchy
>>> for path in Traverser(call(lambda _, depth: _.name == 'a.mp4' and depth == 0)):
>>>     print(str(path))
>>>
>>> # recursively print all paths named "a.mp4" and located at a level lower than 5 in the root directory subtree hierarchy whose relative path starts with "a/b/c"
>>> for path in Traverser(
>>>     call(lambda _, depth, rel: _.name == 'a.mp4' and depth < 5 and starts_with(rel, Path('a/b/c')))
>>> ):
>>>     print(str(path))
```
- the user can use any callable object
- there is only one mandatory input parameter for the callable object, it is the absolute path to the accepted file or directory
- user can also use following optional input parameters:
    - **depth**: root directory subtree level
    - **rel**: relative path to the accepted file or directory
    - **root**: path to root directory
    - **skipsubtree**: a function that can be used to skip scanning some subdirectories


### Iterable and Iterator
- 'Traverser' is an iterable object. Iterable object can produce many iterators
- 'Traverser' can produce iterators in two ways:
    - **iter(Traverser())**
    - **Traverser().iter()**
    - **Traverser().files**: filters from 'Traverser' object + one additional 'files' filter
    - **Traverser().files(filter1, filter2, ...)**: filters from 'Traverser' object + [files, filter1, filter2, ...] filters
    - **Traverser().dirs**: filters from 'Traverser' object + one additional 'dirs' filter
    - **Traverser().dirs(filter1, filter2, ...)**: filters from 'Traverser' object + [dirs, filter1, filter2, ...] filters
    - **Traverser().symlinks**: filters from 'Traverser' object + one additional 'symlinks' filter
    - **Traverser().symlinks(filter1, filter2, ...)**: filters from 'Traverser' object + [symlinks, filter1, filter2, ...] filters
    - **Traverser().filter(filter1, filter2, ...)**: filters from 'Traverser' object + [filter1, filter2, ...] filters


### Skipping subtrees
We can dynamically instruct Traverser to skip visiting hierarchies of some subdirectories. It means Traverser will not step down into skipped directories and will not iterate over contents of such directories
```python
>>> from PathTraverser import Traverser
>>> from PathTraverser.Traverser import Iterator
>>> from PathTraverser.filters import call
>>> from PathTraverser.utils.Path import starts_with
>>> 
>>> # let's assume we have the following directory structure
>>> # | a
>>> # |-- b
>>> # |---- b1
>>> # |---- b2
>>> # |---- b3
>>> # |------- b4
>>> # |-- c
>>> # |-- d
>>> 
>>> # such code will recursively scan the entire root directory structure from top to bottom
>>> paths = Traverser(Path('a')).get()
>>> 
>>> # but what if we wanted to skip traversing directory b and all of its subdirectories? This code would allow us to do that
>>> for _ in (paths := Traverser(Path('a')).iter()):
>>>     if _.name == 'b' and _.is_dir():
>>>         paths.skipsubtree(_)
>>>         continue
>>>     print(str(_))
>>> 
>>> # and all 5 examples below have basically the same effect:
>>> 
>>> # 1
>>> for _ in (paths := iter(Traverser(TEST_DATA_ROOT))):
>>>     if _.name == 'b' and _.is_dir():
>>>         paths.skipsubtree(_)
>>>         continue
>>>     print(str(_))
>>> 
>>> # 2
>>> with Traverser(TEST_DATA_ROOT).iter() as paths:
>>>     for _ in paths:
>>>         if _.name == 'b' and _.is_dir():
>>>             paths.skipsubtree(_)
>>>             continue
>>>         print(str(_))
>>> 
>>> # 3
>>> with iter(Traverser(TEST_DATA_ROOT)) as paths:
>>>     for _ in paths:
>>>         if _.name == 'b' and _.is_dir():
>>>             paths.skipsubtree(_)
>>>             continue
>>>         print(str(_))
>>> 
>>> # 4
>>> paths: Iterator = Traverser(TEST_DATA_ROOT).iter()
>>> for _ in paths:
>>>     if _.name == 'b' and _.is_dir():
>>>         paths.skipsubtree(_)
>>>         continue
>>>     print(str(_))
>>> 
>>> # 5
>>> paths: Iterator = iter(Traverser(TEST_DATA_ROOT))
>>> for _ in paths:
>>>     if _.name == 'b' and _.is_dir():
>>>         paths.skipsubtree(_)
>>>         continue
>>>     print(str(_))
>>>
>>> # and let's compare all these examples with the one below
>>> for path in Traverser(call(lambda _, rel: not starts_with(rel, Path('a/b')))):
>>>     print(str(path))
>>>
>>> # the last example gives the same results, but is less efficient than the previous ones, because the directory "a/b" is still scanned recursively, but all of its contents are not accepted
```


### 'Traverser' object hooks: on_each, on_file, on_dir, on_symlink
- ```on_each```: reacts on each accepted path
- ```on_file```: reacts on each accepted file
- ```on_dir```: reacts on each accepted directory
- ```on_symlink```: reacts on each accepted symlink
```python
>>> from PathTraverser import Traverser
>>>
>>> Traverser() \
>>>     .on_each(lambda _: print(str(_), 'is any path')) \
>>>     .on_file(lambda _: print(str(_), 'is a file')) \
>>>     .on_dir(lambda _: print(str(_), 'is a directory')) \
>>>     .on_symlink(lambda _: print(str(_), 'is a symlink')) \
>>>     .get()
```

### Context manager
The Traverser object and all the iterators it generates are context managers. There is no magic behind it, but it allows you to write the same code in a different style if desired
```python
>>> from PathTraverser import Traverser
>>> from PathTraverser.filters import hidden, files, dirs
>>>
>>> # 'context manager' style
>>> # recursively print all hidden files and next all hidden dirs
>>> with Traverser(TEST_DATA_ROOT, hidden) as paths:
>>>     for _ in paths.files:
>>>         print(str(_))
>>>     for _ in paths.dirs:
>>>         print(str(_))
>>>
>>> # 'normal' style
>>> # recursively print all hidden files and next all hidden dirs
>>> paths = Traverser(TEST_DATA_ROOT, hidden)
>>> for _ in paths.files:
>>>     print(str(_))
>>> for _ in paths.dirs:
>>>     print(str(_))
>>>
>>> # 'context manager' style
>>> # recursively print all hidden files and next all hidden dirs
>>> with Traverser(TEST_DATA_ROOT, hidden) as paths:
>>>     for _ in paths.filter(files):
>>>         print(str(_))
>>>     for _ in paths.filter(dirs):
>>>         print(str(_))
>>>
>>> # 'normal' style
>>> # recursively print all hidden files and next all hidden dirs
>>> paths = Traverser(TEST_DATA_ROOT, hidden)
>>> for _ in paths.filter(files):
>>>     print(str(_))
>>> for _ in paths.filter(dirs):
>>>     print(str(_))
```


### Iterators produced by 'Traverser' object have some usefull read only properties
- ```root```: iterated root directory (points to the directory specified by the user when creating the Traverser instance)
- ```depth```: current iteration depth
```python
>>> from PathTraverser import Traverser
>>>
>>> # recursively print all files and directories with iteration depth == 0
>>> for _ in (paths := iter(Traverser(TEST_DATA_ROOT))):
>>>     if paths.depth == 0 and _.is_dir():
>>>         paths.skipsubtree(_)
>>>     print(str(_))
```


### This project also provides some useful tools as an extension of the built-in pathlib.Path functionality
- ```first(path)```: returns first part of a given path (return type is pathlib.Path)
- ```last(path)```: returns last part of a given path (return type is pathlib.Path)
- ```part_count(path)```: returns number of path parts of a given path (return type is int)
- ```starts_with(path_a, path_b)```: check if path_b is a parent of or equal to path_a. The comparison is done by comparing individual parts of the paths, not by comparing the characters of the simple string representation of the paths. Note that no path resolution/normalization is performed automatically when executing this function. Normalization should be performed by the user if necessary (return type is bool)

```python
>>> from pathlib import Path
>>> from PathTraverser.utils.Path import first, last, part_count, starts_with
>>>
>>> first(Path('a/b/c')).name == 'a'
>>> last(Path('a/b/c')).name == 'c'
>>> part_count(Path('a/b/c')) == 3
>>> starts_with(Path('a/b/c/d'), Path('a/b/c')) == True
>>> starts_with(Path('a/b/c/d2'), Path('a/b/c/d')) == False
```

We can also import these path utilities in the form of monkey patching the original pathlib.Path class:
```python
>>> from PathTraverser.utils.Path import Path  # this import executes also monkey patching of pathlib.Path
>>>
>>> Path('a/b/c').first.name == 'a'
>>> Path('a/b/c').last.name == 'c'
>>> Path('a/b/c').part_count == 3
>>> Path('a/b/c/d').starts_with(Path('a/b/c')) == True
```


### More examples
More examples can be found in a test file of this project: **tests/testTraverser.py**
