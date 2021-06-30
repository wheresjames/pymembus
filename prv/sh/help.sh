#!/bin/bash

#--------------------------------------------------------------------------------------------------
# Where are the help files?

LINK="${ROOTDIR}/bld/html/index.html"

if [ ! -f "$LINK" ]; then
    PYMEMBUSCMD=`which pymembus`
    if [ ! -z $PYMEMBUSCMD ]; then
        LINK="$(pymembus info share)/dox/index.html"
    fi
fi

if [ ! -f "$LINK" ]; then
    UPONE=`dirname "${ROOTDIR}"`
    LINK="${UPONE}/share/pymembus/dox/index.html"
fi

if [ ! -f "$LINK" ]; then
    LINK="/usr/share/pymembus/dox/index.html"
fi

if [ ! -f "$LINK" ]; then
    LINK="/usr/local/share/pymembus/dox/index.html"
fi

# Did we find help?
if [ ! -f $LINK ]; then
    exitWithError "Help not found"
fi

showInfo "Help : file://$LINK"


#--------------------------------------------------------------------------------------------------
# Can we open a browser?
OPTS="xdg-open open lynx w3m links2 links"
for v in $OPTS; do
    TEST=`which $v`
    if [ ! -z $TEST ]; then
        BROWSER=$TEST
        break
    fi
done

if [ ! -z $BROWSER ]; then
    $BROWSER $LINK
fi
