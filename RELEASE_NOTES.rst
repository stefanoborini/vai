Release Notes
=============

Vai 1.6
~~~~~~~

   - Plugin system. Syntax color plugins allow you to personalize the colorization of syntax highlighting tokens.
     The command plugins allows you to execute code whenever a user issues a :command
   - Solved a pernicious issue with ncursesw on some linux distros.
   - Pasting now brings the cursor forward to the first non-blank character.
   - Python highlights public, private and dunder methods with different colors. Similar for classes.
   - `Bugfixing <https://github.com/stefanoborini/vai/issues?q=is%3Aissue+milestone%3Av1.6+is%3Aclosed+label%3ABug>`_

Vai 1.5
~~~~~~~

   - Bookmarks (ma and 'a vim keys)
   - Initial support for 256 colors.
   - Automatically add closing parenthesis/quote
   - Indent/dedent current line with Ctrl-T/Ctrl-D in insert mode
   - Fixed a potential deadlock condition
   - Tooltip linter now disappears automatically after timeout.
   - `Bugfixing <https://github.com/stefanoborini/vai/issues?q=is%3Aissue+milestone%3Av1.5+is%3Aclosed+label%3ABug>`_

Vai 1.4
~~~~~~~

   - Unicode icons for the Side Ruler. Can be disabled with appropriate setting in the .config/vai/vairc file.
   - Command line option ``--dump-default-config`` to create a default vairc file.
   - Dumping of current open buffers in case of crash.
   - More performance improvements.
   - Now tooltip messages don't stay when you move around or start typing.
   - Parentheses are no longer removed when using ``dw``
   - Improved color schema
   - Implemented vim movements ``hjkl``
   - Removing leading spaces when breaking a line.
   - Implemented :x to write and quit.
   - Implementation of XDG Base Directory Specification.
   - Command bar tabbing autocompletes filenames and directory names.
   - Markers added when a line is deleted.
   - Refactorings
   - `Bugfixing <https://github.com/stefanoborini/vai/issues?q=is%3Aissue+milestone%3Av1.4+is%3Aclosed+label%3ABug>`_

Vai 1.3
~~~~~~~

   - Deleting to end of word should also delete the spaces following it.
   - Implemented redo with Ctrl+R
   - :r command to read and include a file
   - Performance improvements
   - `Bugfixing <https://github.com/stefanoborini/vai/issues?q=is%3Aissue+milestone%3Av1.3+is%3Aclosed+label%3ABug>`_

Vai 1.2
~~~~~~~

   - Reset optimistic column when adding new line.
   - Indentation markers proof of concept.
   - Restore cursor position at load
   - Introduced ZZ command
   - Initial Configuration file infrastructure. Basic colors of StatusBar/SideRuler can be changed.
   - Handle long filenames in StatusBar
   - Major refactoring of the MVC structure
   - `Bugfixing <https://github.com/stefanoborini/vai/issues?q=milestone%3Av1.2+label%3ABug>`_

Vai 1.1
~~~~~~~

.. image:: https://github.com/stefanoborini/vai/blob/master/static/images/screenshot-1.1.png

..

   - Highlight of False/True  
   - Change name to prevent issues with Vix video editor
   - Highlighting of current identifier 
   - copy/cut/paste (single line)
   - Hovering tooltip
   - Replace commands
   - Delete word 
   - Asterisk search
   - Add ^N ^P as shortcuts for buffer nav 
   - Delete tabspaces on backspace
   - Autoindent
   - Tab completion
   - Solved color difference on Mac vs Linux
   - `Bugfixing <https://github.com/stefanoborini/vai/issues?q=milestone%3Av1.1+label%3ABug>`_


Vai 1.0
~~~~~~~

   - First release

