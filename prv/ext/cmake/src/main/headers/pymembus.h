#pragma once

#define PYMEMBUS_NS pmb

namespace PYMEMBUS_NS
{

#if defined(_WIN32)
#define   PYMEMBUS_WINDOWS
#else
#define   PYMEMBUS_POSIX
#endif

}; // end namespace

#include "pymembus/sys.h"
#include "pymembus/blank.h"
