import sys
import os
import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pipeline.data_utils import clean_salary, hash_password, clean_gender, infer_dob


def test_clean_salary():
    assert clean_salary("£12,500.00") == 12500.0
    assert clean_salary(None) is None
    assert clean_salary("$10,000.00", period=12) == 120000.0


def test_hash_password():
    hashed = hash_password("test123")
    assert isinstance(hashed, str)
    assert len(hashed) == 64  # SHA-256 hash length


def test_clean_gender():
    mapping = {'M': 'Male', 'F': 'Female'}
    assert clean_gender('M', mapping) == 'Male'
    assert clean_gender('X', mapping) is None  # logs warning
    assert clean_gender(None, mapping) is None


def test_infer_dob():
    age = 25
    known_date = '01/01/99'
    dob = infer_dob(known_date, age)
    print(type(dob))
    assert isinstance(dob, datetime.date)

    fallback_date = '99-01-01'
    dob2 = infer_dob(fallback_date, age)
    assert isinstance(dob2, datetime.date)

    assert infer_dob("invalid", age) is None