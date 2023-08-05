# -*- coding: utf-8 -*-
import logging
from .fabled_rest import FabledREST
from .handlers.endpoints import endpoint, fields, Field

"""Top-level package for Fabled REST."""

__author__ = """Zachary Young"""
__email__ = 'solve@fabled.dev'
__version__ = '0.2.2'

FabledREST = FabledREST
endpoint = endpoint
fields = fields
logging.getLogger('fabled_REST').addHandler(logging.NullHandler())
