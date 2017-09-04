# -*- coding: utf-8 -*-
from models import Singleton
"""

Controlador principal de la Lib.
Author: Jose A. Salgado.

"""


class Controller(object):
    """
    Implementación del controlador principal de la librería.
    """
    __metaclass__ = Singleton

    def __init__(self):
        pass

    def _build_scenario(self):
        """

        :return:
        """
        # Load Config

        # Create folders
