#!/bin/bash

_mk_deps_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _MK_DEPS_COMPLETE=complete $1 ) )
    return 0
}

complete -F _mk_deps_completion -o default mk-deps;
