# -*- coding: utf-8 -*-

import os

"""
Applocation Globals
"""

HERE_PATH =  os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.abspath(os.path.join(HERE_PATH, ".."))

print(ROOT_PATH)
STATIC_PATH = os.path.abspath(os.path.join(ROOT_PATH, "openplc_desktop", "static"))


import settings as settings_lib


settings = settings_lib.XSettings()
"""instance of :class:`settings_lib.XSettings` """



