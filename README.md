# PathTraverser

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Because traversing through files and directories in Python should be as easy and fun as in Groovy.


## Installation

```bash
$ pip install --user --upgrade PathTraverser
```

## Usage

### Basic example of simple iteration over files and directories
```python
>>> from PathTraverser import Traverser
>>>
>>> with Traverser('.') as paths:
>>>    for _ in paths:
>>>        print(str(_))
```

```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(Path.cwd()) as paths:
>>>    for _ in paths:
>>>        print(str(_))
```
Iterated root path can be of type string or pathlib.Path and can be relative or absolute

### We can iterate multiple times over the same Traverser
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(Path.cwd()) as paths:
>>>    for _ in paths:
>>>        print(str(_))
>>>    for _ in paths:
>>>        print(str(_))
```

### We can nest multiple Traversers
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(Path.cwd()) as paths:
>>>     for _ in paths:
>>>         if _ == Path.cwd() / 'docs':
>>>             with Traverser(_) as docs:
>>>                 for doc in docs:
>>>                     print(str(doc))
>>>             break
```

### We can filter iterated paths by exact name
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         namefilter='d.mp4'
>>> ) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

### We can filter iterated paths by regexp name
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         namefilter=re.compile(r'.*\.mp4')
>>> ) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

### We can filter iterated paths by extension
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         extfilter='txt'
>>> ) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

### We can limit max depth of iteration
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         maxdepth=0
>>> ) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

### We can limit min depth of iteration
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         mindepth=2
>>> ) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

### We can filter different types of files
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser, PathTypes
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         pathtype=PathTypes.FILE) as files:
>>>     for _ in files:
>>>         print(str(_))
```

```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser, PathTypes
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         pathtype=PathTypes.DIRECTORY) as dirs:
>>>     for _ in dirs:
>>>         print(str(_))
```

```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser, PathTypes
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         pathtype=PathTypes.LINK) as links:
>>>     for _ in links:
>>>         print(str(_))
```

### We can build custom complex filters
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         pathfilter=lambda _: 'dog' in _.name) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

First argument of path filter is positional and mandatory and is of type pathlib.Path. It means: current path to check

Path filter can also have any of following optional key word arguments:
- rel: relative form of current path against root path (of type pathlib.Path)
- root: root path (of type pathlib.Path)
- depth: current iteration depth (of type int)

```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         pathfilter=lambda _, rel: rel.parts[0] in {'sub2', 'sub3'}
>>> ) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         pathfilter=lambda _, depth: depth < 1
>>> ) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>> from PathTraverser.PathUtils import starts_with
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         pathfilter=lambda _, root: starts_with(_, root / 'sub1')
>>> ) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

### We can use multiple filters at once
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser, PathTypes
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         extfilter='txt',
>>>         pathtype=PathTypes.FILE,
>>>         pathfilter=lambda _, rel: rel.parts[0] in {'sub2', 'sub3'}
>>> ) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

### We can exclude iterated paths by exact name
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         exclude_namefilter='d.mp4'
>>> ) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

### We can exclude iterated paths by regexp name
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         exclude_namefilter=re.compile(r'.*\.mp4')
>>> ) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

### We can exclude iterated paths by extension
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         exclude_extfilter='txt'
>>> ) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

### We can build custom complex exclude filters
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         exclude_pathfilter=lambda _: 'dog' in _.name) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

Arguments for exclude_pathfilter are the same as described for pathfilter

### We can mix filters and exclude filters together
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser, PathTypes
>>>
>>> with Traverser(
>>>         Path.cwd(),
>>>         extfilter='txt',
>>>         pathtype=PathTypes.FILE,
>>>         pathfilter=lambda _, rel: rel.parts[0] in {'sub2', 'sub3'},
>>>         exclude_namefilter='d.txt'
>>> ) as paths:
>>>     for _ in paths:
>>>         print(str(_))
```

### We can dynamically instruct Traverser to skip visiting hierarchies of some subdirectories. It means Traverser will not step down into skipped directories and will not iterate over contents of such directories
```python
>>> from pathlib import Path
>>> from PathTraverser import Traverser
>>>
>>> with Traverser(Path.cwd()) as paths:
>>>     for _ in paths:
>>>         if paths.depth == 0 and _.is_dir() and _.name == 'x':
>>>             paths.skipsubtree(_)  # do not enter 'x' directory and do not traverse its content
>>>             continue
>>>         print(str(_))
```
Skipping subtrees is done by ```def skipsubtree(self, *names: Union[Path, str]) -> 'Traverser'``` method which is part of a Traverser object.

Please notice another usefull Traverser property that is used in this example: ```Traverser.depth``` which means depth of current iteration

### Traverser constructor has following input parameters
```
root: Union[Path, str]                                  -> root path
pathtype: PathTypes                                     -> path typ filter
mindepth: int = 0                                       -> min depth filter
maxdepth: int = None                                    -> max depth filter
pathfilter: Callable = None                             -> complex path filter
namefilter: Union[re.Pattern, str] = None               -> name filter
extfilter: str = None                                   -> extension filter
exclude_pathfilter: Callable = None                     -> exclude complex path filter
exclude_namefilter: Union[re.Pattern, str] = None       -> exclude name filter
exclude_extfilter: str = None                           -> exclude extension filter
followlinks: bool = True                                -> do follow symbolic links to subdirectories during traversing?
onerror: Callable = None                                -> by default errors from the os.scandir() call are ignored. If optional arg 'onerror' is specified, it should be a function; it will be called with one argument, an OSError instance. It can report the error to continue with the walk, or raise the exception to abort the walk. Note that the filename is available as the filename attribute of the exception object

```

### Traverser object has some usefull read only properties
- ```root```: root directory being iterated (it points to a directory provided by user during instantiation of Traverser object)
- ```depth```: depth of current iteration


### This project provides also some usefull utilities as an extension to pathlib.Path built in functionality
- ```first(path)```: returns first part of a given path (return type is pathlib.Path)
- ```last(path)```: returns last part of a given path (return type is pathlib.Path)
- ```part_count(path)```: returns number of path parts of a given path (return type is int)
- ```starts_with(path_a, path_b)```: check if path_b is parent to path_a. The comparison is done by comparing individual parts of the paths, not by comparing the characters of the simple string representation of the paths. Please note that no path resolution/normalization is done automatically when performing this function. Normalization should be performed by the user if necessary (return type is bool)


```python
>>> from pathlib import Path
>>> from PathTraverser.PathUtils import first, last, part_count, starts_with
>>>
>>> first(Path('a/b/c')).name == 'a'
>>> last(Path('a/b/c')).name == 'c'
>>> part_count(Path('a/b/c')) == 3
>>> starts_with(Path('a/b/c/d'), Path('a/b/c')) == True
>>> starts_with(Path('a/b/c/d2'), Path('a/b/c/d')) == False

```

We can also import this path utilities in the form of monkey patching of original pathlib.Path class:
```python
>>> from PathTraverser.PathUtils import Path  # this import executes also monkey patching of pathlib.Path
>>>
>>> Path('a/b/c').first.name == 'a'
>>> Path('a/b/c').last.name == 'c'
>>> Path('a/b/c').part_count == 3
>>> Path('a/b/c/d').starts_with(Path('a/b/c')) == True

```