#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################


from subprocess import call
from os.path import join, dirname, realpath, exists, expanduser
import sys

if getattr(sys, 'frozen', False):
    APP_DIR = dirname(sys.executable)
else:
    APP_DIR = dirname(realpath(__file__))
def main(): 
    call(['python3', join(APP_DIR, 'asm_window.py')])
