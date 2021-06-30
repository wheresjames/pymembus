#!/bin/bash

#--------------------------------------------------------------------------------------------------
TEST=$1
if [ -z $TEST ]; then
    TEST="$SHDIR/pymembus-test"
fi

if [ ! -f $TEST ]; then
    TEST="cmake --build ./bld --target pymembus-test"
fi

$TEST