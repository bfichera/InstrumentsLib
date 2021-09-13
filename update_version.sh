#!/bin/bash

echo $1 > .version
echo -ne "from .instrument import instrument\nfrom .utilities import get_instrument_cfg\n__version__ = '$1'\n" > instrumentslib/__init__.py
