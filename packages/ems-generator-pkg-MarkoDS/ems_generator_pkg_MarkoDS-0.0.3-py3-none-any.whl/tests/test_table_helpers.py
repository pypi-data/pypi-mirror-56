import pytest

from generator.structure import (ADDRESS_1_FIELDS, ADDRESS_2_FIELDS,
                                 ENVIRONMENT_FIELDS, VEHICLE_FIELDS)
from generator.table_helpers import (default_table_name, mitchell_table_name,
                                     table_field_specs, table_structure)

from .test_data import (LEGACY_ADMINISTRATIVE_ONE_STRUCTURE,
                        LEGACY_ADMINISTRATIVE_TWO_STRUCTURE,
                        LEGACY_ENVELOPE_STRUCTURE, LEGACY_VEHICLE_STRUCTURE)


@pytest.mark.parametrize(
    "input, expected", [
        ('.ad1', ADDRESS_1_FIELDS),
        ('.ad2', ADDRESS_2_FIELDS),
        ('.veh', VEHICLE_FIELDS),
        ('.env', ENVIRONMENT_FIELDS)
    ]
)
def test_table_structure(input, expected):
    """Test if receivied structures are in sync with defined structures."""
    assert table_structure(input) == expected


@pytest.mark.parametrize(
    "input, expected", [
        ('.ad1', 'test_ems.ad1'),
        ('.ad2', 'test_ems.ad2'),
        ('.veh', 'test_ems.veh'),
        ('.env', 'test_ems.env')
    ]
)
def test_default_table_name(input, expected):
    """Test if default table name is in sync with ems standard."""
    assert default_table_name(
        input, claim={'CLAIM_NUMBER': 'test_ems'}
    ) == expected


@pytest.mark.parametrize(
    "input, expected", [
        ('.ad1', 'test_emsa.ad1'),
        ('.ad2', 'test_emsb.ad2'),
        ('.veh', 'test_emsv.veh'),
        ('.env', 'test_ems.env')
    ]
)
def test_mitchell_table_name(input, expected):
    """Test if mitchell table name is in sync with ems standard."""
    assert mitchell_table_name(
        input, claim={'CLAIM_NUMBER': 'test_ems'}
    ) == expected


@pytest.mark.parametrize(
    "input, expected", [
        (ADDRESS_1_FIELDS, LEGACY_ADMINISTRATIVE_ONE_STRUCTURE),
        (ADDRESS_2_FIELDS, LEGACY_ADMINISTRATIVE_TWO_STRUCTURE),
        (VEHICLE_FIELDS, LEGACY_VEHICLE_STRUCTURE),
        (ENVIRONMENT_FIELDS, LEGACY_ENVELOPE_STRUCTURE)
    ]
)
def test_table_field_specs(input, expected):
    """Test if received field specs are in sync with legacy field speds."""
    assert table_field_specs(input) == expected
