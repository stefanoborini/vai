[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fstefanoborini%2Fvai.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fstefanoborini%2Fvai?ref=badge_shield)

Vai
===

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/stefanoborini/vai
   :target: https://gitter.im/stefanoborini/vai?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. image:: https://travis-ci.org/stefanoborini/vai.svg?branch=master
   :target: https://travis-ci.org/stefanoborini/vai
   :alt: Build status
.. image:: https://img.shields.io/pypi/dm/vai.svg
   :target: https://pypi.python.org/pypi/vai/
   :alt: Downloads
.. image:: https://img.shields.io/pypi/pyversions/vai.svg
   :target: https://pypi.python.org/pypi/vai/
   :alt: Supported Python versions
.. image:: https://img.shields.io/pypi/v/vai.svg
   :target: https://pypi.python.org/pypi/vai/
   :alt: Latest version
.. image:: https://landscape.io/github/stefanoborini/vai/master/landscape.png
   :target: https://landscape.io/github/stefanoborini/vai
   :alt: Latest version
.. image:: http://img.shields.io/gratipay/StefanoBorini.svg
   :target: https://gratipay.com/StefanoBorini/
   :alt: gratipay
   
We love vim, but we want more. We want a terminal-based IDE that looks like vim,
handles like vim, but has all those nice features of Eclipse and Sublime, is
integrated with git, and is fully coded in python. 

For more information about the Rationale behind the project, the development
methodology and the planned features see the `RATIONALE document <https://github.com/stefanoborini/vai/blob/master/RATIONALE.rst>`_.

Implemented Features
--------------------

   - General vim look and feel.
   - Syntax highlighting for python. Partial support for other languages.
   - Highlighting of all occurrences of the identifier currently under the cursor.
   - Linting for python 3 with pyflakes
   - Shows linting results on the sidebar. Linting messages popup inline.
   - Backward and forward search (no regexp yet)
   - Tab completion for editor and command bar (while accessing files)
   - Undo/Redo
   - Indentation levels
   - Multiple buffers
   - Copying and pasting
   - Multiple lines selection
   - Minimal configuration of colors
   - Cursor position restored between runs.
   - Autoindent
   - Syntax color plugins
   - :command plugins

See the current vim keys compatibility list in the `FEATURES document <https://github.com/stefanoborini/vai/blob/master/FEATURES.rst>`_.

**Note**: vai is currently focused mostly on Python editing. Future additions will handle other languages.


Screenshots
-----------

Vai 1.6/1.7

.. image:: https://github.com/stefanoborini/vai/blob/master/static/images/screenshot-1.6.png

Vai 1.4/1.5

.. image:: https://github.com/stefanoborini/vai/blob/master/static/images/screenshot-1.4.png

Vai 1.2/1.3

.. image:: https://github.com/stefanoborini/vai/blob/master/static/images/screenshot-1.2.gif


Download
--------

You can get the latest version of vai from `pypi
<https://pypi.python.org/pypi/vai>`_, either manually
or via pip

   pip3.4 install vai

**Important Note**: you need python 3.4. Python 3.3 will not work. 

See the `Release Notes <https://github.com/stefanoborini/vai/blob/master/RELEASE_NOTES.rst>`_ for details
about the release changes.

Contributors
------------

If you want to contribute to Vai, a good place to start is to read the `Design
document <https://github.com/stefanoborini/vai/blob/master/docs/Design.rst>`_.

If you want to develop plugins, the document `WritingPlugins
<https://github.com/stefanoborini/vai/blob/master/docs/WritingPlugins.rst>`_ is what you are
looking for. Keep into account that the API is evolving, and at the moment, rather limited.


Main development:
- `Stefano Borini <http://forthescience.org>`_

Additional contributions:
- `Carl George (cgtx) <https://github.com/cgtx>`_



## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fstefanoborini%2Fvai.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fstefanoborini%2Fvai?ref=badge_large)