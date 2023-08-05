import dbf


def envelope_fields(claim: dict):
    """T."""
    return {
        'EST_SYSTEM C(1)': '',
        'SW_VERSION C(10)': '',
        'DB_VERSION C(12)': '',
        'DB_DATE D': None,  # ?
        'UNQFILE_ID C(8)': str(claim['ID']),
        'RO_ID C(8)': '',
        'ESTFILE_ID C(38)': str(claim['ID']),
        'SUPP_NO C(3)': '',
        'EST_CTRY C(3)': '',
        'TOP_SECRET C(80)': '',
        'H_TRANS_ID C(9)': '',
        'H_CTRL_NO C(9)': '',
        'TRANS_TYPE C(1)': 'A',
        'STATUS L': None,  # ?
        'CREATE_DT D': dbf.Date(claim['DATE_TIME_CREATED'].date()),
        'CREATE_TM C(6)': '',  # str(claim['DATE_TIME_CREATED'].date()),
        'TRANSMT_DT D': None,  # ?
        'TRANSMT_TM C(6)': '',
        'INCL_ADMIN L': True,
        'INCL_VEH L': True,
        'INCL_EST L': False,
        'INCL_PROFL L': False,
        'INCL_TOTAL L': False,
        'INCL_VENDR L': False,
        'EMS_VER C(5)': '2.0'
    }
