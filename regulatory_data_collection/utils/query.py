import logging
from pprint import pformat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_code_string(codes: set, base_string: str) -> str:
    """
    Create query from codes.

    :param set codes: Codes to create query for
    :param str base_string: Base string for query
    :return:
    """
    code_string: str = f"{base_string} = {codes[0]}"
    if len(codes) >= 1:
        for code in codes[1:]:
            code_string += f" OR {code}"

    logger.debug(f"code_string: {code_string}")
    return code_string


def create_query_dict(
    euro_voc_descriptor_codes: set, years: set, type_of_act_codes: set
) -> dict:
    """
    Create query for EUR-Lex webservice.

    :param set euro_voc_descriptor_codes: Codes for EuroVoc descriptors
    :param set years: Years for results
    :param set type_of_act_codes: Codes for type of acts
    :return dict query_dict: Query for  EUR-Lex webservice
    """
    # Create query strings for years, type of acts, and EuroVoc descriptors
    dc_code_string: str = create_code_string(euro_voc_descriptor_codes, "DC_TT_CODED")
    dta_code_string: str = create_code_string(years, "DTA")
    fm_code_string: str = create_code_string(type_of_act_codes, "FM_CODED")

    # Create query dict
    expert_query: str = (
        "DTS_SUBDOM = LEGISLATION AND "
        f"{dta_code_string} AND "
        f"{fm_code_string} AND "
        f"{dc_code_string}"
    )
    query_dict: dict = {
        "expertQuery": expert_query,
        "page": 1,
        "pageSize": 10,
        "searchLanguage": "de",
    }

    logger.info(f"query_dict: {pformat(query_dict)}")

    return query_dict
