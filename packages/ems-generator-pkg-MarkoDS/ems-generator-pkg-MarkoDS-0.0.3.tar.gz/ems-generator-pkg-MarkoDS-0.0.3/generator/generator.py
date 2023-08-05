import dbf

from .table_helpers import (table_default_values, table_field_specs,
                            table_name, table_structure)

EMS_TYPES = ['.ad1', '.ad2', '.veh', '.env']


def generate_ems(est_software: str, claim: dict):
    """Doc String missing."""
    for ems_type in EMS_TYPES:
        generate_file(
            ems_type=ems_type,
            structure=table_structure(ems_type, claim),
            est_software=est_software,
            claim=claim
        )


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


# def test():
#     ad1_new = dbf.Table('test.ad1')
#     ad1_old = dbf.Table('7784374a.ad1')
#     print(ad1_new.field_count, ad1_old.field_count)

#     ad2_new = dbf.Table('test.ad2')
#     ad2_old = dbf.Table('7784374b.ad2')
#     print(ad2_new.field_count, ad2_old.field_count)

#     veh_new = dbf.Table('test.veh')
#     veh_old = dbf.Table('7784374v.veh')
#     print(veh_old.field_count, veh_new.field_count)

#     env_new = dbf.Table('test.env')
#     env_old = dbf.Table('7784374.env')
#     print(env_new.field_count, env_old.field_count)
