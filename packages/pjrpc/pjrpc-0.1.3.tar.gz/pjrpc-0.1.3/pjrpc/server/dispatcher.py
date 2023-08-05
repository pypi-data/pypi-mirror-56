import asyncio
import collections
import functools as ft
import json
import logging

import pjrpc
from pjrpc.common import v20, UNSET
from . import validators

logger = logging.getLogger(__package__)

default_validator = validators.base.BaseValidator()


class Method:
    """
    JSON-RPC method wrapper. Stores method itself and some metainformation.

    :param method: method
    :param name: method name
    :param context: context name
    """

    def __init__(self, method, name=None, context=None):
        self.method = method
        self.name = name or getattr(method, 'name', method.__name__)
        self.context = context
        self.validator, self.validator_args = getattr(method, '__pjrpc_meta__', (default_validator, {}))

    def bind(self, params, context=None):
        method_params = self.validator.validate_method(
            self.method, params, exclude=(self.context,) if self.context else (), **self.validator_args
        )

        if self.context is not None:
            method_params[self.context] = context

        return ft.partial(self.method, **method_params)


class ViewMethod(Method):
    """
    View method.

    :param view_cls: view class
    :param name: view class method name
    :param context: context name
    """

    def __init__(self, view_cls, name, context=None):
        super().__init__(view_cls, name, context)

        self.view_cls = view_cls

    def bind(self, params, context=None):
        view = self.view_cls(context) if self.context else self.view_cls()
        method = getattr(view, self.name)

        method_params = self.validator.validate_method(method, params, **self.validator_args)

        return ft.partial(method, **method_params)


class View:
    """
    Class based method handler.
    """

    @classmethod
    def __methods__(cls):
        for attr_name in filter(lambda name: not name.startswith('_'), dir(cls)):
            attr = getattr(cls, attr_name)
            if callable(attr):
                yield attr


class MethodRegistry:
    """
    Method registry.

    :param prefix: method name prefix to be used for naming containing methods
    """

    def __init__(self, prefix=None):
        self._prefix = prefix
        self._registry = {}

    def __iter__(self):
        """
        Returns registry method iterator.
        """

        return iter(self._registry)

    def __getitem__(self, item):
        """
        Returns a method from the registry by name.

        :param item: method name
        :returns: found method
        :raises: KeyError
        """

        return self._registry[item]

    def get(self, item):
        """
        Returns a method from the registry by name.

        :param item: method name
        :returns: found method or `None`
        """

        return self._registry.get(item)

    def add(self, maybe_method=None, name=None, context=None):
        """
        Decorator adding decorated method to the registry.

        :param maybe_method: method or `None`
        :param name: method name to be used instead of `__name__` attribute
        :param context: parameter name to be used as an application context
        :returns: decorated method or decorator
        """

        def decorator(method):
            full_name = '.'.join(filter(None, (self._prefix, name or getattr(method, 'name', method.__name__))))
            self.add_methods(Method(method, full_name, context))

            return method

        if maybe_method is None:
            return decorator
        else:
            return decorator(maybe_method)

    def add_methods(self, *methods):
        """
        Adds methods to the registry.

        :param methods: methods to be added. Each one can be an instance of :py:class:`pjrpc.server.Method`
                        or plain method
        """

        for method in methods:
            if isinstance(method, Method):
                self._add_method(method.name, method)
            else:
                self.add(method)

    def view(self, maybe_view=None, context=None, prefix=None):
        """
        Methods view decorator.

        :param maybe_view: view class instance or `None`
        :param context: application context name
        :param prefix: view methods prefix
        :return: decorator or decorated view
        """

        def decorator(view):
            for method in view.__methods__():
                full_name = '.'.join(filter(None, (self._prefix, prefix, method.__name__)))
                self._add_method(full_name, ViewMethod(view, method.__name__, context))

            return view

        # maybe_view's type depends on the usage of the decorator.  It's a View
        # if it's used as `@view` but ``None`` if used as `@view()`.
        if maybe_view is None:
            return decorator
        else:
            return decorator(maybe_view)

    def merge(self, other):
        """
        Merges two registries.

        :param other: registry to be merged in the current one
        """

        for name in other:
            self._add_method(name, other[name])

    def _add_method(self, name, method):
        if name in self._registry:
            logger.warning(f"method '{name}' already registered")

        self._registry[name] = method


