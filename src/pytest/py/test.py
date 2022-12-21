#!/usr/bin/env python3

import os
import sys
import time
import argparse
import inspect
import traceback

# csp = os.path.dirname(os.path.realpath(__file__))
# print(csp)
# sys.path.append(csp)

# C:/Users/bob/AppData/Local/Temp/pip-req-build-1ldcogu6/_skbuild/win-amd64-3.9/cmake-build/lib/Release/test.py
# C:\Users\bob\AppData\Local\Temp\pip-req-build-1ldcogu6\_skbuild\win-amd64-3.9\cmake-build\lib\Release\test.py
isNumpy = False
try:
    import numpy
    isNumpy = True
except Exception as e:
    isNumpy = False

def exitWithError(s):

    text = ""

    if isinstance(s, Exception):

        try:
            tb = traceback.TracebackException.from_exception(s)
            dep = len(tb.stack)
            filename = os.path.basename(str(tb.stack[dep-1][0]))
            lineno = str(tb.stack[dep-1][1])
            reason = str(tb._str)
            if not reason:
                reason = str(tb.exc_type)
            stack = ""
            for st in tb.stack:
                stack += "  %s(%s): %s() : %s\n" % (st[0], st[1], st[2], st[3])
            text = "%s(%s): [\033[91mERROR\033[0m] %s\n%s" % (filename, lineno, reason, stack)

        except Exception as e:
            st = inspect.stack()
            dep = len(st)
            fi = inspect.getframeinfo(st[dep-1][0])
            reason = traceback.format_exc()
            text += "\n%s:%s(%s): [\033[91mERROR\033[0m] %s" % (os.path.basename(fi.filename), fi.function, fi.lineno, reason)

    if not text:
        st = inspect.stack()
        fi = inspect.getframeinfo(st[1][0])
        text += "%s:%s(%s): [\033[91mERROR\033[0m] %s" % (os.path.basename(fi.filename), fi.function, fi.lineno, s)

    print(text)
    exit(-1)


