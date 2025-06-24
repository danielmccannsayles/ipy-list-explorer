# Ipy List Explorer

_This is subject to major overhaul - if you want to use it it's probably best to just copy the code from `src/ipy_list_explorer/widget.py` :)_

[![PyPI - Version](https://img.shields.io/pypi/v/ipy-list-explorer)](https://pypi.org/project/ipy-list-explorer/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ipy-list-explorer)](https://pypi.org/project/ipy-list-explorer/)
[![GitHub License](https://img.shields.io/github/license/danielmccannsayles/ipy-list-explorer)](https://github.com/danielmccannsayles/ipy-list-explorer/blob/main/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/ipy-list-explorer)](https://pypi.org/project/ipy-list-explorer/)

**A simple list explorer for Ipython, made entirely from ipywidgets.**

Pass in a list of strings, and view them in two ways

1. As a condensed list view (with a single line per entry)
2. As a detail view per item.

While in the detail view, use the arrows to navigate through the list.

## Screenshots

![Contains three items in a vertical stack. Gray buttons for each item](https://raw.githubusercontent.com/danielmccannsayles/ipy-list-explorer/refs/heads/main/public/list-view.png "List View")
![Detailed view of text for item 3. Shows scrollbar. Top menu has Back, Prev, Next buttons from Left to Right ](https://raw.githubusercontent.com/danielmccannsayles/ipy-list-explorer/refs/heads/main/public/detail-view.png "Detail View")

## Usage:

```
from ipy_list_explorer import ListExplorer

ListExplorer(["Item1"])
```

## Misc

Feel free to use this however you'd like.
I found it helpful as opposed to printing out long lists to the console.

I welcome any contributions - I'd like it to look nicer/ be more customizable.
I'd also like it if this were part of a larger set of ipy widgets. It's annoying to have to install it individually

Inspired by [InspectAI's Log Viewer](https://inspect.aisi.org.uk/log-viewer.html)
