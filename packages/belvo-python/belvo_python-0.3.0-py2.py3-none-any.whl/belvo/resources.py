from datetime import date
from typing import Dict, Generator, List, Union

from belvo.http import JWTSession


class Resource:
    endpoint: str

    def __init__(self, session: JWTSession) -> None:
        self._session = session

    @property
    def session(self) -> JWTSession:
        return self._session

    def list(self, **kwargs) -> Generator:
        endpoint = self.endpoint
        return self.session.list(endpoint, params=kwargs)

    def get(self, id: str, **kwargs) -> Dict:
        return self.session.get(self.endpoint, id, params=kwargs)

    def delete(self, id: str) -> bool:
        return self.session.delete(self.endpoint, id)

    def resume(
        self, session: str, token: str, *, link: str = None, **kwargs
    ) -> Union[List[Dict], Dict]:

        data = {"session": session, "token": token}

        if link is not None:
            data.update(link=link)

        return self.session.patch(self.endpoint, data=data, **kwargs)


class Links(Resource):
    endpoint = "/api/links/"

    def create(
        self,
        institution: str,
        username: str,
        password: str,
        *,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
    ) -> Union[List[Dict], Dict]:

        data = {
            "institution": institution,
            "username": username,
            "password": password,
            "save_data": save_data,
        }

        if token:
            data.update(token=token)

        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(self.endpoint, data=data)


class Accounts(Resource):
    endpoint = "/api/accounts/"

    def create(
        self,
        link: str,
        *,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
        **kwargs: str,
    ) -> Union[List[Dict], Dict]:

        data = {"link": link, "save_data": save_data}

        if token:
            data.update(token=token)
        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(self.endpoint, data=data, **kwargs)


class Transactions(Resource):
    endpoint = "/api/transactions/"

    def create(
        self,
        link: str,
        date_from: str,
        *,
        date_to: str = None,
        account: str = None,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
        **kwargs: str,
    ) -> Union[List[Dict], Dict]:

        if date_to is None:
            date_to = date.today().isoformat()

        data = {"link": link, "date_from": date_from, "date_to": date_to, "save_data": save_data}

        if account:
            data.update(account=account)
        if token:
            data.update(token=token)
        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(self.endpoint, data=data, **kwargs)


class Institutions(Resource):
    endpoint = "/api/institutions/"

    def delete(self, id: str) -> bool:
        raise NotImplementedError()

    def resume(self, session: str, token: str, *, link: str = None, **kwargs: str) -> Dict:
        raise NotImplementedError()


class Owners(Resource):
    endpoint = "/api/owners/"

    def create(
        self,
        link: str,
        *,
        token: str = None,
        encryption_key: str = None,
        save_data: bool = True,
        **kwargs: str,
    ) -> Union[List[Dict], Dict]:

        data = {"link": link, "save_data": save_data}

        if token:
            data.update(token=token)
        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(self.endpoint, data=data, **kwargs)


class Invoices(Resource):
    endpoint = "/api/invoices/"

    def create(
        self,
        link: str,
        date_from: str,
        date_to: str,
        type_: str,
        *,
        encryption_key: str = None,
        save_data: bool = True,
        **kwargs: str,
    ) -> Union[List[Dict], Dict]:

        data = {
            "link": link,
            "date_from": date_from,
            "date_to": date_to,
            "type": type_,
            "save_data": save_data,
        }

        if encryption_key:
            data.update(encryption_key=encryption_key)

        return self.session.post(self.endpoint, data=data, **kwargs)

    def get(self, id: str, **kwargs) -> Dict:
        raise NotImplementedError()

    def resume(self, session: str, token: str, *, link: str = None, **kwargs: str) -> Dict:
        raise NotImplementedError()
