#!/bin/bash

if [ $UID -eq 0 ]; then
	python3 setup.py install --root=/ --record=installed-files.txt
else
	echo "Run this file as root (ex: sudo $0)."
fi
