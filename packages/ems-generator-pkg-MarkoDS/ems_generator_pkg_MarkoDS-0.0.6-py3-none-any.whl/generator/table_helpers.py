from .structure import (address_one_fields, address_two_fields,
                        envelope_fields, vehicle_fields)


def table_structure(ems_type: str, claim: dict) -> dict:
    """
    Return a structure with field names and default falues for given ems_type.

    :param ems_type:  String, '.ad1', '.ad2', '.veh', '.env'
    :return: Dict with table structure if structure for received
             ems_type is defined. {'INS_CO_NM': 'ACD', 'INS_CTRY': 'USA' ...}
    """
    structures = {
        '.ad1': address_one_fields(claim),
        '.ad2': address_two_fields(claim),
        '.veh': vehicle_fields(claim),
        '.env': envelope_fields(claim)
    }

    try:
        return structures[ems_type]
    except KeyError:
        return 'Structure does not exists!'


def table_field_specs(structure: dict) -> list:
    """
    Return a list of field specifications for given structure.

    :param structure:  Dictionary, {'INS_ST C(1)': '', 'SUPP_NO C(10)': '' ...}
    :return: List of strings. Each string represent field specifiaction.
            ['INS_ST C(1)', 'SUPP_NO C(10)', ...]

    """
    return [key for key, value in structure.items()]


def table_default_values(structure: dict) -> list:
    """
    Return a list of default values for given structure.

    :param structure:  Dictionary, {'OWNR_FN': 'JOHN', 'OWNR_LN': 'DOE' ...}
    :return: List of strings. Each string represent a value.
            ['JOHN', 'DOE', ...]

    """
    return [value for key, value in structure.items()]


def table_name(ems_type: str, est_software: str, claim) -> str:
    """
    Return table name for given based on given est_software.

    Calls mitchell_table_name() or default_table_name().

    :param ems_type: String, '.ad1', '.ad2', '.veh', '.env'
    :param est_software: String, 'M', 'C', 'A'
    :param claim: Dictionary, {'CLAIM_NUMBER': 'TEST', 'OWNR_LN': 'DOE' ...}
    :return: mitchell_table_name() or default_table_name()
    """
    if est_software == 'M':
        name = mitchell_table_name(ems_type, claim)
    else:
        name = default_table_name(claim)

    return name + ems_type


def mitchell_table_name(ems_type: str, claim: dict) -> str:
    """
    Construct a table name for mitchell with given claim and ems_type.

    Adds 'a' or 'b' or 'v' to file names based on receivied ems_type.

    :param ems_type: String, '.ad1', '.ad2', '.veh', '.env'
    :param claim: Dictionary, {'CLAIM_NUMBER': 'TEST', 'OWNR_LN': 'DOE' ...}
    :return: claim['CLAIM_NUMBER'] + 'a' or 'b' or 'v' + ems_type, 'TEST.veh'
    """
    names = {
        '.ad1': claim['CLAIM_NUMBER'] + 'a',
        '.ad2': claim['CLAIM_NUMBER'] + 'b',
        '.veh': claim['CLAIM_NUMBER'] + 'v',
        '.env': claim['CLAIM_NUMBER']
    }

    return names[str(ems_type)]


def default_table_name(claim: dict) -> str:
    """
    Construct a default name for table with given claim and ems_type.

    :param ems_type: String, '.ad1', '.ad2', '.veh', '.env'
    :param claim: Dictionary, {'CLAIM_NUMBER': 'TEST', 'OWNR_LN': 'DOE' ...}
    :return: claim['CLAIM_NUMBER'] + ems_type, 'TEST.veh'
    """
    return claim['CLAIM_NUMBER']


def to_upper_dict(lower_dict: dict) -> dict:
    """Retrun received dictionary with a upper case keys and values.

    :param lower_dict: Dictionary, { 'key': 'value' }
    :return: upper_dict, { 'KEY': 'VALUE' }
    """
    upper_dict = {}

    for k, v in lower_dict.items():
        if isinstance(v, dict):
            v = to_upper_dict(v)
        v = v if not isinstance(v, str) else v.upper()
        upper_dict[k.upper()] = v

    return upper_dict


def zip_filename(claim, est_software):
    """Return name for zipfile."""
    number = claim['CLAIM_NUMBER']
    software_names = {
        'C': 'CCC',
        'M': 'Mitchell',
        'A': 'Audatex'
    }

    return number + '_ems_files_' + software_names[est_software] + '.zip'
