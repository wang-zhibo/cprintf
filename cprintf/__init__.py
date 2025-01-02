#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Author:
# E-mail:
# Date  :
# Desc  :

from .color_print import ColorPrint

debug = ColorPrint.debug
info = ColorPrint.info
ok = ColorPrint.ok
warn = ColorPrint.warn
err = ColorPrint.err
fatal = ColorPrint.fatal
custom = ColorPrint.custom
line = ColorPrint.line
progress_bar = ColorPrint.progress_bar
print_table = ColorPrint.print_table
get_colored_string = ColorPrint.get_colored_string
set_log_level = ColorPrint.set_log_level

__all__ = [
    "ColorPrint",
    "set_log_level",
    "debug",
    "ok",
    "info",
    "warn",
    "err",
    "fatal",
    "custom",
    "line",
    "progress_bar",
    "print_table",
    "get_colored_string"
]