class Dispatcher:
    """
    Method dispatcher.

    :param request_class: JSON-RPC request class
    :param response_class: JSON-RPC response class
    :param batch_request: JSON-RPC batch request class
    :param batch_response: JSON-RPC batch response class
    :param json_loader: request json loader
    :param json_dumper: response json dumper
    :param json_encoder: response json encoder
    :param json_decoder: request json decoder
    :param error_handler: error handling function
    """

    def __init__(
        self,
        *,
        request_class=v20.Request,
        response_class=v20.Response,
        batch_request=v20.BatchRequest,
        batch_response=v20.BatchResponse,
        json_loader=json.loads,
        json_dumper=json.dumps,
        json_encoder=None,
        json_decoder=None,
        error_handler=None,
    ):
        self._json_loader = json_loader
        self._json_dumper = json_dumper
        self._json_encoder = json_encoder or pjrpc.JSONEncoder
        self._json_decoder = json_decoder
        self._request_class = request_class
        self._response_class = response_class
        self._batch_request = batch_request
        self._batch_response = batch_response
        self._error_handler = error_handler or self._handle_jsonrpc_error

        self._registry = MethodRegistry()

    def add(self, method, name=None, context=None):
        """
        Adds method to the registry.

        :param method: method
        :param name: method name
        :param context: application context name
        :returns:
        """

        self._registry.add(method, name, context)

    def add_methods(self, *methods):
        """
        Adds methods to the registry.

        :param methods: method list. Each method may be an instance of :py:class:`pjrpc.server.MethodRegistry`,
                        :py:class:`pjrpc.server.Method` or plain function
        """

        for method in methods:
            if isinstance(method, MethodRegistry):
                self._registry.merge(method)
            elif isinstance(method, Method):
                self._registry.add_methods(method)
            else:
                self._registry.add(method)

    def view(self, view):
        """
        Adds class based view to the registry.

        :param view: view to be added
        """

        self._registry.view(view)

    def dispatch(self, request_text, context=None):
        """
        Deserializes request, dispatches it to the required method and serializes the result.

        :param request_text: request text representation
        :param context: application context (if supported)
        :return: response text representation
        """

        logger.debug("request received: %s", request_text)

        try:
            request_json = self._json_loader(request_text, cls=self._json_decoder)
            if isinstance(request_json, (list, tuple)):
                request = self._batch_request.from_json(request_json)
            else:
                request = self._request_class.from_json(request_json)

        except json.JSONDecodeError as e:
            response = self._response_class(id=None, error=pjrpc.exceptions.ParseError(data=str(e)))

        except (pjrpc.exceptions.DeserializationError, pjrpc.exceptions.IdentityError) as e:
            response = self._response_class(id=None, error=pjrpc.exceptions.InvalidRequestError(data=str(e)))

        else:
            if isinstance(request, collections.Iterable):
                response = self._batch_response(*filter(lambda resp: resp is not UNSET, (
                    self._handle_rpc_request(request, context) for request in request
                )))

            else:
                response = self._handle_rpc_request(request, context)

        if response is not UNSET:
            response_text = self._json_dumper(response.to_json(), cls=self._json_encoder)
            logger.debug("response sent: %s", response_text)

            return response_text

    def _handle_rpc_request(self, request, context):
        response_id, result, error = request.id, UNSET, UNSET

        try:
            result = self._handle_rpc_method(request.method, request.params, context)
        except pjrpc.exceptions.JsonRpcError as e:
            logger.info("method execution error %s(%r): %r", request.method, request.params, e)
            error = e
        except Exception as e:
            logger.exception("internal server error: %r", e)
            error = pjrpc.exceptions.InternalError()

        if response_id is None:
            return UNSET

        if error:
            error = self._error_handler(error)

        return self._response_class(id=response_id, result=result, error=error)

    def _handle_rpc_method(self, method_name, params, context):
        method = self._registry.get(method_name)
        if method is None:
            raise pjrpc.exceptions.MethodNotFoundError(data=f"method '{method_name}' not found")

        try:
            method = method.bind(params, context=context)
        except validators.ValidationError as e:
            raise pjrpc.exceptions.InvalidParamsError(data=e) from e

        try:
            return method()

        except pjrpc.exceptions.JsonRpcError:
            raise

        except Exception as e:
            logger.exception("method unhandled exception %s(%r): %r", method_name, params, e)
            raise pjrpc.exceptions.ServerError() from e

    def _handle_jsonrpc_error(self, error):
        if error and error.data:
            error.data = str(error.data)

        return error


class AsyncDispatcher(Dispatcher):
    """
    Asynchronous method dispatcher.
    """

    async def dispatch(self, request_text, context=None):
        """
        Deserializes request, dispatches it to the required method and serializes the result.

        :param request_text: request text representation
        :param context: application context (if supported)
        :return: response text representation
        """

        logger.debug("request received: %s", request_text)

        try:
            request_json = self._json_loader(request_text, cls=self._json_decoder)
            if isinstance(request_json, (list, tuple)):
                request = self._batch_request.from_json(request_json)
            else:
                request = self._request_class.from_json(request_json)

        except json.JSONDecodeError as e:
            response = self._response_class(id=None, error=pjrpc.exceptions.ParseError(data=str(e)))

        except (pjrpc.exceptions.DeserializationError, pjrpc.exceptions.IdentityError) as e:
            response = self._response_class(id=None, error=pjrpc.exceptions.InvalidRequestError(data=str(e)))

        else:
            if isinstance(request, collections.Iterable):
                response = self._batch_response(*filter(lambda resp: resp is not UNSET, [
                    await self._handle_rpc_request(request, context) for request in request
                ]))

            else:
                response = await self._handle_rpc_request(request, context)

        if response is not UNSET:
            response_text = self._json_dumper(response.to_json(), cls=self._json_encoder)
            logger.debug("response sent: %s", response_text)

            return response_text

    async def _handle_rpc_request(self, request, context):
        response_id, result, error = request.id, UNSET, UNSET

        try:
            result = await self._handle_rpc_method(request.method, request.params, context)
        except pjrpc.exceptions.JsonRpcError as e:
            logger.info("method execution error %s(%r): %r", request.method, request.params, e)
            error = e
        except Exception as e:
            logger.exception("internal server error: %r", e)
            error = pjrpc.exceptions.InternalError()

        if response_id is None:
            return UNSET

        if error:
            error = self._error_handler(error)

        return self._response_class(id=response_id, result=result, error=error)

    async def _handle_rpc_method(self, method_name, params, context):
        method = self._registry.get(method_name)
        if method is None:
            raise pjrpc.exceptions.MethodNotFoundError(data=f"method '{method_name}' not found")

        try:
            method = method.bind(params, context=context)
        except validators.ValidationError as e:
            raise pjrpc.exceptions.InvalidParamsError(data=e) from e

        try:
            result = method()
            if asyncio.iscoroutine(result):
                result = await result

            return result

        except pjrpc.exceptions.JsonRpcError:
            raise

        except Exception as e:
            logger.exception("method unhandled exception %s(%r): %r", method_name, params, e)
            raise pjrpc.exceptions.ServerError() from e
