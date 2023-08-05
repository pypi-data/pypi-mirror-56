import pytest

import io
import string
import tempfile

from pyorc import (
    Reader,
    Writer,
    typedescription,
    TypeKind,
    StructRepr,
    ParseError,
    stripe as Stripe,
)


@pytest.fixture
def orc_data():
    def _init(row):
        data = io.BytesIO()
        with Writer(
            data, "struct<col0:int,col1:string>", struct_repr=StructRepr.DICT
        ) as writer:
            for i in range(row):
                writer.write(
                    {
                        "col0": i,
                        "col1": "Test {0}".format(string.ascii_uppercase[i % 26]),
                    }
                )
        data.seek(0)
        return data

    return _init


@pytest.fixture
def striped_orc_data():
    def _init(row):
        data = io.BytesIO()
        with Writer(
            data,
            "struct<col0:int>",
            batch_size=65535,
            stripe_size=128,
            compression_block_size=128,
        ) as writer:
            for i in range(row):
                writer.write((i,))
        data.seek(0)
        return data

    return _init


def test_init(orc_data):
    with pytest.raises(TypeError):
        _ = Reader(0)
    with pytest.raises(TypeError):
        _ = Reader(orc_data(1), "fail")
    reader = Reader(orc_data(2), 1)
    assert reader is not None


def test_open_file():
    with tempfile.NamedTemporaryFile(mode="wb") as fp:
        with pytest.raises(ParseError):
            _ = Reader(fp)
        fp.write(b"TESTTORC\x08\x03\x10\x03")
        fp.flush()
        fp.seek(0)
        with open(fp.name, "rb") as fp2:
            with pytest.raises(ParseError):
                _ = Reader(fp2)
        fp.write(b'ORC\x08\x03\x10\x03"k\x08\x0c\x12\x0c\x01\x02\x03')
        fp.flush()
        fp.seek(0)
        with open(fp.name, "rt") as fp2:
            with pytest.raises(ParseError):
                _ = Reader(fp2)
        with open(fp.name, "rb") as fp2:
            with pytest.raises(ParseError):
                _ = Reader(fp2)
        fp.seek(0)
        Writer(fp, "struct<col0:int,col1:string>").close()
        with open(fp.name, "ab") as fp2:
            with pytest.raises(io.UnsupportedOperation):
                _ = Reader(fp2)
        with open(fp.name, "rb") as fp2:
            reader = Reader(fp2)
            assert reader is not None
            assert len(reader) == 0


def test_next():
    data = io.BytesIO()
    Writer(data, "struct<col0:int,col1:string>").close()
    with pytest.raises(StopIteration):
        reader = Reader(data)
        next(reader)
    expected = (0, "Test A")
    data = io.BytesIO()
    with Writer(data, "struct<col0:int,col1:string>") as writer:
        writer.write(expected)
    reader = Reader(data)
    assert next(reader) == expected
    with pytest.raises(StopIteration):
        next(reader)


def test_iter(orc_data):
    reader = Reader(orc_data(20))
    result = [row for row in reader]
    assert len(result) == 20
    assert (0, "Test A") == result[0]
    assert (19, "Test T") == result[-1]
    assert (12, "Test M") in result


def test_len():
    data = io.BytesIO()
    Writer(data, "struct<col0:int,col1:string>").close()
    reader = Reader(data)
    assert len(reader) == 0

    data = io.BytesIO()
    with Writer(data, "struct<col0:int,col1:string>") as writer:
        writer.write((0, "Test A"))
    reader = Reader(data)
    assert len(reader) == 1

    data = io.BytesIO()
    with Writer(data, "struct<col0:int,col1:string>") as writer:
        for i in range(10):
            writer.write((i, "Test"))
    reader = Reader(data)
    assert len(reader) == 10


def test_schema():
    schema_str = "struct<col0:int,col1:string>"
    data = io.BytesIO()
    Writer(data, schema_str).close()
    reader = Reader(data)

    assert str(reader.schema) == schema_str
    with pytest.raises(AttributeError):
        reader.schema = "fail"
    with pytest.raises(AttributeError):
        del reader.schema

    schema = reader.schema
    del reader
    assert isinstance(schema, typedescription)
    assert schema.kind == TypeKind.STRUCT


def test_current_row(orc_data):
    reader = Reader(orc_data(20))
    assert reader.current_row == 0
    for _ in range(10):
        _ = next(reader)
    assert reader.current_row == 10
    res = next(reader)
    assert reader.current_row == 11
    assert res[0] == 10
    _ = [_ for _ in reader]
    assert reader.current_row == len(reader)

    with pytest.raises(AttributeError):
        reader.current_row = "fail"
    with pytest.raises(AttributeError):
        del reader.current_row


