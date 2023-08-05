import re
import dbf


def loss_cat_map(loss_cat):
    """Doc string gmissing."""
    loss_categories = {
        'COLL': 'C',
        'COMP': 'M',
        'PD': 'P',
        'UNKNOWN': 'U'
    }

    return loss_categories[loss_cat]


def insured_info(claim):
    """Doc string gmissing."""
    last_name = 'UNK'
    first_name = 'UNK'

    if claim['INSURED_FIRST_NAME'] != '':
        first_name = claim['INSURED_FIRST_NAME']
    else:
        first_name = claim['OWNER_FIRST_NAME']

    if claim['INSURED_LAST_NAME'] != '':
        last_name = claim['INSURED_LAST_NAME']
    else:
        last_name = claim['OWNER_LAST_NAME']

    return [last_name, first_name]


def clean_phone_format(number):
    """Doc string gmissing."""
    if len(number) > 0:
        return re.sub('[^0-9]', '', number)

    return None


def address_one_fields(claim: dict):
    """Doc string gmissing."""
    insured = claim['OWNER_INSURED_OR_CLAIMANT'] == 'INSURED'

    return {
        'INS_CO_ID C(5)': '',
        'INS_CO_NM C(35)': 'ACD',
        'INS_ADDR1 C(40)': '',
        'INS_ADDR2 C(40)': '',
        'INS_CITY C(30)': '',
        'INS_ST C(2)': '',
        'INS_ZIP C(11)': '',
        'INS_CTRY C(3)': 'USA',
        'INS_PH1 C(10)': '',
        'INS_PH1X C(8)': '',
        'INS_PH2 C(10)': '',
        'INS_PH2X C(8)': '',
        'INS_FAX C(10)': '',
        'INS_FAXX C(8)': '',
        'INS_CT_LN C(35)': '',
        'INS_CT_FN C(35)': '',
        'INS_TITLE C(35)': '',
        'INS_CT_PH C(10)': '',
        'INS_CT_PHX C(8)': '',
        'INS_EA C(80)': '',
        'INS_MEMO C(10)': '',
        'POLICY_NO C(30)': '',
        'DED_AMT N(9,2)': claim['DEDUCTIBLE'],
        'DED_STATUS C(2)': '',
        'ASGN_NO C(25)': '',
        'ASGN_DATE D': dbf.Date(claim['DATE_TIME_CREATED']),
        'ASGN_TYPE C(1)': '',
        'CLM_NO C(30)': claim['CLAIM_NUMBER'],
        'CLM_OFC_ID C(5)': '',
        'CLM_OFC_NM C(35)': '',
        'CLM_ADDR1 C(40)': '',
        'CLM_ADDR2 C(40)': '',
        'CLM_CITY C(30)': '',
        'CLM_ST C(2)': '',
        'CLM_ZIP C(11)': '',
        'CLM_CTRY C(3)': '',
        'CLM_PH1 C(10)': '',
        'CLM_PH1X C(8)': '',
        'CLM_PH2 C(10)': '',
        'CLM_PH2X C(8)': '',
        'CLM_FAX C(10)': '',
        'CLM_FAXX C(8)': '',
        'CLM_CT_LN C(35)': '',
        'CLM_CT_FN C(35)': '',
        'CLM_TITLE C(35)': '',
        'CLM_CT_PH C(10)': '',
        'CLM_CT_PHX C(8)': '',
        'CLM_EA C(80)': '',
        'PAYEE_NMS C(85)': '',
        'PAY_TYPE C(2)': '',
        'PAY_DATE D': None,  # ?
        'PAY_CHKNM C(16)': '',
        'PAY_AMT N(10,2)': None,  # ?
        'PAY_MEMO C(10)': '',
        'AGT_CO_ID C(5)': '',
        'AGT_CO_NM C(35)': '',
        'AGT_ADDR1 C(40)': '',
        'AGT_ADDR2 C(40)': '',
        'AGT_CITY C(30)': '',
        'AGT_ST C(2)': '',
        'AGT_ZIP C(11)': '',
        'AGT_CTRY C(3)': '',
        'AGT_PH1 C(10)': '',
        'AGT_PH1X C(8)': '',
        'AGT_PH2 C(10)': '',
        'AGT_PH2X C(8)': '',
        'AGT_FAX C(10)': '',
        'AGT_FAXX C(8)': '',
        'AGT_CT_LN C(35)': '',
        'AGT_CT_FN C(35)': '',
        'AGT_CT_PH C(10)': '',
        'AGT_CT_PHX C(8)': '',
        'AGT_EA C(80)': '',
        'AGT_LIC_NO C(30)': '',
        'LOSS_DATE D': dbf.Date(claim['DATE_OF_LOSS']),
        'LOSS_CAT C(1)': loss_cat_map(claim['COVERAGE_TYPE']),
        'LOSS_TYPE C(7)': '',
        'LOSS_DESC C(38)': '',
        'THEFT_IND L': None,
        'CAT_NO C(30)': '',
        'TLOS_IND L': None,
        'LOSS_MEMO C(10)': '',
        'CUST_PR C(1)': claim['OWNER_INSURED_OR_CLAIMANT'][0],
        'INSD_LN C(35)': insured_info(claim)[0],
        'INSD_FN C(35)': insured_info(claim)[1],
        'INSD_TITLE C(2)': '',
        'INSD_CO_NM C(35)': '',
        'INSD_ADDR1 C(40)': claim['OWNER_ADDRESS_LINE1'] if insured else None,
        'INSD_ADDR2 C(40)': claim['OWNER_ADDRESS_LINE2'] if insured else None,
        'INSD_CITY C(30)': claim['OWNER_ADDRESS_CITY'] if insured else None,
        'INSD_ST C(2)': claim['OWNER_ADDRESS_STATE'] if insured else None,
        'INSD_ZIP C(11)': claim['OWNER_ADDRESS_ZIP'] if insured else None,
        'INSD_CTRY C(3)': '',
        'INSD_PH1 C(10)': '',
        'INSD_PH1X C(8)': '',
        'INSD_PH2 C(10)': '',
        'INSD_PH2X C(8)': '',
        'INSD_FAX C(10)': '',
        'INSD_FAXX C(8)': '',
        'INSD_EA C(80)': '',
        'OWNR_LN C(35)': claim['OWNER_LAST_NAME'],
        'OWNR_FN C(35)': claim['OWNER_FIRST_NAME'],
        'OWNR_TITLE C(2)': '',
        'OWNR_CO_NM C(35)': claim['OWNER_COMPANY'],
        'OWNR_ADDR1 C(40)': claim['OWNER_ADDRESS_LINE1'],
        'OWNR_ADDR2 C(40)': claim['OWNER_ADDRESS_LINE2'],
        'OWNR_CITY C(30)': claim['OWNER_ADDRESS_CITY'],
        'OWNR_ST C(2)': claim['OWNER_ADDRESS_STATE'],
        'OWNR_ZIP C(11)': claim['OWNER_ADDRESS_ZIP'],
        'OWNR_CTRY C(3)': '',
        'OWNR_PH1 C(10)': claim['OWNER_PHONE_MOBILE'],  # ?
        'OWNR_PH1X C(8)': '',
        'OWNR_PH2 C(10)': claim['OWNER_PHONE_WORK'],  # ?
        'OWNR_PH2X C(8)': '',
        'OWNR_FAX C(10)': '',  # ?
        'OWNR_FAXX C(8)': '',
        'OWNR_EA C(80)': '',
    }


