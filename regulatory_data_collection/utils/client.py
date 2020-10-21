import logging

from zeep import CachingClient
from zeep import Settings
from zeep.wsse import UsernameToken

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_client(wsdl: str, raw_response: bool = True) -> CachingClient:
    """
    Creates Zeep client that caches the WSDL.

    :param str wsdl: Link to the WSDL
    :param bool raw_response: Whether the client should return the raw XML response
    :return CachingClient client: Zeep client
    """
    # We want the raw response as there is an error when Zeep parses the XML
    settings: Settings = Settings(raw_response=raw_response)

    # Client that caches the WSDL
    client: CachingClient = CachingClient(
        wsdl=wsdl,
        # TODO: Store PW encrypted
        wsse=UsernameToken("n00394gz", "g427Ix19LMB"),
        settings=settings,
    )
    logger.debug(f"Client created")

    return client
