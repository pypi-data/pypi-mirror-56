from aiohttp import test_utils
from aiohttp.helpers import noop
from aiohttp.web_response import StreamResponse
from guillotina import app_settings
from guillotina import configure
from guillotina import routes
from guillotina import task_vars
from guillotina.api.service import Service
from guillotina.component import get_utility
from guillotina.component import query_multi_adapter
from guillotina.db.transaction import Status
from guillotina.exceptions import ConflictError
from guillotina.interfaces import ACTIVE_LAYERS_KEY
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import IContainer
from guillotina.interfaces import IPermission
from guillotina.response import ErrorResponse
from guillotina.response import HTTPError
from guillotina.response import HTTPPreconditionFailed
from guillotina.response import Response
from guillotina.security.utils import get_view_permission
from guillotina.transactions import get_tm
from guillotina.transactions import get_transaction
from guillotina.traversal import generate_error_response
from guillotina.traversal import traverse
from guillotina.utils import get_registry
from guillotina.utils import get_security_policy
from guillotina.utils import import_class
from multidict import CIMultiDict
from unittest import mock
from urllib.parse import urlparse
from yarl import URL
from zope.interface import alsoProvides

import backoff
import logging
import posixpath
import ujson


logger = logging.getLogger("guillotina_batch")


class SimplePayload:
    def __init__(self, data):
        self.data = data
        self.read = False

    async def readany(self):
        if self.read:
            return bytearray()
        self.read = True
        return bytearray(self.data, "utf-8")

    def at_eof(self):
        return self.read


async def abort_txn(ctx):
    tm = get_tm()
    await tm.abort()


