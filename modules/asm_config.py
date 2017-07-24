# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

import os.path
from os import mkdir
import configparser
import sys

myfile = os.path.expanduser('~/.asmaa/asmaafile.cfg')
config = configparser.RawConfigParser()
config.read(myfile)
section = 'settings'

if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(os.path.dirname(sys.executable))
else:
    APP_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DEFAULT_DATA   = os.path.join(APP_DIR, 'asmaa-librery', 'data', 'Listbooks.db')

def load():
    if not config.has_section(section):
        config.add_section(section)
    if not config.has_option(section, 'path'):
        config.set(section, 'path', DEFAULT_DATA)
    if not config.has_option(section, 'idx_quran'):
        config.set(section, 'idx_quran', 1)
    if not config.has_option(section, 'saved_session'):
        config.set(section, 'saved_session', 0)
    if not config.has_option(section, 'start_session'):
        config.set(section, 'start_session', '[[],0,[]]')
    if not config.has_option(section, 'font_window'):
        config.set(section, 'font_window', 'KacstOne 12')
    if not config.has_option(section, 'font_lists_titles'):
        config.set(section, 'font_lists_titles', 'KacstOne 13')
    if not config.has_option(section, 'font_quran'):
        config.set(section, 'font_quran', 'Amiri Quran 25')
    if not config.has_option(section, 'font_lists_parts'):
        config.set(section, 'font_lists_parts', 'KacstOne 15')
    if not config.has_option(section, 'font_lists_books'):
        config.set(section, 'font_lists_books', 'KacstOne 14')
    if not config.has_option(section, 'font_nasse_books'):
        config.set(section, 'font_nasse_books', 'نسخ مبسط 20')
    if not config.has_option(section, 'font_nasse_others'):
        config.set(section, 'font_nasse_others', 'Amiri 16')
    if not config.has_option(section, 'font_anawin'):
        config.set(section, 'font_anawin', 'KacstOne 15')
    if not config.has_option(section, 'color_lists_parts'):
        config.set(section, 'color_lists_parts', '#868609091515')
    if not config.has_option(section, 'color_lists_books'):
        config.set(section, 'color_lists_books', '#202040400000')
    if not config.has_option(section, 'color_nasse_books'):
        config.set(section, 'color_nasse_books', '#202040400000')
    if not config.has_option(section, 'color_nasse_others'):
        config.set(section, 'color_nasse_others', '#202040400000')
    if not config.has_option(section, 'color_anawin'):
        config.set(section, 'color_anawin', '#868609091515')
    if not config.has_option(section, 'color_lists_titles'):
        config.set(section, 'color_lists_titles', '#868609091515')
    if not config.has_option(section, 'color_quran'):
        config.set(section, 'color_quran', '#868609091515')
    if not config.has_option(section, 'background_lists_parts'):
        config.set(section, 'background_lists_parts', '#fdfdfdfdd7d7')
    if not config.has_option(section, 'background_lists_books'):
        config.set(section, 'background_lists_books', '#fdfdfdfdd7d7')
    if not config.has_option(section, 'background_nasse_books'):
        config.set(section, 'background_nasse_books', '#fdfdfdfdd7d7')
    if not config.has_option(section, 'background_nasse_others'):
        config.set(section, 'background_nasse_others', '#fdfdfdfdd7d7')
    if not config.has_option(section, 'background_anawin'):
        config.set(section, 'background_anawin', '#fdfdfdfdd7d7')
    if not config.has_option(section, 'background_lists_titles'):
        config.set(section, 'background_lists_titles', '#fdfdfdfdd7d7')
    if not config.has_option(section, 'background_quran'):
        config.set(section, 'background_quran', '#fdfdfdfdd7d7')
    if not config.has_option(section, 'color_selected'):
        config.set(section, 'color_selected', '#ffffffffffff')
    if not config.has_option(section, 'background_selected'):
        config.set(section, 'background_selected', '#9e9ec1c17a7a')
    if not config.has_option(section, 'color_searched'):
        config.set(section, 'color_searched', '#ffffffffffff')
    if not config.has_option(section, 'background_searched'):
        config.set(section, 'background_searched', '#fe71fab0870b')
    if not config.has_option(section, 'color_hover'):
        config.set(section, 'color_hover', '#ffffffffffff')
    if not config.has_option(section, 'background_hover'):
        config.set(section, 'background_hover', '#9e9ec1c17a7a')
    if not config.has_option(section, 'theme'):
        config.set(section, 'theme',1)
    if not config.has_option(section, 'tashkil'):
        config.set(section, 'tashkil', 1)
    if not config.has_option(section, 'marks'):
        config.set(section, 'marks', '[]')
    if not config.has_option(section, 'list_tafsir'):
        config.set(section, 'list_tafsir', '[3, [], 0]')
    if not config.has_option(section, 'quran_pos'):
        config.set(section, 'quran_pos', 1)
    if not config.has_option(section, 'view_books'):
        config.set(section, 'view_books', 1)
    if not config.has_option(section, 'show_side'):
        config.set(section, 'show_side', 0)
    if not config.has_option(section, 'mouse_browse'):
        config.set(section, 'mouse_browse', 1)
    if not config.has_option(section, 'style_browse'):
        config.set(section, 'style_browse', 3)
    if not config.has_option(section, 'time_browse'):
        config.set(section, 'time_browse', 3)
    if not config.has_option(section, 'auto_browse'):
        config.set(section, 'auto_browse', 3)
    if not config.has_option(section, 'nmbrs'):
        config.set(section, 'nmbrs', 0)
    if not config.has_option(section, 'search'):
        config.set(section, 'search', 0)
    with open(myfile, 'w') as configfile:
        config.write(configfile)

def setv(option, value):
    config.set(section, option, value)
    with open(myfile, 'w') as configfile:
        config.write(configfile)
   
def getv(option):
    value = config.get(section, option)
    return value

def getn(option):
    value = config.getint(section, option)
    return value

def getf(option):
    value = config.getfloat(section, option)
    return value
  
mydir = os.path.dirname(myfile)
if not os.path.exists(mydir):
    try:  mkdir(mydir)
    except: raise

if not os.path.exists(os.path.join(mydir, 'searchs')):
    try:  mkdir(os.path.join(mydir, 'searchs'))
    except: raise

if not os.path.exists(myfile):
    try: 
        open(myfile,'w+')
    except: raise
load()
