from validator import Validator

def test_validator_blocks_odd():
    v = Validator()
    valid, _ = v.validate({"result": 3})
    assert not valid

def test_validator_accepts_even():
    v = Validator()
    valid, _ = v.validate({"result": 4})
    assert valid