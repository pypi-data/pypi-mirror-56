#!python
# -*- coding: utf-8 -*-
"""
@author: Peter Morgan <openplc@daffodil.uk.com>
@copyright: Peter Morgan

"""

import argparse

import openplc_desktop
import openplc_desktop.main_window

parser = argparse.ArgumentParser(description="Launch desktop application")
parser.add_argument("--pedro", help="Pedro's Developer mode", action="store_true")

if __name__ == '__main__':


    args = parser.parse_args()

    openplc_desktop.start_app(openplc_desktop.main_window.MainWindow, args)
