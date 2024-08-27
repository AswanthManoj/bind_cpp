#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <string>
#include <vector>
#include <map>
#include <functional>

namespace py = pybind11;

class Element {
public:
    Element(std::string tag, bool closing_tag = true)
        : tag(tag), closing_tag(closing_tag), end_tag("</" + tag + ">"),
          starting_tag("<" + tag + " ") {}

    std::string operator()(py::args args, py::kwargs kwargs) const {
        std::string attr_str;
        std::string content_str;

        // Handle attributes
        for (const auto& item : kwargs) {
            std::string key = py::cast<std::string>(item.first);
            std::string value = py::cast<std::string>(item.second);
            if (key == "cls") {
                key = "class";
            } else {
                key = std::string(py::str(item.first));
            }
            attr_str += key + "=\"" + value + "\" ";
        }

        // Handle content
        for (const auto& arg : args) {
            content_str += py::cast<std::string>(arg);
        }

        std::string result = starting_tag + attr_str;
        if (closing_tag) {
            result += ">" + content_str + end_tag;
        } else {
            result += "/>";
        }

        return result;
    }

private:
    std::string tag;
    bool closing_tag;
    std::string end_tag;
    std::string starting_tag;
};

std::function<std::string(py::args, py::kwargs)> create_element(const std::string& tag, bool closing_tag = true) {
    Element element(tag, closing_tag);
    return [element](py::args args, py::kwargs kwargs) -> std::string {
        return element(args, kwargs);
    };
}

std::string render(const std::vector<std::string>& html) {
    std::string result;
    for (const auto& part : html) {
        result += part;
    }
    return result;
}

PYBIND11_MODULE(html_generator, m) {
    py::class_<Element>(m, "Element")
        .def(py::init<std::string, bool>())
        .def("__call__", &Element::operator())
        .def("__str__", [](const Element& e) { return e(py::args(), py::kwargs()); });

    m.def("create_element", &create_element, py::arg("tag"), py::arg("closing_tag") = true);
    m.def("render", &render);
}