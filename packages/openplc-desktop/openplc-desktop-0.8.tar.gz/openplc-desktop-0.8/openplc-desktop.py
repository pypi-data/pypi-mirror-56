#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Peter Morgan <pete@daffodil.uk.com>
@copyright: Peter Morgan

"""

import argparse

import desktop
import desktop.main_window

parser = argparse.ArgumentParser(description="Launch desktop application")
parser.add_argument("--pedro", help="Pedro's Developer mode", action="store_true")

if __name__ == '__main__':


    args = parser.parse_args()

    desktop.start_app(desktop.main_window.MainWindow, args)
