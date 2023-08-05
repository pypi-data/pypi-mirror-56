# Root Folder Search

This package finds the root directory of a project by recursively traversing parent directories starting at a given path.

I used it to overcome a limitation in Jupyter Notebooks, that doesn't provide the `__file__` variable that would let me easily find the root folder of a project, regardless the current working directory. You might find it useful in other scenarios.

# How to use

```
import rootfoldersearch

# returns a string with the absolute path to the root folder, where Readme.md is located, starting the search in the CWD.
rootfoldersearch.findpath('Readme.md')

# the same, but using a file in a subfolder as reference to find the root directory
rootfoldersearch.findpath('/util/a-file')

# the same, but only tries 3 parent folders recursively (default is 10)
rootfoldersearch.findpath('Readme.md', depth=3)

# starting the search in a specific directory (as opposed to using the CWD)
rootfoldersearch.findpath('Readme.md', cwd='/..')

```
