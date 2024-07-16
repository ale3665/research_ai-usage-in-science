from requests import Response, get


class Search:
    def __init__(
        self,
        headers: dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",  # noqa: E501,
        },
    ) -> None:
        self.headers: dict[str, str] = headers

    def search(self, url: str) -> Response:
        resp: Response = get(url=url, headers=self.headers, timeout=60)
        return resp
