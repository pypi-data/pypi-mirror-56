#include "Reader.h"
#include "TypeDescription.h"
#include "Writer.h"

namespace py = pybind11;

PYBIND11_MODULE(_pyorc, m)
{
    m.doc() = "_pyorc c++ extension";
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) {
                std::rethrow_exception(p);
            }
        } catch (const orc::ParseError& e) {
            py::object err = py::module::import("pyorc.errors").attr("ParseError");
            PyErr_SetString(err.ptr(), e.what());
        }
    });
    py::class_<TypeDescription>(m, "typedescription")
      .def(py::init<std::string>(), py::arg("str_schema"))
      .def(py::init<int>(), py::arg("kind"))
      .def("__str__", [](TypeDescription& td) -> std::string { return td.str(); })
      .def_property_readonly("kind", [](TypeDescription& td) { return td.getKind(); })
      .def_property_readonly("column_id",
                             [](TypeDescription& td) { return td.getColumnId(); })
      .def_property("container_types",
                    &TypeDescription::getContainerTypes,
                    &TypeDescription::setContainerTypes)
      .def_property(
        "precision", &TypeDescription::getPrecision, &TypeDescription::setPrecision)
      .def_property("scale", &TypeDescription::getScale, &TypeDescription::setScale)
      .def_property(
        "max_length", &TypeDescription::getMaxLength, &TypeDescription::setMaxLength)
      .def_readonly("fields", &TypeDescription::fields, py::return_value_policy::copy)
      .def("add_field", &TypeDescription::addField)
      .def("remove_field", &TypeDescription::removeField)
      .def("find_column_id", &TypeDescription::findColumnId);
    py::class_<Stripe>(m, "stripe")
      .def(
        py::init([](Reader& reader, uint64_t num) { return reader.readStripe(num); }),
        py::keep_alive<0, 2>())
      .def("__next__", [](Stripe& s) -> py::object { return s.next(); })
      .def("__iter__", [](Stripe& s) -> Stripe& { return s; })
      .def("__len__", &Stripe::len)
      .def("read", &Stripe::read, py::arg_v("num", -1, "-1"))
      .def("seek", &Stripe::seek, py::arg("row"), py::arg_v("whence", 0, "0"))
      .def_property_readonly("bytes_length", [](Stripe& s) { return s.length(); })
      .def_property_readonly("bytes_offset", [](Stripe& s) { return s.offset(); })
      .def_property_readonly("bloom_filter_columns",
                             [](Stripe& s) { return s.bloomFilterColumns(); })
      .def_property_readonly("writer_timezone",
                             [](Stripe& s) { return s.writerTimezone(); })
      .def_readonly("current_row", &Stripe::currentRow)
      .def_readonly("row_offset", &Stripe::firstRowOfStripe);
    py::class_<Reader>(m, "reader")
      .def(py::init<py::object,
                    uint64_t,
                    std::list<uint64_t>,
                    std::list<std::string>,
                    unsigned int>(),
           py::arg("fileo"),
           py::arg_v("batch_size", 1024, "1024"),
           py::arg_v("col_indices", std::list<uint64_t>{}, "None"),
           py::arg_v("col_names", std::list<std::string>{}, "None"),
           py::arg_v("struct_repr", 0, "StructRepr.TUPLE"))
      .def("__next__", [](Reader& r) -> py::object { return r.next(); })
      .def("__iter__", [](Reader& r) -> Reader& { return r; })
      .def("__len__", &Reader::len)
      .def("read", &Reader::read, py::arg_v("num", -1, "-1"))
      .def("read_stripe", &Reader::readStripe, py::keep_alive<0, 1>())
      .def("seek", &Reader::seek, py::arg("row"), py::arg_v("whence", 0, "0"))
      .def_property_readonly("schema", &Reader::schema)
      .def_property_readonly("num_of_stripes",
                             [](Reader& r) { return r.numberOfStripes(); })
      .def_readonly("current_row", &Reader::currentRow);
    py::class_<Writer>(m, "writer")
      .def(py::init<py::object,
                    TypeDescription&,
                    uint64_t,
                    uint64_t,
                    int,
                    int,
                    uint64_t,
                    std::set<uint64_t>,
                    double,
                    unsigned int>(),
           py::arg("fileo"),
           py::arg("schema"),
           py::arg_v("batch_size", 1024, "1024"),
           py::arg_v("stripe_size", 67108864, "67108864"),
           py::arg_v("compression", 1, "CompressionKind.ZLIB"),
           py::arg_v("compression_strategy", 0, "CompressionStrategy.SPEED"),
           py::arg_v("compression_block_size", 65536, "65536"),
           py::arg_v("bloom_filter_columns", std::set<uint64_t>{}, "None"),
           py::arg_v("bloom_filter_fpp", 0.05, "0.05"),
           py::arg_v("struct_repr", 0, "StructRepr.TUPLE"))
      .def("write", &Writer::write)
      .def("close", &Writer::close)
      .def_readonly("current_row", &Writer::currentRow);
}