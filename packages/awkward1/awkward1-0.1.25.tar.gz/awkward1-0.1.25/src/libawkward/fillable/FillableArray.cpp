// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#include <sstream>

#include "awkward/type/ArrayType.h"

#include "awkward/fillable/FillableArray.h"

namespace awkward {
  const std::string FillableArray::tostring() const {
    std::stringstream out;
    out << "<FillableArray length=\"" << length() << "\" type=\"" << type().get()->tostring() << "\"/>";
    return out.str();
  }

  int64_t FillableArray::length() const {
    return fillable_.get()->length();
  }

  void FillableArray::clear() {
    fillable_.get()->clear();
  }

  const std::shared_ptr<Type> FillableArray::type() const {
    return std::shared_ptr<Type>(new ArrayType(fillable_.get()->type(), fillable_.get()->length()));
  }

  const std::shared_ptr<Content> FillableArray::snapshot() const {
    return fillable_.get()->snapshot();
  }

  const std::shared_ptr<Content> FillableArray::getitem_at(int64_t at) const {
    return snapshot().get()->getitem_at(at);
  }

  const std::shared_ptr<Content> FillableArray::getitem_range(int64_t start, int64_t stop) const {
    return snapshot().get()->getitem_range(start, stop);
  }

  const std::shared_ptr<Content> FillableArray::getitem_field(const std::string& key) const {
    return snapshot().get()->getitem_field(key);
  }

  const std::shared_ptr<Content> FillableArray::getitem_fields(const std::vector<std::string>& keys) const {
    return snapshot().get()->getitem_fields(keys);
  }

  const std::shared_ptr<Content> FillableArray::getitem(const Slice& where) const {
    return snapshot().get()->getitem(where);
  }

  bool FillableArray::active() const {
    return fillable_.get()->active();
  }

  void FillableArray::null() {
    maybeupdate(fillable_.get()->null());
  }

  void FillableArray::boolean(bool x) {
    maybeupdate(fillable_.get()->boolean(x));
  }

  void FillableArray::integer(int64_t x) {
    maybeupdate(fillable_.get()->integer(x));
  }

  void FillableArray::real(double x) {
    maybeupdate(fillable_.get()->real(x));
  }

  void FillableArray::beginlist() {
    maybeupdate(fillable_.get()->beginlist());
  }

  void FillableArray::endlist() {
    Fillable* tmp = fillable_.get()->endlist();
    if (tmp == nullptr) {
      throw std::invalid_argument("endlist doesn't match a corresponding beginlist");
    }
    maybeupdate(tmp);
  }

  void FillableArray::begintuple(int64_t numfields) {
    maybeupdate(fillable_.get()->begintuple(numfields));
  }

  void FillableArray::index(int64_t index) {
    maybeupdate(fillable_.get()->index(index));
  }

  void FillableArray::endtuple() {
    maybeupdate(fillable_.get()->endtuple());
  }

  void FillableArray::beginrecord() {
    beginrecord(0);
  }

  void FillableArray::beginrecord(int64_t disambiguator) {
    maybeupdate(fillable_.get()->beginrecord(disambiguator));
  }

  void FillableArray::field_fast(const char* key) {
    maybeupdate(fillable_.get()->field_fast(key));
  }

  void FillableArray::field_check(const char* key) {
    maybeupdate(fillable_.get()->field_check(key));
  }

  void FillableArray::endrecord() {
    maybeupdate(fillable_.get()->endrecord());
  }

  void FillableArray::maybeupdate(Fillable* tmp) {
    if (tmp != fillable_.get()  &&  tmp != nullptr) {
      fillable_ = std::shared_ptr<Fillable>(tmp);
    }
  }
}

uint8_t awkward_FillableArray_length(void* fillablearray, int64_t* result) {
  awkward::FillableArray* obj = reinterpret_cast<awkward::FillableArray*>(fillablearray);
  try {
    *result = obj->length();
  }
  catch (...) {
    return 1;
  }
  return 0;
}

uint8_t awkward_FillableArray_clear(void* fillablearray) {
  awkward::FillableArray* obj = reinterpret_cast<awkward::FillableArray*>(fillablearray);
  try {
    obj->clear();
  }
  catch (...) {
    return 1;
  }
  return 0;
}

uint8_t awkward_FillableArray_null(void* fillablearray) {
  awkward::FillableArray* obj = reinterpret_cast<awkward::FillableArray*>(fillablearray);
  try {
    obj->null();
  }
  catch (...) {
    return 1;
  }
  return 0;
}

uint8_t awkward_FillableArray_boolean(void* fillablearray, bool x) {
  awkward::FillableArray* obj = reinterpret_cast<awkward::FillableArray*>(fillablearray);
  try {
    obj->boolean(x);
  }
  catch (...) {
    return 1;
  }
  return 0;
}

uint8_t awkward_FillableArray_integer(void* fillablearray, int64_t x) {
  awkward::FillableArray* obj = reinterpret_cast<awkward::FillableArray*>(fillablearray);
  try {
    obj->integer(x);
  }
  catch (...) {
    return 1;
  }
  return 0;
}

uint8_t awkward_FillableArray_real(void* fillablearray, double x) {
  awkward::FillableArray* obj = reinterpret_cast<awkward::FillableArray*>(fillablearray);
  try {
    obj->real(x);
  }
  catch (...) {
    return 1;
  }
  return 0;
}

uint8_t awkward_FillableArray_beginlist(void* fillablearray) {
  awkward::FillableArray* obj = reinterpret_cast<awkward::FillableArray*>(fillablearray);
  try {
    obj->beginlist();
  }
  catch (...) {
    return 1;
  }
  return 0;
}

uint8_t awkward_FillableArray_endlist(void* fillablearray) {
  awkward::FillableArray* obj = reinterpret_cast<awkward::FillableArray*>(fillablearray);
  try {
    obj->endlist();
  }
  catch (...) {
    return 1;
  }
  return 0;
}
