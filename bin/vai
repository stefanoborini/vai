#!/bin/bash

# Script to workaround the ncurses wide character issue. We let vai_exec
# deal with installing the workaround. 
export LD_LIBRARY_PATH=$HOME/.local/lib/vai:$LD_LIBRARY_PATH

vai_exec $@

# If it returns 42, it means that it installed the workaround. Just relaunch it.
if test $? -eq 42;
then
    vai_exec $@
fi
