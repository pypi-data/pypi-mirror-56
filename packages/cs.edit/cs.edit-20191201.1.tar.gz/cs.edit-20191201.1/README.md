Convenience functions for editing things. - Cameron Simpson <cs@cskk.id.au> 02jun2016


*Latest release 20191201.1*:
Initial PyPI release: assorted functions for invoking editors on strings.

Convenience functions for editing things.
- Cameron Simpson <cs@cskk.id.au> 02jun2016

## Function `choose_editor(editor=None, environ=None)`

Choose an editor.

## Function `edit(lines, editor=None, environ=None)`

Write lines to a temporary file, edit the file, return the new lines.

## Function `edit_strings(strs, editor=None, environ=None)`

Edit a list of string, return tuples of changed string pairs.
Honours $EDITOR envvar, defaults to "vi".



# Release Log

*Release 20191201.1*:
Initial PyPI release: assorted functions for invoking editors on strings.
