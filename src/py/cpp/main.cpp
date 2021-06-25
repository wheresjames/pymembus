
#include <libmembus.h>
#include <pybind11/pybind11.h>

#include "pymembus.h"
using namespace mmb;

namespace py = pybind11;
namespace PYMEMBUS_NS
{

PYBIND11_MODULE(APPNAMERAW, m)
{
    m.doc() = APPDESC;
    m.attr("__version__") = APPVER;
    m.attr("__build__") = APPBUILD;
    m.def("version", [] () { return APPVER; });
    m.def("build", [] () { return APPBUILD; });

    py::class_<memmap>(m, "memmap", py::buffer_protocol())
        .def(py::init<>())
        .def("open", &memmap::open,
                        py::arg("sName"),
                        py::arg("nSize"),
                        py::arg("bCreate") = false,
                        py::arg("bNew") = false
            )
        .def("close", &memmap::close)
        .def("existing", &memmap::existing)
        .def("isOpen", &memmap::isOpen)
        .def("read", &memmap::read,
                        py::arg("sz") = -1)
        .def("write", &memmap::write)
        .def("size", &memmap::size)
        .def_buffer([](memmap &m) -> py::buffer_info
        {   return py::buffer_info(
                m.data(),                                   // Data pointer
                sizeof(char),                               // Size of data element
                py::format_descriptor<char>::format(),      // Data format
                1,                                          // Dimemsions
                { m.size() },                               // Buffer dimensions
                { sizeof(char) }                            // Buffer stride in bytes
            );
        });
        ;

    py::class_<memvid::vidview>(m, "vidview", py::buffer_protocol())
        .def_buffer([](memvid::vidview &m) -> py::buffer_info
        {   return py::buffer_info(
                m.m_ptr,                                            // Data pointer
                sizeof(char),                                       // Size of data element
                py::format_descriptor<unsigned char>::format(),     // Data format
                3,                                                  // Dimemsions
                { (int)m.m_h, (int)m.m_w, 3 },                      // Buffer dimensions
                { (int)m.m_sw, 3, 1 }                               // Buffer stride in bytes
            );
        });
        ;

    py::class_<memvid>(m, "memvid")
        .def(py::init<>())
        .def("open", &memvid::open)
        .def("open_existing", &memvid::open_existing)
        .def("close", &memvid::close)
        .def("existing", &memvid::existing)
        .def("isOpen", &memvid::isOpen)
        .def("getBuf", &memvid::getBuf)
        .def("fill", &memvid::fill)
        .def("__getitem__",[](memvid& r, long i) {return r.getBuf(i);})
        .def("getBufs", &memvid::getBufs)
        .def("__len__", &memvid::getBufs)
        .def("getPtr", &memvid::getPtr)
        .def("setPtr", &memvid::setPtr)
        .def("getPtrErr", &memvid::getPtrErr)
        .def("next", &memvid::next)
        .def("getWidth", &memvid::getWidth)
        .def("getHeight", &memvid::getHeight)
        .def("getBpp", &memvid::getBpp)
        .def("getFps", &memvid::getFps)
        ;

    py::class_<memaud::audview>(m, "audview", py::buffer_protocol())
        .def_buffer([](memaud::audview &m) -> py::buffer_info
        {   return py::buffer_info(
                m.m_ptr,                                                // Data pointer
                2,                                                      // Size of data element
                py::format_descriptor<int16_t>::format(),               // Data format
                2,                                                      // Dimemsions
                { (int)1, (int)(m.m_size / 2)},                         // Buffer dimensions
                { (int)(m.m_size), (int)2}                              // Buffer stride in bytes
            );
        });
        ;

    py::class_<memaud>(m, "memaud")
        .def(py::init<>())
        .def("open", &memaud::open)
        .def("open_existing", &memaud::open_existing)
        .def("close", &memaud::close)
        .def("existing", &memaud::existing)
        .def("isOpen", &memaud::isOpen)
        .def("getBuf", &memaud::getBuf)
        .def("fill", &memaud::fill)
        .def("__getitem__",[](memaud& r, long i) {return r.getBuf(i);})
        .def("getBufs", &memaud::getBufs)
        .def("__len__", &memaud::getBufs)
        .def("getPtr", &memaud::getPtr)
        .def("setPtr", &memaud::setPtr)
        .def("getPtrErr", &memaud::getPtrErr)
        .def("next", &memaud::next)
        .def("getChannels", &memaud::getChannels)
        .def("getBps", &memaud::getBps)
        .def("getBitRate", &memaud::getBitRate)
        .def("getFps", &memaud::getFps)
        .def("getBufSize", &memaud::getBufSize)
        ;

    py::class_<memmsg>(m, "memmsg")
        .def(py::init<>())
        .def("open", &memmsg::open)
        .def("close", &memmsg::close)
        .def("existing", &memmsg::existing)
        .def("write", &memmsg::write)
        .def("read", &memmsg::read)
        ;

}

}; // end namespace

