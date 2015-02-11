Design
======

The overall design is the following:

- vaitk: an independent toolkit with an interface as close as possible to Qt, but oriented toward the terminal.
- vai: the vim-alike editor built on top of vaitk.

vaitk is divided into a core part (which handles non-"gui" stuff, mostly the object hierarchy, timers, and other low level concepts) and the gui part (which handles widgets, windows, and so on). If you know Qt, you should find yourself at home. At the moment, what happens is that the VApplication has an exec_method. There, the event loop happens: keyboard events are fetched, converted into VKeyEvents, and delivered to the focused widget. This triggers stuff that enqueues other events (e.g. show/hide) and eventually reaches the point where the widgets are marked as "need update". Finally, the event loop checks the full widget tree, and sends paint events to each widget that needs update, plus all the widgets that may be damaged by it (e.g. if a widget is hidden, the underlying one needs to update).

On vaitk, what is needed is the following:

 - More porting of Qt functionalities. In particular, layout management (the layout manager resizes and repositions the widgets before issuing a repaint), and other widgets (dialogs, comboboxes, and so on). 
 - Tests for all this stuff.
 - general performance improvements.
 - secondary: get rid of ncurses, because it interacts badly with threading. Eventually get rid of the Threading approach to get the keyboard events, but then a proper select() strategy is needed to handle timers, and it must be portable. so, not easy thing.

For vai, it's mostly MVC. I do a lot of experiments there because I am writing a book on MVC in parallel, so it's also a platform for experimentation. The idea is that you have the logic in the controllers, and they are in charge of performing actions on the models. All the models are visual-component independent, and contain the textdocument, the state of the GUI, etc. It's plain and simple MVC, nothing fancy.

The TextDocument contains the text, but it's "surrounded" by additional classes for metainformation. This stuff is in progress, but I have LineMetaInfo as a successful implementation. The idea is that Linters, git, and other stuff that scout the document can put meta information on the document itself. You have three types of metainfo: per document, per line, and per character. Of course the big issue is to keep everything in sync. 
Textdocument Metainformation (but not only) is added by two types of analyzer: synchronous and asynchronous. This is not implemented yet, but there's an initial design. Synchronous happen as you type (e.g. tokenization). Asynchronous are "in the background" (e.g. they periodically scout the code for new autocompletion files, or run the unittests as you are working on them, so you see if the test or function under test you are working on right now is actually passing). Another async could scout the code for TODO comments and mark them in a lateral pane. You name it. 

I am very open to better design suggestions. As I said, I am mostly doing experiments in some cases.

Things that are needed right now are

- unittests, in particular of vaitk. it would be a good introduction to the overall code structure.
- A more specialized thing I need is a merkle tree metainformation, 
- a better autocompleter, possibly giving complete information about the signature. I've seen something for python already, but I don't know other languages. 
- If you feel adventurous, you can start thinking how to make a better parser for the commandbar (the current one is very basic), or how to structure a plugin downloader/installation.
- Of course, you can always take some command from vim and implement it (generally as a command, see the commands package dir) or any of the already present issues, but ask me first because some of them may be outdated and badly explained.

Please create issues on github, so we can keep track of them.

My approach is that I implement stuff that works, and refactor it merciless as I go and see that a common design emerges. I have no problems rewriting a whole subsystem if needed. If something stinks, I change it.
