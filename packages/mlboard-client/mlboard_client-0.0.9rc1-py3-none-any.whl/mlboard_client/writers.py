import typing as t
import requests
from requests import Response
from uuid import UUID
from urllib.parse import urljoin
from datetime import datetime
from json import dumps

from logging import Logger
from .encoders import CustomJSONEncoder


class Writer:
    def __init__(
        self, url: str,
        workspace_name: str,
        params: t.Dict[str, t.Any] = {},
        logger: t.Optional[Logger] = None,
    ) -> None:
        self.url = url
        self._trace_id_map: t.Dict[str, UUID] = {}
        self._workspace_id = self.register_workspace(
            name=workspace_name,
            params=params,
        )
        self.workspace_name = workspace_name
        self._logger = logger

    def _post(self, url: str, data: t.Any) -> Response:
        return requests.post(
            url,
            data=dumps(data, cls=CustomJSONEncoder),
        )

    def register_workspace(self, name: str, params: t.Dict[str, t.Any]) -> UUID:
        res = self._post(
            urljoin(self.url, 'workspace'),
            data={
                "name": name,
                "params": params,
            }
        )
        res.raise_for_status()
        return res.json()

    def register_trace(self, name: str) -> UUID:
        if name in self._trace_id_map:
            return self._trace_id_map[name]
        res = self._post(
            urljoin(self.url, 'trace'),
            data={
                "name": name,
                'workspace_id': self._workspace_id,
            }
        )
        res.raise_for_status()
        self._trace_id_map[name] = res.json()
        return res.json()

    def add_scalar(self, name: str, value: float, ts: t.Optional[datetime] = None) -> int:
        trace_id = self.register_trace(name)
        res = self._post(
            urljoin(self.url, 'point/add-scalar'),
            data={
                "trace_id": trace_id,
                "value": value,
                "ts": ts,
            }
        )
        res.raise_for_status()
        if self._logger is not None:
            self._logger.info(f"{self.workspace_name} - add_scalar '{name}': {value}")
        return res.json()

    def add_scalars(self, values: t.Dict[str, float], ts: t.Optional[datetime] = None) -> int:
        _values = {self.register_trace(k): v for k, v in values.items()}
        res = self._post(
            urljoin(self.url, 'point/add-scalars'),
            data={
                "values": _values,
                "ts": ts,
            }
        )
        res.raise_for_status()
        if self._logger is not None:
            self._logger.info(f'{self.workspace_name} - add_scalars: {values}')
        return res.json()
