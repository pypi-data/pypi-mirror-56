// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#ifndef AWKWARD_TYPE_H_
#define AWKWARD_TYPE_H_

#include <memory>

#include "awkward/cpu-kernels/util.h"

namespace awkward {
  class Type {
  public:
    virtual ~Type() { }

    std::string tostring() const { return tostring_part("", "", ""); };
    virtual std::string tostring_part(std::string indent, std::string pre, std::string post) const = 0;
    virtual const std::shared_ptr<Type> shallow_copy() const = 0;
    virtual bool equal(std::shared_ptr<Type> other) const = 0;
    virtual bool compatible(std::shared_ptr<Type> other, bool bool_is_int, bool int_is_float, bool ignore_null, bool unknown_is_anything) const = 0;
  };
}

#endif // AWKWARD_TYPE_H_