def runTests(_p):

    print("\n------------------------- Starting tests -------------------------")
    print("PARAMETERS  : %s" % _p)
    print("PYTHON      : %s" % sys.version.replace("\n", ""))
    print("WORKING DIR : %s" % os.getcwd())
    print("------------------------------------------------------------------")

    # Assert macros
    assert True
    assert not False

    # from pymembus import pymembus
    import pymembus
    if hasattr(pymembus, "pymembus"):
        pymembus = pymembus.pymembus

    # Module attributes
    print(dir(pymembus))

    # for k in dir(pymembus):
    #     print("%s = %s" % (k, getattr(pymembus, k)))

    print("[%s] %s" % (pymembus.__name__, pymembus.__file__))

    # Show version number
    print("pymembus version : %s [%s]" % (pymembus.__version__, pymembus.__build__))

    #----------------------------------------------------------------
    # Map shared memory
    sm = pymembus.memmap()
    assert sm.open("/myshare", 1024, True)

    # Write string
    msg = str(time.time())
    assert 0 < sm.write(msg)

    # Read the string
    assert sm.read(len(msg)) == msg

    if isNumpy:
        mem = numpy.array(sm, copy = False)
        print("MEM: %s" % str(mem))

    sm.close()


    #----------------------------------------------------------------
    # Shared message buffer
    tx = pymembus.memmsg()
    assert tx.open("/mymsg", 1024, True, True)
    assert not tx.existing()

    rx = pymembus.memmsg()
    assert rx.open("/mymsg", 1024, False, False)
    assert rx.existing()

    for i in range(0, 10):
        # print("WRITE: %s" % i)
        assert tx.write("Message %s" % i)

    i = 0
    max = 20
    while 10 > i and 0 < max:
        max -= 1
        msg = rx.read(0)
        if 0 < len(msg):
            # print("READ : %s" % msg)
            i += 1

    print("i = %s" % i)

    assert 10 <= i

    tx.close()
    rx.close()

    #----------------------------------------------------------------
    # Huge write test
    print("Huge write test")

    for b in range(0, 128):

        assert tx.open("/mymsg", 64 + b, True, True)
        assert not tx.existing()
        assert rx.open("/mymsg", 64 + b, False, False)
        assert rx.existing()

        for i in range(0, 1000):
            msg = "Message %s-%s" % (b, i)
            assert tx.write(msg)
            rmsg = rx.read(0)
            assert rmsg == msg

        tx.close()
        rx.close()

    for b in range(128, 0):

        assert tx.open("/mymsg", 64 + b, True, True)
        assert not tx.existing()
        assert rx.open("/mymsg", 64 + b, False, False)
        assert rx.existing()

        for i in range(0, 1000):
            msg = "Message %s-%s" % (b, i)
            assert tx.write(msg)
            rmsg = rx.read(0)
            assert rmsg == msg

        tx.close()
        rx.close()

    #----------------------------------------------------------------
    # Shared image
    print("Shared image test")

    imgs = pymembus.memvid()

    # Make sure getBuf() on invalid object throws
    asserted = False
    try:
        img = imgs[0]
    except Exception as e:
        asserted = True
    assert asserted

    # Open a share
    w = 320
    h = 240
    bpp = 24
    fps = 30
    bufs = 10
    assert imgs.open("/myvideo", True, w, h, bpp, fps, bufs)

    # Check values
    assert imgs.getWidth() == w
    assert imgs.getHeight() == h
    assert imgs.getBpp() == bpp
    assert imgs.getFps() == fps
    assert imgs.getBufs() == bufs
    assert imgs.getPtr(0) == 0
    assert imgs.next(1) == 1
    assert imgs.next(-1) == 0
    assert imgs.getPtrErr(3, 1) == 2
    assert len(imgs) == bufs

    # Check second share
    imgs2 = pymembus.memvid()
    assert imgs2.open_existing("/myvideo")
    assert imgs2.getWidth() == w
    assert imgs2.getHeight() == h
    assert imgs2.getBpp() == bpp
    assert imgs2.getFps() == fps
    assert imgs2.getBufs() == bufs
    imgs2.close()

    if isNumpy:

        # Write into the image buffer
        img = numpy.array(imgs[0], copy = False)

        try:
            import cv2
            cv2.rectangle(img, (10, 10), (60, 60), (50,255,50), -1)
            cv2.rectangle(img, (50, 50), (110, 110), (255,50,50), -1)
            cv2.rectangle(img, (100, 100), (150, 150), (50,50,255), -1)

        except Exception as e:
            print(e)


    #----------------------------------------------------------------
    # Shared audio
    print("Shared audio test")

    auds = pymembus.memaud()

    ch = 2
    bps = 16
    abr = 48000
    fps = 50
    bufs = 10
    assert auds.open("/myaudio", True, ch, bps, abr, fps, bufs)
    assert auds.getChannels() == ch
    assert auds.getBps() == bps
    assert auds.getBitRate() == abr
    assert auds.getFps() == fps
    assert auds.getBufs() == bufs
    assert len(auds) == bufs
    print("%s -- %s" % (auds.getBufSize(), (abr / fps)))
    assert auds.getBufSize() == (abr / fps)

    auds2 = pymembus.memaud()
    assert auds2.open_existing("/myaudio")
    assert auds2.getChannels() == ch
    assert auds2.getBps() == bps
    assert auds2.getBitRate() == abr
    assert auds2.getFps() == fps
    assert auds2.getBufs() == bufs

    if isNumpy:

        aud = numpy.array(auds[0], copy = False)
        aud2 = numpy.array(auds2[0], copy = False)

        # Create numpy audio buffer
        msamples = int(abr / fps)
        nsamples = msamples * ch
        src = numpy.zeros((1, nsamples), dtype='int16')
        src.fill(0)

        dch, dsz = aud.shape
        sch, ssz = src.shape

        # Ensure channel sizes match
        print("%s : %s --- %s : %s" % (dch, dsz, sch, ssz))
        assert dch == sch
        assert dsz == ssz

        # Check share
        aud[0][3] = 1234
        assert aud[0][3] == aud2[0][3]

        # Check the fill function
        auds.fill(0, 0)
        assert aud[0][3] == 0

        # Copy data
        aud = src

    auds.close()
    auds2.close()

    print("--- SUCCESS --- ")


def main():

    #---------------------------------------------------------------
    # Parse command line arguments
    ap = argparse.ArgumentParser(description='Test')
    ap.add_argument('--output', '-o', default='', type=str, help='Output file or directory')
    _p = vars(ap.parse_args())

    try:
        runTests(_p)

    except Exception as e:
        exitWithError(e)

if __name__ == '__main__':
    main()

