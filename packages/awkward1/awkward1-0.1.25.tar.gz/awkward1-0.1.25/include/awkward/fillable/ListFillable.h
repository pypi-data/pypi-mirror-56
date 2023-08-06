// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#ifndef AWKWARD_LISTFILLABLE_H_
#define AWKWARD_LISTFILLABLE_H_

#include <vector>

#include "awkward/cpu-kernels/util.h"
#include "awkward/fillable/FillableOptions.h"
#include "awkward/fillable/GrowableBuffer.h"
#include "awkward/fillable/Fillable.h"
#include "awkward/fillable/UnknownFillable.h"

namespace awkward {
  class ListFillable: public Fillable {
  public:
    ListFillable(const FillableOptions& options, const GrowableBuffer<int64_t>& offsets, Fillable* content, bool begun): options_(options), offsets_(offsets), content_(std::shared_ptr<Fillable>(content)), begun_(begun) { }

    static ListFillable* fromempty(const FillableOptions& options) {
      GrowableBuffer<int64_t> offsets = GrowableBuffer<int64_t>::empty(options);
      offsets.append(0);
      return new ListFillable(options, offsets, UnknownFillable::fromempty(options), false);
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
    GrowableBuffer<int64_t> offsets_;
    std::shared_ptr<Fillable> content_;
    bool begun_;

    Fillable* maybeupdate(Fillable* tmp);
  };
}

#endif // AWKWARD_LISTFILLABLE_H_
