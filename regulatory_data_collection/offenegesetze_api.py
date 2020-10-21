import logging
from itertools import product
from pprint import pformat

import click
import requests

from regulatory_data_collection.pipelines import MongoPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--api_root", default="https://api.offenegesetze.de/v1/veroeffentlichung")
@click.option(
    "--search_terms", "-s", default=("lebensmittel",), multiple=True, type=str
)
@click.option("--years", "-y", default=("2020",), multiple=True, type=str)
@click.option(
    "--type_of_acts", "-t", default=("bgbl1", "bgbl2"), multiple=True, type=str
)
@click.option(
    "--mongo_uri",
    default="mongodb+srv://dev-maml:x28sEnupWng04CsT@dev-complai-jbfiu.mongodb.net/"
    "test?retryWrites=true&w=majority",
    type=str,
)
@click.option("--mongo_database", default="data_collection_items", type=str)
@click.option("--mongo_collection", default="offenegesetze", type=str)
def main(**kwargs):
    logger.info(f"kwargs:\n{pformat(kwargs)}")

    for search_term, year, type_of_act in product(
        kwargs["search_terms"], kwargs["years"], kwargs["type_of_acts"]
    ):
        payload = {"q": search_term, "year": year, "kind": type_of_act}
        response = requests.get(kwargs["api_root"], params=payload)

        mongo_pipeline = MongoPipeline(
            kwargs["mongo_uri"], kwargs["mongo_database"], kwargs["mongo_collection"]
        )

        for result in response.json()["results"]:
            logger.info(pformat(result))

            mongo_pipeline.process_item(result, id_key="id")


if __name__ == "__main__":
    main()