def address_two_fields(claim: dict):
    """T."""
    cliamant = claim['OWNER_INSURED_OR_CLAIMANT'] == 'CLAIMANT'

    return {  # should only be populated if owner  type is claimant
        'CLMT_LN C(35)': claim['OWNER_LAST_NAME'] if cliamant else None,
        'CLMT_FN C(35)': claim['OWNER_FIRST_NAME'] if cliamant else None,
        'CLMT_TITLE C(2)': '',
        'CLMT_CO_NM C(35)': '',
        'CLMT_ADDR1 C(40)': claim['OWNER_ADDRESS_LINE1'] if cliamant else None,
        'CLMT_ADDR2 C(40)': claim['OWNER_ADDRESS_LINE2'] if cliamant else None,
        'CLMT_CITY C(30)': claim['OWNER_ADDRESS_CITY'] if cliamant else None,
        'CLMT_ST C(2)': claim['OWNER_ADDRESS_STATE'] if cliamant else None,
        'CLMT_ZIP C(11)': claim['OWNER_ADDRESS_ZIP'] if cliamant else None,
        'CLMT_CTRY C(3)': '',
        'CLMT_PH1 C(10)': claim['OWNER_PHONE_MOBILE'] if cliamant else None,
        'CLMT_PH1X C(8)': '',
        'CLMT_PH2 C(10)': claim['OWNER_PHONE_WORK'] if cliamant else None,
        'CLMT_PH2X C(8)': '',
        'CLMT_FAX C(10)': '',
        'CLMT_FAXX C(8)': '',
        'CLMT_EA C(80)': '',
        'EST_CO_ID C(5)': '',
        'EST_CO_NM C(35)': 'AUTOCLAIMS DIRECT',
        'EST_ADDR1 C(40)': '',
        'EST_ADDR2 C(40)': '',
        'EST_CITY C(30)': '',
        'EST_ST C(2)': '',
        'EST_ZIP C(11)': '',
        'EST_CTRY C(3)': '',
        'EST_PH1 C(10)': '',
        'EST_PH1X C(8)': '',
        'EST_PH2 C(10)': '',
        'EST_PH2X C(8)': '',
        'EST_FAX C(10)': '',
        'EST_FAXX C(8)': '',
        'EST_CT_LN C(35)': '',
        'EST_CT_FN C(35)': '',
        'EST_EA C(80)': '',
        'EST_LIC_NO C(30)': '',
        'EST_FILENO C(25)': '',
        'INSP_CT_LN C(35)': '',
        'INSP_CT_FN C(35)': '',
        'INSP_ADDR1 C(40)': '',
        'INSP_ADDR2 C(40)': '',
        'INSP_CITY C(30)': '',
        'INSP_ST C(2)': '',
        'INSP_ZIP C(11)': '',
        'INSP_CTRY C(3)': '',
        'INSP_PH1 C(10)': '',
        'INSP_PH1X C(8)': '',
        'INSP_PH2 C(10)': '',
        'INSP_PH2X C(8)': '',
        'INSP_FAX C(10)': '',
        'INSP_FAXX C(8)': '',
        'INSP_EA C(80)': '',
        'INSP_CODE C(4)': '',
        'INSP_DESC C(40)': '',
        'INSP_DATE D': None,  # ?
        'INSP_TIME C(4)': '',
        'RF_CO_ID C(5)': '',
        'RF_CO_NM C(35)': '',
        'RF_ADDR1 C(40)': '',
        'RF_ADDR2 C(40)': '',
        'RF_CITY C(30)': '',
        'RF_ST C(2)': '',
        'RF_ZIP C(11)': '',
        'RF_CTRY C(3)': '',
        'RF_PH1 C(10)': '',
        'RF_PH1X C(8)': '',
        'RF_PH2 C(10)': '',
        'RF_PH2X C(8)': '',
        'RF_FAX C(10)': '',
        'RF_FAXX C(8)': '',
        'RF_CT_LN C(35)': '',
        'RF_CT_FN C(35)': '',
        'RF_EA C(80)': '',
        'RF_TAX_ID C(30)': '',
        'RF_LIC_NO C(30)': '',
        'RF_BAR_NO C(30)': '',
        'RO_IN_DATE D': None,  # ?
        'RO_IN_TIME C(4)': '',
        'RO_AUTH C(10)': '',
        'TAR_DATE D': None,  # ?
        'TAR_TIME C(4)': '',
        'RO_CMPDATE D': None,  # ?
        'RO_CMPTIME C(4)': '',
        'DATE_OUT D': None,  # ?
        'TIME_OUT C(4)': '',
        'RF_ESTIMTR C(35)': '',
        'MKTG_TYPE C(2)': '',
        'MKTG_SRC C(35)': '',
        'LOC_NM C(35)': claim['VEHICLE_LOCATION_NAME'],
        'LOC_ADDR1 C(40)': claim['VEHICLE_ADDRESS_LINE1'],
        'LOC_ADDR2 C(40)': claim['VEHICLE_ADDRESS_LINE2'],
        'LOC_CITY C(30)': claim['VEHICLE_ADDRESS_CITY'],
        'LOC_ST C(2)': claim['VEHICLE_ADDRESS_STATE'],
        'LOC_ZIP C(11)': claim['VEHICLE_ADDRESS_ZIP'],
        'LOC_CTRY C(3)': '',
        'LOC_PH1 C(10)': '',
        'LOC_PH1X C(8)': '',
        'LOC_PH2 C(10)': '',
        'LOC_PH2X C(8)': '',
        'LOC_FAX C(10)': '',
        'LOC_FAXX C(8)': '',
        'LOC_CT_LN C(35)': '',
        'LOC_CT_FN C(35)': '',
        'LOC_TITLE C(35)': '',
        'LOC_PH C(10)': '',
        'LOC_PHX C(8)': '',
        'LOC_EA C(80)': ''
    }
