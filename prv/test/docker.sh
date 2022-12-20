#!/bin/bash

SCRIPTPATH=$(realpath ${BASH_SOURCE[0]})
ROOTDIR=$(dirname $SCRIPTPATH)
if [[ -f "${ROOTDIR}/rbashutils.sh" ]]; then
    . "${ROOTDIR}/rbashutils.sh"
elif [[ -f "${ROOTDIR}/../sh/rbashutils.sh" ]]; then
    . "${ROOTDIR}/../sh/rbashutils.sh"
else
    echo "rbashutils.sh not found"
    exit -1
fi

#--------------------------------------------------------------------------------------------------
# Functions

installCMake()
{
    CMAKEVER=$1

    showInfo "Installing CMake version $CMAKEVER"

    apt-get -yqq update
    apt-get -yqq install libssl-dev

    mkdir -p /code/cmake
    cd /code/cmake

    git clone https://github.com/Kitware/CMake.git ./
    exitOnError "Failed to clone cmake"

    git checkout $CMAKEVER
    exitOnError "Failed to checkout tag : $CMAKEVER"

    ./bootstrap
    exitOnError "Failed to bootstrap cmake version $CMAKEVER"

    make -j8
    exitOnError "Failed to build cmake version $CMAKEVER"

    make install
    exitOnError "Failed to install cmake version $CMAKEVER"

    cd /code
    rm -Rf /code/cmake
}


#--------------------------------------------------------------------------------------------------
if [[ $1 == "check-cmake" ]]; then

    CMAKEVER=$(cmake --version)
    echo "$CMAKEVER"
    if compareVersion "$CMAKEVER" "$2" "<"; then
        echo "CMake version is below $2, installing $3"
        installCMake "$3"
    fi

fi


#--------------------------------------------------------------------------------------------------
if [[ $1 == "test-cmake" ]]; then

    showBanner "CMake Test"

    cp -R /code/pymembus /code/pymembus-cmake
    exitOnError "test-cmake: Failed to copy to directory : /code/pymembus-cmake"

    cd /code/pymembus-cmake
    exitOnError "test-cmake: Failed to switch to directory : /code/pymembus-cmake"

    ./clean.sh

    ./add.sh cmake -y
    exitOnError "test-cmake: Failed to add cmake to project"

    cmake . -B ./bld -G "Unix Makefiles"
    exitOnError "test-cmake: Failed to configure"

    cmake --build ./bld
    exitOnError "test-cmake: Failed to build"

    cmake --install ./bld
    exitOnError "test-cmake: Failed to install"

    pymembus uninstall
    exitOnError "test-cmake: Failed to uninstall"

    # --- Install with deb file

    # cpack -B ./pck --config ./bld/CPackConfig.cmake -G DEB -C Release
    # exitOnError "test-conan: Failed to create package"

    # sudo apt install ./pck/pymembus-0.1.0-Linux.deb
    # exitOnError "test-conan: Failed to install deb package"

    # pymembus test
    # exitOnError "test-cmake: Failed to test"

    # apt remove pymembus
    # exitOnError "test-cmake: Failed to uninstall"

fi


#--------------------------------------------------------------------------------------------------
if [[ $1 == "test-pip" ]]; then

    showBanner "pip Test"

    apt-get -yqq update
    apt-get -yqq install python3 python3-pip
    exitOnError "test-pip: Failed to install dependencies"

    cp -R /code/pymembus /code/pymembus-pip
    exitOnError "test-pip: Failed to copy to directory : /code/pymembus-pip"

    cd /code/pymembus-pip
    exitOnError "test-pip: Failed to switch to directory : /code/pymembus-pip"

    ./clean.sh

    # ./add.sh pip -y
    # exitOnError "test-pip: Failed to add pip to project"

    pip3 install .
    exitOnError "test-pip: Failed to install pip module"

    pip3 list

    # export PYTHONPATH=${PYTHONPATH}:/usr/local/

    # python3 ./src/pytest/py/test.py
    # exitOnError "test-pip: Failed to pass test"

    pip3 uninstall -y pymembus
    exitOnError "test-pip: Failed to uninstall"

fi



