import logging
from pprint import pformat
from typing import Iterator

import click
from zeep import CachingClient

from regulatory_data_collection.pipelines import MongoPipeline
from regulatory_data_collection.utils.client import create_client
from regulatory_data_collection.utils.item import get_items
from regulatory_data_collection.utils.query import create_query_dict
from regulatory_data_collection.utils.result import get_results

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--wsdl", default="https://eur-lex.europa.eu/eurlex-ws?wsdl", show_default=True
)
@click.option(
    "--euro_voc_descriptor_codes",
    "-e",
    default=("2735", "1258", "2736"),
    multiple=True,
    type=str,
)
@click.option("--years", "-y", default=("2020",), multiple=True, type=str)
@click.option(
    "--type_of_act_codes", "-t", default=("DEC", "REG", "DIR"), multiple=True, type=str
)
@click.option(
    "--mongo_uri",
    default="mongodb+srv://dev-maml:x28sEnupWng04CsT@dev-complai-jbfiu.mongodb.net/"
    "test?retryWrites=true&w=majority",
    type=str,
)
@click.option("--mongo_database", default="data_collection_items", type=str)
@click.option("--mongo_collection", default="eur_lex", type=str)
def main(**kwargs):
    logger.info(f"kwargs:\n{pformat(kwargs)}")

    client: CachingClient = create_client(kwargs["wsdl"])

    query_dict: dict = create_query_dict(
        kwargs["euro_voc_descriptor_codes"],
        kwargs["years"],
        kwargs["type_of_act_codes"],
    )

    results: Iterator = get_results(client, query_dict)

    items: Iterator = get_items(results)

    mongo_pipeline = MongoPipeline(
        kwargs["mongo_uri"], kwargs["mongo_database"], kwargs["mongo_collection"]
    )

    for idx, item in enumerate(items):
        logger.info(f"{idx}:\n{pformat(item)}")

        mongo_pipeline.process_item(item, id_key="id_celex")


if __name__ == "__main__":
    main()
