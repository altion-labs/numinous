import aiohttp

from neurons.validator.models.numinous_signals import SignalsResponse

DEFAULT_BASE_URL = "https://signals.numinouslabs.io"
DEFAULT_TIMEOUT = 120.0


class NuminousSignalsClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        if not api_key:
            raise ValueError("Numinous Signals API key is not set")
        self.__api_key = api_key
        self.__base_url = base_url
        self.__timeout = aiohttp.ClientTimeout(total=timeout)
        self.__headers = {
            "X-API-Key": self.__api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def compute_signals(
        self,
        market: str | None = None,
        question: str | None = None,
        relevance_threshold: float = 0.25,
        max_events_per_source: int = 25,
        time_window_hours: int = 72,
    ) -> SignalsResponse:
        body: dict = {
            "relevance_threshold": relevance_threshold,
            "max_events_per_source": max_events_per_source,
            "time_window_hours": time_window_hours,
        }
        if market is not None:
            body["market"] = market
        if question is not None:
            body["question"] = question

        url = f"{self.__base_url}/api/v1/signals"
        async with aiohttp.ClientSession(timeout=self.__timeout, headers=self.__headers) as session:
            async with session.post(url, json=body) as response:
                response.raise_for_status()
                data = await response.json()
                return SignalsResponse.model_validate(data)
