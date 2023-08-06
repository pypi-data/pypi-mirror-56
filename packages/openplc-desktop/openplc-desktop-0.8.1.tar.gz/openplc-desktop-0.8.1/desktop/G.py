# -*- coding: utf-8 -*-

import os

## App Globals

HERE_PATH =  os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.abspath(os.path.join(HERE_PATH, ".."))

STATIC_PATH = os.path.abspath(os.path.join(ROOT_PATH, "static"))

import settings as settings_lib


settings = settings_lib.XSettings()


