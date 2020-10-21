import logging
from typing import Iterator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_items(results: Iterator[dict]) -> Iterator[dict]:
    """
    Create items from results

    :param Iterator[dict] results: Query results from EUR-Lex webservice
    :return Iterator[dict] items: Items to insert into database
    """
    for result in results:
        item = {}
        item["title"] = None
        item["subtitle"] = None

        # Reference
        item["reference"] = result["reference"]

        content = result["content"]

        expression = get_item(content, "NOTICE", "EXPRESSION")

        # Title and subtitle
        item["title"] = get_item(expression, "EXPRESSION_TITLE", "VALUE")
        item["subtitle"] = get_item(expression, "EXPRESSION_SUBTITLE", "VALUE")

        work = get_item(content, "NOTICE", "WORK")

        item["id_celex"] = get_item(work, "ID_CELEX", "VALUE")

        item["date_end_of_validity"] = get_item(
            work, "RESOURCE_LEGAL_DATE_END-OF-VALIDITY", "VALUE"
        )
        item["date_last_modification"] = get_item(work, "LASTMODIFICATIONDATE", "VALUE")
        item["date_entry_into_force"] = get_item(
            work, "RESOURCE_LEGAL_DATE_ENTRY-INTO-FORCE", "VALUE"
        )

        item["date_document"] = get_date_document(work)

        item["eli"] = get_item(work, "RESOURCE_LEGAL_ELI", "VALUE")
        item["in_force"] = get_item(work, "RESOURCE_LEGAL_IN-FORCE", "VALUE")
        item["created_by"] = get_item(work, "WORK_CREATED_BY_AGENT", "PREFLABEL")
        item["resource_type"] = get_item(work, "WORK_HAS_RESOURCE-TYPE", "PREFLABEL")
        item["eurovoc_descriptors"] = get_euroc_descriptors(work)

        yield item


def get_item(item_dict: dict, key: str, value_key: str):
    if item_dict is None:
        return None

    if key in item_dict:
        value = item_dict[key]

        if isinstance(value, list):
            return [element[value_key] for element in value]
        elif isinstance(value, dict):
            return value[value_key] if value_key in value else None
        else:
            return value
    else:
        return None


def get_euroc_descriptors(work):
    return [
        item["WORK_IS_ABOUT_CONCEPT_EUROVOC_CONCEPT"]["PREFLABEL"]
        for item in work["WORK_IS_ABOUT_CONCEPT_EUROVOC"]
    ]


def get_date_document(work):
    if "WORK_DATE_DOCUMENT" in work:
        work_date_document = work["WORK_DATE_DOCUMENT"]

        # Does not have key VALUE, only DAY, MONTH, YEAR
        day = work_date_document["DAY"]
        month = work_date_document["MONTH"]
        year = work_date_document["YEAR"]

        return f"{year}-{month}-{day}"
