import pytest

from generator.structure import (address_one_fields, address_two_fields,
                                 envelope_fields, vehicle_fields)
from generator.table_helpers import (default_table_name, mitchell_table_name,
                                     table_field_specs, table_structure,
                                     to_upper_dict)

from .test_data import (CLAIM, LEGACY_ADMINISTRATIVE_ONE_STRUCTURE,
                        LEGACY_ADMINISTRATIVE_TWO_STRUCTURE,
                        LEGACY_ENVELOPE_STRUCTURE, LEGACY_VEHICLE_STRUCTURE)


CLAIM = to_upper_dict(CLAIM)


@pytest.mark.parametrize(
    "input, expected", [
        ('.ad1', address_one_fields(CLAIM)),
        ('.ad2', address_two_fields(CLAIM)),
        ('.veh', vehicle_fields(CLAIM)),
        ('.env', envelope_fields(CLAIM))
    ]
)
def test_table_structure(input, expected):
    """Test if receivied structures are in sync with defined structures."""
    assert table_structure(input, CLAIM) == expected


def test_default_table_name():
    """Test if default table name is in sync with ems standard."""
    assert default_table_name(CLAIM) == CLAIM['CLAIM_NUMBER']


@pytest.mark.parametrize(
    "input, expected", [
        ('.ad1', CLAIM['CLAIM_NUMBER'] + 'a'),
        ('.ad2', CLAIM['CLAIM_NUMBER'] + 'b'),
        ('.veh', CLAIM['CLAIM_NUMBER'] + 'v'),
        ('.env', CLAIM['CLAIM_NUMBER'])
    ]
)
def test_mitchell_table_name(input, expected):
    """Test if mitchell table name is in sync with ems standard."""
    assert mitchell_table_name(
        input, CLAIM
    ) == expected


@pytest.mark.parametrize(
    "input, expected", [
        (address_one_fields(CLAIM), LEGACY_ADMINISTRATIVE_ONE_STRUCTURE),
        (address_two_fields(CLAIM), LEGACY_ADMINISTRATIVE_TWO_STRUCTURE),
        (vehicle_fields(CLAIM), LEGACY_VEHICLE_STRUCTURE),
        (envelope_fields(CLAIM), LEGACY_ENVELOPE_STRUCTURE)
    ]
)
def test_table_field_specs(input, expected):
    """Test if received field specs are in sync with legacy field speds."""
    assert table_field_specs(input) == expected
