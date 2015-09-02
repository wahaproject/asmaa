# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

import os.path
from os import mkdir
import configparser

myfile = os.path.expanduser('~/.asmaa/asmaafile.cfg')
config = configparser.RawConfigParser()
config.read(myfile)
section = 'settings'

def load():
    if not config.has_section(section):
        config.add_section(section)
    if not config.has_option(section, 'path'):
        config.set(section, 'path', os.path.expanduser('~/.asmaa/asmaa-library/data/Listbooks.db'))
    if not config.has_option(section, 'idx_qrn'):
        config.set(section, 'idx_qrn', 1)
    if not config.has_option(section, 'saved_session'):
        config.set(section, 'saved_session', 0)
    if not config.has_option(section, 'start_session'):
        config.set(section, 'start_session', '[[],0,[]]')
    if not config.has_option(section, 'font_tit'):
        config.set(section, 'font_tit', 'KacstOne 15')
    if not config.has_option(section, 'font_prts'):
        config.set(section, 'font_prts', 'KacstOne 18')
    if not config.has_option(section, 'font_bks'):
        config.set(section, 'font_bks', 'KacstOne 15')
    if not config.has_option(section, 'font_nass'):
        config.set(section, 'font_nass', 'Simplified Naskh 22')
    if not config.has_option(section, 'font_oth'):
        config.set(section, 'font_oth', 'Simplified Naskh 22')
    if not config.has_option(section, 'font_qrn'):
        config.set(section, 'font_qrn', 'Amiri Quran 23')
    if not config.has_option(section, 'font_idx'):
        config.set(section, 'font_idx', 'KacstOne 15')
    if not config.has_option(section, 'color_tit'):
        config.set(section, 'color_tit', '#868609091515')
    if not config.has_option(section, 'color_idx'):
        config.set(section, 'color_idx', '#676f0584533d')
    if not config.has_option(section, 'color_nass'):
        config.set(section, 'color_nass', '#202040400000')
    if not config.has_option(section, 'color_oth'):
        config.set(section, 'color_oth', '#202040400000')
    if not config.has_option(section, 'color_qrn'):
        config.set(section, 'color_qrn', '#202040400000')
    if not config.has_option(section, 'color_prts'):
        config.set(section, 'color_prts', '#202040400000')
    if not config.has_option(section, 'color_bks'):
        config.set(section, 'color_bks', '#868609091515')
    if not config.has_option(section, 'color_bg'):
        config.set(section, 'color_bg', '#fdfdfdfdd7d7')
    if not config.has_option(section, 'color_bgs'):
        config.set(section, 'color_bgs', '#fca9fca9f231')
    if not config.has_option(section, 'color_sel'):
        config.set(section, 'color_sel', '#ffffffffffff')
    if not config.has_option(section, 'color_bg_sel'):
        config.set(section, 'color_bg_sel', '#9e9ec1c17a7a')
    if not config.has_option(section, 'color_fnd'):
        config.set(section, 'color_fnd', '#fe71fab0870b')
    if not config.has_option(section, 'color_bg_qrn'):
        config.set(section, 'color_bg_qrn', '#fcb2eb47aeb5')
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
if not os.path.exists(myfile):
    try: 
        open(myfile,'w+')
    except: raise
load()
