// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#ifndef AWKWARD_TUPLEFILLABLE_H_
#define AWKWARD_TUPLEFILLABLE_H_

#include <vector>

#include "awkward/cpu-kernels/util.h"
#include "awkward/fillable/FillableOptions.h"
#include "awkward/fillable/GrowableBuffer.h"
#include "awkward/fillable/Fillable.h"
#include "awkward/fillable/UnknownFillable.h"

namespace awkward {
  class TupleFillable: public Fillable {
  public:
    TupleFillable(const FillableOptions& options, const std::vector<std::shared_ptr<Fillable>>& contents, int64_t length, bool begun, size_t nextindex)
        : options_(options)
        , contents_(contents)
        , length_(length)
        , begun_(begun)
        , nextindex_(nextindex) { }

    static TupleFillable* fromempty(const FillableOptions& options) {
      return new TupleFillable(options, std::vector<std::shared_ptr<Fillable>>(), -1, false, -1);
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

    int64_t numfields() const { return (int64_t)contents_.size(); }

  private:
    const FillableOptions options_;
    std::vector<std::shared_ptr<Fillable>> contents_;
    int64_t length_;
    bool begun_;
    int64_t nextindex_;

    void maybeupdate(int64_t i, Fillable* tmp);
  };
}

#endif // AWKWARD_TUPLEFILLABLE_H_
