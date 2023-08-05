#ifndef READER_H
#define READER_H

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "orc/OrcFile.hh"

#include "Converter.h"
#include "TypeDescription.h"

namespace py = pybind11;

class ORCIterator
{
  protected:
    uint64_t batchItem;
    orc::RowReaderOptions rowReaderOpts;
    std::unique_ptr<orc::RowReader> rowReader;
    std::unique_ptr<orc::ColumnVectorBatch> batch;
    std::unique_ptr<Converter> converter;

  public:
    uint64_t currentRow;
    uint64_t firstRowOfStripe;
    virtual uint64_t len() const = 0;
    py::object next();
    py::object read(int64_t = -1);
    uint64_t seek(int64_t, uint16_t = 0);
    const orc::RowReaderOptions getRowReaderOptions() const { return rowReaderOpts; };
};

class Stripe; /* Forward declaration */

class Reader : public ORCIterator
{
  private:
    std::unique_ptr<orc::Reader> reader;
    std::unique_ptr<TypeDescription> typeDesc;
    uint64_t batchSize;
    unsigned int structKind;

  public:
    Reader(py::object,
           uint64_t = 1024,
           std::list<uint64_t> = {},
           std::list<std::string> = {},
           unsigned int = 0);
    uint64_t len() const override;
    uint64_t numberOfStripes() const;
    TypeDescription& schema();
    Stripe readStripe(uint64_t);

    const orc::Reader& getORCReader() const { return *reader; }
    const uint64_t getBatchSize() const { return batchSize; }
    const unsigned int getStructKind() const { return structKind; }
};

class Stripe : public ORCIterator
{
  private:
    uint64_t stripeIndex;
    std::unique_ptr<orc::StripeInformation> stripeInfo;
    const Reader& reader;

  public:
    Stripe(const Reader&, uint64_t, std::unique_ptr<orc::StripeInformation>);
    py::object bloomFilterColumns();
    uint64_t len() const override;
    uint64_t length() const;
    uint64_t offset() const;
    std::string writerTimezone();
};

#endif