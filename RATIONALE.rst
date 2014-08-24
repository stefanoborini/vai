Rationale
=========

A most frequent question I've been asked is "why not NeoVim?". 
Before starting vai, and more or less a month before the annoucement of neovim,
I put my nose in the vim source code. Here are my findings

   - It's completely in C, and not good C because of portability considerations
     and an old programming style. Adding any of the features I want to that is
     going to be complete hell.

   - vim as it is is not multithreaded. Adding multithreading to vim is going
     to be an ugly task which I don't want to perform. On the reason why I want
     multithreading is because I want the editor to perform operations in the
     background, such as checking for syntax, checking the git for changes, saving
     backups, running tests and marking them as green/red as I type.

   - vim does not use ncurses, and for many good reasons (ncurses is really
     bad), but if I have to render something I don't want to rely on its
     internal IO layer. I want to get up and running fast with a well known
     well documented interface.

   - vim is bloated. Some features are not really needed today (e.g. rot13).
     Others are overdesigned (e.g. folding). Others rely on external tools
     (e.g. ctags) that are a bit ancient in design and choke on unusual situations.

   - I want features such as intellisense like autocompletion, semantic
     highlighting, multicursors and so on. These are complex features that you don't
     want to implement in C. 

   - Developing plugins in python would be much cooler than with a proprietary
     language that has no practical use outside of vim.

   - It takes ages to get a productive vim configuration. vim is missing a
     proper configuration panel and access to an online plugin repo as in
     sublimetext.

   - I wanted to have fun reimplementing a Qt-like library to learn about Qt itself.

Shortly afterwards, Neovim was announced as a refactoring of vim to address
most of my points above. The problem is that, being a refactoring, it will
still be in C and will grow again to become ugly and nasty.

I am not saying they are not amazing programmers and they are not doing an
amazing job. I am saying that it's time to move on. It makes no sense to write
something that complex and without a real need for system programming in C in
2014. Leave C to low level programming, and use high level languages for
everything else. Maybe they will eventually reach the point of coming up with a
lean C core where everything is moved to plugins, but for now they haven't
released anything that can run. I do. They have 96 contributors on the github.
I am alone.

The Neovim guys want to keep compatibility to vim, or better vim plugins.  I am
also trying to keep compatibility, but only limited to key bindings and general
behavior. I am not planning to preserve plugin compatibility at all.
In a sense we have different goals. The question is if their goals actually
matter.

Another question I am asked is "Why not use eclipse/anything else if you want an
IDE?". Eclipse is great software but it's an elephant that's just not for me.
I generally find GUI based development slower, considering my terminal and
keyboard oriented workflow. I would have to throw away and relearn years of
muscle memory training, and it's an investment I am not willing to do. While
vim compatibility modes do exist, I find them limited and I still don't get the
flexibility I get from pure vim. I don't even use gvim, just to contextualize.

Development methodology
-----------------------

I develop in short feature-driven cycles of 2 or 3 weeks, trying to keep
individual entries in the github feature within a proper scope so that I 
implement around 30 features per cycle (according to my current last three
cycles). 

If you want to help with development, there are plenty of small little things 
to do, even not requiring a lot of training or time, and every bit matters, 
but the fact that you are trying it out it's already of great help. 

About vaitk
-----------

Vai foundation rests on VaiTk, a terminal UI toolkit heavily inspired by Qt.
At the moment, VaiTk is part of Vai, but it will eventually become a product 
in its own merit.
