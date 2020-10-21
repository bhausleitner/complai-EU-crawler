import logging
from typing import Iterator
from typing import List
from typing import Tuple

import xmltodict
from zeep import CachingClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_search_results_stats(search_results: dict) -> Tuple[int, int, int]:
    """
    Get stats from search results

    :param search_results:
    :return Tuple[int, int, int] stats: hits, total hits, page
    """
    num_hits: int = int(search_results["numhits"])
    total_hits: int = int(search_results["totalhits"])
    page: int = int(search_results["page"])

    logger.info(f"Got {num_hits} hits of {total_hits} total hits from page {page}")

    return num_hits, page, total_hits


def get_search_results(client: CachingClient, query_dict: dict) -> dict:
    """
    Get search results from EUR-Lex webservice from one page.

    :param CachingClient client: Client to query
    :param dict query_dict: Query for client
    :return dict search_results: Search results from EUR-Lex webservice from one page
    """
    # TODO: store raw response
    # Get raw XML response and decode it as a string
    response_raw: str = client.service.doQuery(**query_dict).content.decode("utf-8")

    # Convert XML response to dict
    response_dict: dict = xmltodict.parse(response_raw)

    # Get search results
    search_results: dict = response_dict["S:Envelope"]["S:Body"]["searchResults"]

    return search_results


def get_search_results_aggregated(
    client: CachingClient, query_dict: dict
) -> List[dict]:
    """
    Return list of search results.

    Each element of the list contains the search results from one page as the
    EUR-Lex webservice returns its results paginated.

    :param CachingClient client: Client to query
    :param dict query_dict: Query for client
    :return List[dict] search_results_aggregated: List of search results from
    EUR-Lex webservice
    """
    # Get search results from query
    search_results: dict = get_search_results(client, query_dict)
    num_hits, page, total_hits = get_search_results_stats(search_results)

    search_results_aggregated = [search_results]
    num_hits_aggregated = num_hits

    # There can be more hits on the next page
    while num_hits_aggregated < total_hits:
        # Go to next page
        query_dict["page"]: str = str(page + 1)

        # Get search results from query
        search_results = get_search_results(client, query_dict)
        num_hits, page, total_hits = get_search_results_stats(search_results)

        # Aggregate search results and num hits
        search_results_aggregated.append(search_results)
        num_hits_aggregated += int(num_hits)

    return search_results_aggregated


def get_results(client: CachingClient, query_dict: dict) -> Iterator[dict]:
    """
    Yield results from queried client.

    :param CachingClient client: Client to query
    :param dict query_dict: Query for client
    :return Iterator[dict] results: Query results
    """
    # Get list of search results
    search_results_aggregated: List[dict] = get_search_results_aggregated(
        client, query_dict
    )

    # Iterate over search results list
    for search_results in search_results_aggregated:
        if isinstance(search_results["result"], list):
            results: List[dict] = search_results["result"]
            for result in results:
                yield result
        else:
            result = search_results["result"]
            yield result
