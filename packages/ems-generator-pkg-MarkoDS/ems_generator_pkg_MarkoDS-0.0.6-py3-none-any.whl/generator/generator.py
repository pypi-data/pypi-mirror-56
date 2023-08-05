import zipfile
import glob
import os
import dbf

from .table_helpers import (table_default_values, table_field_specs,
                            table_name, table_structure, to_upper_dict,
                            zip_filename)


EMS_TYPES = ['.ad1', '.ad2', '.veh', '.env']


def generate_ems(est_software: str, claim: dict):
    """Doc String missing."""
    claim = to_upper_dict(claim)
    filename = zip_filename(claim, est_software)

    with zipfile.ZipFile(filename, 'w') as zip:
        for ems_type in EMS_TYPES:
            file = generate_file(
                ems_type=ems_type,
                structure=table_structure(ems_type, claim),
                est_software=est_software,
                claim=claim
            )
            for f in glob.glob("{}".format(file.filename)):
                zip.write(f)
                os.remove(f)
    
    zip.close()
    return zip


def dbf_table(ems_type: str, structure: str, est_software: str, claim: dict):
    """Doc String missing."""
    file_name = table_name(ems_type, est_software, claim)
    return dbf.Table(
        file_name,
        field_specs=table_field_specs(structure)
    )


def generate_file(ems_type, structure, est_software, claim):
    """Doc string missing."""
    table = dbf_table(ems_type, structure, est_software, claim)
    add_data(table, structure)
    table.close()

    return table


def add_data(table, structure):
    """Test func for populating dummy data."""
    table.open(mode=dbf.READ_WRITE)
    table.append(tuple(table_default_values(structure)))
