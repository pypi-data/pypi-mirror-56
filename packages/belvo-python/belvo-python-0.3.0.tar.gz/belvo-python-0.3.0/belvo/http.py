import logging
from typing import Dict, Generator, List, Union

from requests import HTTPError, Session

from belvo import __version__

logger = logging.getLogger(__name__)


class JWTSession:
    _secret_key_id: str
    _secret_key_password: str
    _access_token: str
    _refresh_token: str
    _url: str

    def __init__(self, url: str) -> None:
        self._url = url
        self._session = Session()
        self._session.headers.update({"User-Agent": f"belvo-python ({__version__})"})

    @property
    def url(self) -> Union[str, None]:
        return self._url

    @property
    def key_id(self) -> Union[str, None]:
        return self._secret_key_id

    @property
    def session(self) -> Session:
        return self._session

    @property
    def headers(self) -> Dict:
        return self.session.headers  # type: ignore

    @property
    def access_token(self) -> Union[str, None]:
        return self._access_token

    @property
    def refresh_token(self) -> Union[str, None]:
        return self._refresh_token

    def set_tokens(self, access: str, refresh: str) -> None:
        self._access_token = access
        self._refresh_token = refresh

    def login(self, secret_key_id: str, secret_key_password: str, timeout: int = 5) -> bool:
        auth_url = "{}/api/token/".format(self.url)
        r = self.session.post(
            auth_url, data={"id": secret_key_id, "password": secret_key_password}, timeout=timeout
        )
        try:
            r.raise_for_status()
        except HTTPError:
            return False
        tokens = r.json()
        self.set_tokens(**tokens)
        self.session.headers.update({"Authorization": "Bearer {}".format(self.access_token)})
        return True

    def _get(self, url: str, params: Dict = None, timeout: int = 5) -> Dict:
        if params is None:
            params = {}

        r = self.session.get(url=url, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()

    def get(self, endpoint: str, id: str, params: Dict = None) -> Dict:
        url = "{}{}{}/".format(self.url, endpoint, id)
        return self._get(url=url, params=params)

    def list(self, endpoint: str, params: Dict = None) -> Generator:
        url = "{}{}".format(self.url, endpoint)
        while True:
            data = self._get(url, params=params)
            for result in data["results"]:
                yield result

            if not data["next"]:
                break

            url = data["next"]
            params = None

    def post(self, endpoint: str, data: Dict, *args, **kwargs) -> Union[List, Dict]:
        url = "{}{}".format(self.url, endpoint)
        r = self.session.post(url, data=data, **kwargs)
        return r.json()

    def patch(self, endpoint: str, data: Dict, **kwargs) -> Union[List[Dict], Dict]:
        url = "{}{}".format(self.url, endpoint)
        r = self.session.patch(url=url, data=data, **kwargs)
        return r.json()

    def delete(self, endpoint: str, id: str, timeout: int = 5) -> bool:
        url = "{}{}{}/".format(self.url, endpoint, id)
        r = self.session.delete(url, timeout=timeout)
        try:
            r.raise_for_status()
        except HTTPError:
            return False
        return True
