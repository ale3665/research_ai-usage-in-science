from requests import Response, get


class Search:
    def __init__(
        self,
        headers: dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",  # noqa: E501,
        },
    ) -> None:
        """
        __init__ _summary_

        _extended_summary_

        :param headers: _description_, defaults to { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",  # noqa: E501, }
        :type headers: _type_, optional
        """
        self.headers: dict[str, str] = headers

    def search(self, url: str) -> Response:
        """
        search _summary_

        _extended_summary_

        :param url: _description_
        :type url: str
        :return: _description_
        :rtype: Response
        """
        resp: Response = get(url=url, headers=self.headers, timeout=60)
        return resp