@configure.service(
    method="POST",
    name="@batch",
    context=IContainer,
    permission="guillotina.AccessContent",
    parameters=[
        {
            "name": "eager-commit",
            "description": "Commit changes to database for each individual request",
            "in": "query",
            "default": False,
            "type": "boolean",
        }
    ],
    requestBody={
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "array",
                    "title": "Requests in batch",
                    "in": "body",
                    "default": [],
                    "items": {
                        "type": "object",
                        "properties": {
                            "method": {"type": "string", "description": "View method"},
                            "endpoint": {
                                "type": "string",
                                "description": "View full path",
                            },
                            "payload": {
                                "type": "object",
                                "default": {},
                                "description": "View body payload",
                            },
                            "headers": {
                                "type": "object",
                                "default": {},
                                "description": "View headers",
                            },
                        },
                        "required": ["method", "endpoint"],
                    },
                }
            }
        },
    },
    responses={
        "200": {
            "description": "Successfully registered interface",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "description": "List of responses for each view in batch",
                        "items": {
                            "type": "object",
                            "properties": {
                                "status": {
                                    "type": "int",
                                    "description": "Response status code",
                                },
                                "success": {
                                    "type": "boolean",
                                    "description": "Whether response was successful",
                                },
                                "body": {"type": "object", "properties": {}},
                            },
                        },
                    }
                }
            },
        }
    },
    allow_access=True,
    validate=True,
)
class Batch(Service):

    _eager_commit = False

    def __init__(self, context, request, eager_commit=False):
        super().__init__(context, request)
        self._eager_commit = eager_commit

    @property
    def eager_commit(self):
        return (
            self._eager_commit
            or self.request.query.get("eager-commit", "false").lower() == "true"
        )

    async def clone_request(self, method, endpoint, payload, headers):
        container = task_vars.container.get()
        container_url = IAbsoluteURL(container, self.request)()
        url = posixpath.join(container_url, endpoint)
        parsed = urlparse(url)
        dct = {"method": method, "url": URL(url), "path": parsed.path}
        dct["headers"] = CIMultiDict(headers)
        dct["raw_headers"] = tuple(
            (k.encode("utf-8"), v.encode("utf-8")) for k, v in headers.items()
        )

        message = self.request._message._replace(**dct)

        payload_writer = mock.Mock()
        payload_writer.write_eof.side_effect = noop
        payload_writer.drain.side_effect = noop

        protocol = mock.Mock()
        protocol.transport = test_utils._create_transport(None)
        protocol.writer = payload_writer

        request = self.request.__class__(
            message,
            SimplePayload(payload),
            protocol,
            payload_writer,
            self.request._task,
            self.request._loop,
            client_max_size=self.request._client_max_size,
            state=self.request._state.copy(),
            scheme=self.request.scheme,
            host=self.request.host,
            remote=self.request.remote,
        )

        registry = await get_registry(container)
        layers = registry.get(ACTIVE_LAYERS_KEY, [])
        for layer in layers:
            try:
                alsoProvides(request, import_class(layer))
            except ModuleNotFoundError:
                pass
        return request

    async def handle(self, message):
        payload = message.get("payload") or {}
        if not isinstance(payload, str):
            payload = ujson.dumps(payload)
        headers = dict(self.request.headers)
        headers.update(message.get("headers") or {})
        request = await self.clone_request(
            message["method"], message["endpoint"], payload, headers
        )
        try:
            task_vars.request.set(request)
            try:
                result = await self._handle(request, message)
            except Exception as err:
                if self.eager_commit:
                    tm = get_tm()
                    await tm.abort()
                logger.warning("Error executing batch item", exc_info=True)
                result = self._gen_result(
                    generate_error_response(err, request, "ViewError")
                )
            return result
        finally:
            task_vars.request.set(self.request)

    @backoff.on_exception(
        backoff.constant, ConflictError, max_tries=3, on_backoff=abort_txn
    )
    async def _handle(self, request, message):
        tm = get_tm()
        txn = get_transaction()
        if txn.status in (Status.ABORTED, Status.COMMITTED, Status.CONFLICT):
            # start txn
            txn = await tm.begin()

        method = app_settings["http_methods"][message["method"].upper()]
        endpoint = urlparse(message["endpoint"]).path
        path = tuple(p for p in endpoint.split("/") if p)
        obj, tail = await traverse(request, task_vars.container.get(), path)

        if tail and len(tail) > 0:
            # convert match lookups
            view_name = routes.path_to_view_name(tail)
            # remove query params from view name
            view_name = view_name.split("?")[0]
        elif not tail:
            view_name = ""
        else:
            raise

        permission = get_utility(IPermission, name="guillotina.AccessContent")

        security = get_security_policy()
        allowed = security.check_permission(permission.id, obj)
        if not allowed:
            return {"success": False, "body": {"reason": "Not allowed"}, "status": 401}

        try:
            view = query_multi_adapter((obj, request), method, name=view_name)
        except AttributeError:
            view = None

        try:
            view.__route__.matches(request, tail or [])
        except (KeyError, IndexError, AttributeError):
            view = None

        if view is None:
            return {"success": False, "body": {"reason": "Not found"}, "status": 404}

        ViewClass = view.__class__
        view_permission = get_view_permission(ViewClass)
        if not security.check_permission(view_permission, view):
            return {
                "success": False,
                "body": {"reason": "No view access"},
                "status": 401,
            }

        if hasattr(view, "prepare"):
            view = (await view.prepare()) or view

        view_result = await view()

        if self.eager_commit:
            await tm.commit()

        return self._gen_result(view_result)

    def _gen_result(self, view_result):
        if isinstance(view_result, Response):
            return {
                "body": getattr(
                    view_result, "content", getattr(view_result, "response", {})
                ),
                "status": getattr(
                    view_result, "status_code", getattr(view_result, "status", 200)
                ),
                "success": not isinstance(view_result, (ErrorResponse, HTTPError)),
            }
        elif isinstance(view_result, StreamResponse):
            return {
                "body": view_result.body.decode("utf-8"),
                "status": view_result.status,
                "success": True,
            }

        return {"body": view_result, "status": 200, "success": True}

    async def __call__(self):
        results = []
        messages = await self.request.json()
        if len(messages) >= app_settings["max_batch_size"]:
            return HTTPPreconditionFailed(
                content={
                    "reason": "Exceeded max match size limit",
                    "limit": app_settings["max_batch_size"],
                }
            )
        for message in messages:
            results.append(await self.handle(message))
        return results