def test_seek(orc_data):
    reader = Reader(orc_data(50))
    assert reader.seek(0) == 0
    assert reader.current_row == 0
    assert reader.seek(10) == 10
    assert reader.current_row == 10
    assert next(reader)[0] == 10
    assert reader.seek(0, 2) == len(reader)
    with pytest.raises(StopIteration):
        _ = next(reader)[0]
    assert reader.seek(-1, 2) == 49
    assert next(reader)[0] == 49
    assert reader.seek(-10, 2) == 40
    assert reader.seek(1, 1) == 41
    assert next(reader)[0] == 41
    reader.seek(10)
    assert reader.seek(8, 1) == 18
    assert reader.seek(-5, 1) == 13
    assert next(reader)[0] == 13
    with pytest.raises(ValueError):
        reader.seek(-1, 0)
    with pytest.raises(ValueError):
        reader.seek(10, 10)


def test_read(orc_data):
    reader = Reader(orc_data(80))
    result = reader.read()
    assert len(result) == len(reader)
    assert (0, "Test A") == result[0]
    assert (25, "Test Z") == result[25]
    assert result[-1][0] == 79
    assert reader.current_row == 80
    with pytest.raises(StopIteration):
        _ = next(reader)
    result = reader.read()
    assert result == []

    reader = Reader(orc_data(80))
    with pytest.raises(ValueError):
        _ = reader.read(-5)
    with pytest.raises(TypeError):
        _ = reader.read("a")
    result = reader.read(10)
    assert len(result) == 10
    assert (0, "Test A") == result[0]
    assert (9, "Test J") == result[-1]

    result = reader.read(15)
    assert len(result) == 15
    assert (10, "Test K") == result[0]
    assert (24, "Test Y") == result[-1]
    assert reader.current_row == 25

    result = reader.read()
    assert len(result) == 55
    assert (25, "Test Z") == result[0]

    reader = Reader(orc_data(80))
    result = reader.read(0)
    assert result == []
    result = reader.read(-1)
    assert len(result) == len(reader)


def test_include():
    data = io.BytesIO()
    record = {"col0": 1, "col1": "Test A", "col2": 3.14}
    with Writer(
        data, "struct<col0:int,col1:string,col2:double>", struct_repr=StructRepr.DICT
    ) as writer:
        writer.write(record)
    data.seek(0)
    reader = Reader(data, column_indices=[0], struct_repr=StructRepr.DICT)
    assert next(reader) == {"col0": 1}
    reader = Reader(data, column_indices=[0, 2], struct_repr=StructRepr.DICT)
    assert next(reader) == {"col0": 1, "col2": 3.14}
    with pytest.raises(TypeError):
        _ = Reader(data, column_indices=[0, "2"], struct_repr=StructRepr.DICT)
    reader = Reader(data, column_names=["col0"], struct_repr=StructRepr.DICT)
    assert next(reader) == {"col0": 1}
    reader = Reader(data, column_names=["col1", "col2"], struct_repr=StructRepr.DICT)
    assert next(reader) == {"col1": "Test A", "col2": 3.14}
    with pytest.raises(TypeError):
        _ = Reader(data, column_names=["col1", 2], struct_repr=StructRepr.DICT)
    with pytest.raises(ValueError):
        _ = Reader(data, column_indices=[10], struct_repr=StructRepr.DICT)
    with pytest.raises(ValueError):
        _ = Reader(data, column_names=["col5"], struct_repr=StructRepr.DICT)
    with pytest.raises(ValueError):
        _ = Reader(
            data, column_names=["col1"], column_indices=[2], struct_repr=StructRepr.DICT
        )


def test_num_of_stripes(striped_orc_data):
    reader = Reader(striped_orc_data(655))
    assert reader.num_of_stripes == 1
    reader = Reader(striped_orc_data(655350))
    assert reader.num_of_stripes == 10


def test_read_stripe(striped_orc_data):
    reader = Reader(striped_orc_data(655350))
    stripe = reader.read_stripe(0)
    assert isinstance(stripe, Stripe)
    with pytest.raises(IndexError):
        _ = reader.read_stripe(11)
    with pytest.raises(TypeError):
        _ = reader.read_stripe(-1)
    with pytest.raises(IndexError):
        _ = reader.read_stripe(10)
    stripe = reader.read_stripe(9)
    assert isinstance(stripe, Stripe)


def test_iter_stripe(striped_orc_data):
    reader = Reader(striped_orc_data(655350))
    stripes = list(reader.iter_stripes())
    assert len(stripes) == reader.num_of_stripes
    assert all(isinstance(stripe, Stripe) for stripe in reader.iter_stripes())
