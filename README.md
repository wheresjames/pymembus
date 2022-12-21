
# pymembus


---------------------------------------------------------------------
## Table of contents

* [Install from pypi](#install-from-pypi)
* [Local Build](#local-build)
* [Administration](#administration)
* [Examples](#examples)
* [References](#references)

&nbsp;


---------------------------------------------------------------------
## Install from pypi

    Install dependencies (see below) then run...

    $ pip install pymembus

&nbsp;


---------------------------------------------------------------------
## Local Build

### Windows dependencies

- Install [CMake](https://cmake.org/download/)
- Install [git](https://git-scm.com/downloads)
- Install [boost](https://sourceforge.net/projects/boost/files/boost-binaries/)
- Install [Visual Studio 2017](https://visualstudio.microsoft.com/downloads/). *The free **Community Edition** is fine*


### Linux dependencies

    $ sudo apt-get update
    $ sudo apt-get -yq install build-essential git cmake libboost-all-dev doxygen graphviz go-md2man
    $ sudo apt-get -yq install python3 python3-pip python3-python11
    $ python3 -m pip install scikit-build


### Local Build / Install

    $ python3 -m pip install .

OR

    $ pip3 install .


### Uninstall

    $ pip3 uninstall -y pymembus


### Create wheel

    Software dist
    $ python3 setup.py sdist

    Binary dist
    $ python3 setup.py bdist_wheel

OR

    $ pip3 wheel . --use-feature=in-tree-build

&nbsp;


---------------------------------------------------------------------
## Administration (Linux only)

Library commands, for once you have it installed

- Display help

    **$ pymembus help**

- Uninstall

    **$ sudo pymembus uninstall**

- Show installation roots

    **$ pymembus files**

- Get installation information.  (Change this info in **PROJECT.txt**)

    **$ pymembus info \<variable\>**

    variable = One of [name, description, url, version, build, company, author, lib, include, bin, share]

&nbsp;


---------------------------------------------------------------------
## Examples

``` Python

    import pymembus

    #----------------------------------------------------------------
    # Map shared memory

    sm = pymembus.memmap()
    assert sm.open("/myshare", 1024, True)

    # Write string
    msg = str(time.time())
    assert 0 < sm.write(msg)

    # Read the string
    assert sm.read(len(msg)) == msg

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
    # Shared image
    imgs = pymembus.memvid()

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

```

&nbsp;


---------------------------------------------------------------------
## References

- Python
    - https://www.python.org/

- CMake
    - https://cmake.org

- pip
    - https://pip.pypa.io/en/stable/

- git
    - https://git-scm.com/

- Boost
    - https://www.boost.org/

- Visual Studio
    - https://visualstudio.microsoft.com/

- Doxygen
    - https://github.com/doxygen/doxygen

- Graphviz
    - https://graphviz.org/

- Md2man
    - https://sunaku.github.io/md2man/man/man5/md2man.5.html
    - https://github.com/sunaku/md2man
