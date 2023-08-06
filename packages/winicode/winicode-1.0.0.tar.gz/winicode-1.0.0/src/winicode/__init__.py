# -*- coding: utf-8 -*-


import os
import sys


if os.name == 'nt':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf8')
