Here you will find a list of implemented and still not implemented features, shortcuts and modes.

Actions in command mode
=======================

Movements
---------

=======    =================================  ==========
  Key        Operation                          Status
=======    =================================  ==========
b          Go to beginning of prev. word      TODO
e          Go to end of word                  TODO
gg         Go to first line                   Done
G          Go to last line                    Done
t          Till character                     TODO
w          Word forward                       TODO
h          Cursor left                        Done
j          Cursor down                        Done
k          Cursor up                          Done
l          Cursor right                       Done
Up         Cursor up                          Done
Down       Cursor down                        Done
Left       Cursor left                        Done
Right      Cursor Right                       Done
$          To end of line                     Done
^          To beginning of line               Done
{          To next paragraph                  TODO
}          To prev paragraph                  TODO
n          Go to next search match            Done
*          Search word under cursor           Done
=======    =================================  ==========

Change to insert mode
---------------------

=======    =================================  ==========
  Key        Operation                          Status
=======    =================================  ==========
a          Insert on next char                Done
A          Insert at end of line              Done
i          Insert on current char             Done
I          Insert beginning of line           Done
o          New next line                      Done
O          New prev line                      Done
s          Delete char and start insert       TODO
cc         Delete lines and start insert      TODO
=======    =================================  ==========

Delete 
------

=======    =================================  ==========
  Key        Operation                          Status
=======    =================================  ==========
dd         Delete line                        Done
dw         Delete word                        Done
D          Delete to end of line              Done
=======    =================================  ==========

Other commands
--------------

=======    =================================  ==========
  Key        Operation                          Status
=======    =================================  ==========
u          Undo                               Done
R          Redo                               Done
m          Bookmarks                          TODO
q          Recording                          TODO
p          Paste                              Done
r          Modify current character           Done
v          Start visual mode                  TODO
yy         Yank current line                  Done
.          Repeat last                        TODO
zz         Redraw centering cursor            TODO
^N         Go to next buffer                  Done
^P         Go to previous buffer              Done
=======    =================================  ==========

Colon commands
--------------

===========    =================================  ==========
  Key            Operation                          Status
===========    =================================  ==========
:w             Write to current file              Done
:w file        Write to filename file             Done
:wq            Write and quit                     Done
:x             Write and quit                     Done
:q             Quit with confirmation             Done
:q!            Quit without confirmation          Done
:r file        Read file and dump in current buf  Done
:bp            Select previous buffer             Done
:bn            Select next buffer                 Done
:e file        Open new file in new buffer        Done
===========    =================================  ==========

