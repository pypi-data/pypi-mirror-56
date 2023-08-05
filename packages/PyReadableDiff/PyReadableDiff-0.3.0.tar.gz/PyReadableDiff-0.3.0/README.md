# PyReadableDiff (pydiff)

[![Status](https://travis-ci.org/iuliux/PyReadableDiff.svg?branch=master)](https://travis-ci.org/iuliux/PyReadableDiff)
[![Version](https://img.shields.io/pypi/v/PyReadableDiff.svg)](https://pypi.python.org/pypi/PyReadableDiff)

Intuitive human-readable diff for text.

The [pydiff](https://github.com/iuliux/PyReadableDiff)
library was inspired by the [jsdiff](https://github.com/kpdecker/jsdiff)
library, and it tries to port as much functionality from JS to Python as possible,
though the APIs may differ. Though the current implementation is also based on the algorithm proposed in
["An O(ND) Difference Algorithm and its Variations" (Myers, 1986)](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.4.6927),
one may not assume obtaining identical diffs for all pairs of input strings,
since in some cases there may be several optimal solutions (in terms of [edit distance](https://en.wikipedia.org/wiki/Edit_distance)),
and the algorithms will return only one of them.

## Installation

The package is available through the [PyPI](https://pypi.python.org/pypi/PyReadableDiff),
so you can easily download and install it via `pip`:
```shell
pip install PyReadableDiff
```

After the installation successfully completes, you may open any available Python interpreter and check whether the **pydiff** package can be imported and used:
```python
>>> import pydiff
>>> pydiff.__version__
...
```

Also you can install the library from a clone of the repository by running
```shell
python setup.py install
```
from the root of the local copy.

## API

* `pydiff.diff_characters(old_string, new_string)` - diffs two blocks of text, comparing character by character.

    Returns a list of change dicts (see below).

* `pydiff.diff_words(old_string, new_string)` - diffs two blocks of text, comparing word by word, ignoring whitespaces.

    Returns a list of change dicts (see below).

* `pydiff.diff_words_with_spaces(old_string, new_string)` - diffs two blocks of text, comparing word by word, treating whitespaces as significant.

    Returns a list of change dicts (see below).

* `pydiff.diff_lines(old_string, new_string)` - diffs two blocks of text, comparing line by line.

    Returns a list of change dicts (see below).

* `pydiff.diff_stripped_lines(old_string, new_string)` - diffs two blocks of text, comparing line by line, discarding leading and trailing whitespaces.

    Returns a list of change dicts (see below).

* `pydiff.diff_lists(old_list, new_list)` - diffs two lists (or any other iterable objects which will be converted to lists), comparing element by element.

    Returns a list of change dicts (see below).

* `pydiff.convert_changes_to_xml(changes)` - converts a list of changes to a serialized XML format.

### Change Dicts

Many of the methods above return change dicts. These dicts consist of the following keys:

* `value`: text content
* `count`: number of tokens merged together in order to form the given value
* `added`: `True` if the value was inserted into the new string (`None` or absent otherwise)
* `removed`: `True` of the value was removed from the old string (`None` or absent otherwise)

Note that some cases may omit a particular flag key. Comparison on the flag keys should always be done in a truthy or falsy manner.
We suggest using the `.get(key)` method of dicts for this purpose, e.g.:
```python
if change.get('added'):
    # handle an inserted part
    ...
elif change.get('removed'):
    # handle a deleted part
    ...
else:
    # handle an unchanged part
    ...
```

## Custom Diffs

If you need more customization for your diffs, you can inherit from the `pydiff.Diff` base class and override the following available public methods:

* `preprocess(self, string)` - prepares an input string for processing (is used on `old_string` and `new_string` prior to running the main diff computing algorithm).
By default does nothing and simply returns the same string back.

* `tokenize(self, string)` - splits the preprocessed input string into atomic parts, which are compared with each other during the diffing.
By default uses characters as tokens.

* `join(self, tokens)` - merges tokens into bigger strings, which then form text values of resultant change dicts.
By default simply concatenates all tokens using an empty string as a separator.

* `are_equal(self, left_token, right_token)` - compares two tokens returning `True` or `False`.
By default uses the built-in `==` operator. For example, if you want your diffs to be case insensitive, you may define this method in a following manner:

```python
import pydiff

class CustomDiff(pydiff.Diff):
    ...

    def are_equal(self, left_token, right_token):
        return left_token.lower() == right_token.lower()

    ...
```

After that actual diffs can be computed via the inherited `.diff(self, old_string, new_string)` method of instances of your newly created subclass.

## Compatibility

The **pydiff** is tested and known to be compatible with the following versions of Python: `2.7`, `3.5`, `3.6`, `3.7`, `3.8`.

## Contributing and Testing

If you want to contribute to the library, you are free to create pull requests. Make sure that all your changes are in a separate branch.
If you add some new functionality, don't forget to add corresponding tests. Also check that all the tests pass (both existing and newly added).

In order to run the tests locally, you have to install all the neccessary packages for testing:
```shell
pip install -r test-requirements.txt
```

After that you will be able to run the tests (they are located in `pydiff/tests` and have the prefix `test_`):
```shell
pytest pydiff
```

Simply add `--pep8` to the command above in order to run some `PEP 8` checks instead of the usual unit tests.
