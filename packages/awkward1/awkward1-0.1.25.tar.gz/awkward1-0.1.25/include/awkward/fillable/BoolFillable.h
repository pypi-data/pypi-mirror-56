// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#ifndef AWKWARD_BOOLFILLABLE_H_
#define AWKWARD_BOOLFILLABLE_H_

#include "awkward/cpu-kernels/util.h"
#include "awkward/fillable/FillableOptions.h"
#include "awkward/fillable/GrowableBuffer.h"
#include "awkward/fillable/Fillable.h"

namespace awkward {
  class BoolFillable: public Fillable {
  public:
    BoolFillable(const FillableOptions& options, const GrowableBuffer<uint8_t>& buffer): options_(options), buffer_(buffer) { }

    static BoolFillable* fromempty(const FillableOptions& options) {
      return new BoolFillable(options, GrowableBuffer<uint8_t>::empty(options));
    }

    virtual int64_t length() const;
    virtual void clear();
    virtual const std::shared_ptr<Type> type() const;
    virtual const std::shared_ptr<Content> snapshot() const;

    virtual bool active() const;
    virtual Fillable* null();
    virtual Fillable* boolean(bool x);
    virtual Fillable* integer(int64_t x);
    virtual Fillable* real(double x);
    virtual Fillable* beginlist();
    virtual Fillable* endlist();
    virtual Fillable* begintuple(int64_t numfields);
    virtual Fillable* index(int64_t index);
    virtual Fillable* endtuple();
    virtual Fillable* beginrecord(int64_t disambiguator);
    virtual Fillable* field_fast(const char* key);
    virtual Fillable* field_check(const char* key);
    virtual Fillable* endrecord();

  private:
    const FillableOptions options_;
    GrowableBuffer<uint8_t> buffer_;
  };
}

#endif // AWKWARD_BOOLFILLABLE_H_
