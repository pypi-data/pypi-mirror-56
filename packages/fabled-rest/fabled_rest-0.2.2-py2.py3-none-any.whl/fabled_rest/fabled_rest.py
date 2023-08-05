import copy
import json
import logging

import requests
from tqdm import tqdm

from .local.progress.spinner import PixelSpinner2

try:
    from fabled_rest.handlers.errors import ErrorHandler
except ImportError:
    from fabled_rest.fabled_rest.handlers.errors import ErrorHandler


class ApiClient:
    """Chainable, magical class helps you make requests to RESTful services"""

    HTTP_METHODS = ['get', 'options', 'head', 'post', 'put', 'patch', 'delete']

    def __init__(self, name=None, parent=None, append_slash=False, **kwargs):
        """Constructor

        Arguments:
            name -- name of node
            parent -- parent node for chaining
            append_slash -- flag if you want a trailing slash in urls
            **kwargs -- `requests` session be initiated with if any available
        """
        self._name = name
        self._parent = parent
        self._append_slash = append_slash
        self._session = requests.session()
        for k, v in kwargs.items():
            orig = getattr(self._session, k, None)
            if isinstance(orig, dict):
                orig.update(v)
            elif orig:
                setattr(self._session, k, v)

    def _spawn(self, name):
        """Returns a shallow copy of current `ApiClient` instance as nested child

        Arguments:
            name -- name of child
        """
        child = copy.copy(self)
        child._name = name
        child._parent = self
        return child

    def __getattr__(self, name):
        """Here comes some magic. Any absent attribute typed within class
        falls here and return a new child `ApiClient` instance in the chain.
        """
        # Ignore specials (Otherwise shallow copying causes infinite loops)
        if name.startswith('__'):
            raise AttributeError(name)
        return self._spawn(name)

    def __iter__(self):
        """Iterator implementation which iterates over `ApiClient` chain."""
        current = self
        while current:
            if current._name:
                yield current
            current = current._parent

    def _chain(self, *args):
        """This method converts args into chained ApiClient instances

        Arguments:
            *args -- array of string representable objects
        """
        chain = self
        for arg in args:
            chain = chain._spawn(str(arg))
        return chain

    def _close_session(self):
        """Closes session if exists"""
        if self._session:
            self._session.close()

    def __call__(self, *args):
        """Here comes second magic. If any `ApiClient` instance called it
        returns a new child `Hammock` instance in the chain
        """
        return self._chain(*args)

    def _url(self, *args):
        """Converts current `ApiClient` chain into a url string

        Arguments:
            *args -- extra url path components to tail
        """
        path_comps = [mock._name for mock in self._chain(*args)]
        url = "/".join(reversed(path_comps))
        if self._append_slash:
            url = url + "/"
        return url

    def __repr__(self):
        """ String representation of current `ApiClient` chain"""
        return self._url()

    def _request(self, method, *args, **kwargs):
        """
        Makes the HTTP request using requests module
        """
        return self._session.request(method, self._url(*args), **kwargs)


def bind_method(method, post_hook=None, ):
    """Bind `requests` module HTTP verbs to `ApiClient` class as
    static methods."""

    def aux(hammock, *args, **kwargs):
        response = hammock._request(method, *args, **kwargs)
        ErrorHandler(response)
        if post_hook and callable(post_hook):
            response = post_hook(hammock, response)
        return response

    return aux


class FabledREST(object):
    def __init__(self, base_url, client_data: dict = None, post_hook=None, **kwargs):
        if base_url:
            for m in ApiClient.HTTP_METHODS:
                setattr(ApiClient, m.upper(), bind_method(m, post_hook=post_hook))
            self.client = ApiClient(base_url, **client_data or {})
        if kwargs:
            self.update_self(**kwargs)
        self._name = self.__class__.__name__

    def __str__(self):
        return f"({self._name}) {str(self.dict())}"

    def __dir__(self):
        return self.__dict__.keys()

    def __call__(self, *args, **kwargs):
        clone = copy.copy(self)
        if kwargs:
            return clone.update_self(**kwargs)
        return clone

    def __getattribute____(self, item):
        clone = copy.copy(self)
        return object.__getattribute__(clone, item)

    def json(self, include_only=None):
        return json.dumps(self.dict(include_only=include_only))

    def dict(self, include_only: list = None):
        if len(self.__dict__) < 1:
            return {}
        if include_only:
            include = {k: v for k, v in self.__dict__.items() if k in include_only}
            return {k: v for k, v in include.items() if v and k[0] != '_' and k != 'client'}
        return {k: v for k, v in self.__dict__.items() if v and k[0] != '_' and k != 'client'}

    def update_self(self, **kwargs):
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)
        return self

    @staticmethod
    def progress(*args, **kwargs):
        return tqdm(*args, **kwargs)

    @staticmethod
    def spinner(*args, **kwargs):
        return PixelSpinner2(*args, **kwargs)

    @property
    def logger(self):
        import sys
        name = '.'.join([
            self.__module__,
            self.__class__.__name__
        ])
        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(asctime)s] %(levelname)s %(name)s:%(lineno)d %(message)s",
            datefmt="%H:%M:%S",
            stream=sys.stdout)
        return logging.getLogger(name)
