# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from gi.repository import Gtk
import asm_config, asm_customs

#a----------------------------------------------------------------------       


class MyTheme(object):
    
    def apply_preference(self, *a):
        self.font_window = asm_config.getv('font_window')
        self.font_lists_parts = asm_config.getv('font_lists_parts')
        self.font_lists_books = asm_config.getv('font_lists_books')
        self.font_nasse_books = asm_config.getv('font_nasse_books')
        self.font_nasse_others = asm_config.getv('font_nasse_others')
        self.font_anawin = asm_config.getv('font_anawin')
        self.font_lists_titles = asm_config.getv('font_lists_titles')
        self.font_quran= asm_config.getv('font_quran')
        if asm_config.getn('theme') == 0:
            self.color_lists_parts = 'rgb(46,52,54)'
            self.color_lists_books = 'rgb(85,87,83)'
            self.color_nasse_books = 'rgb(85,87,83)'
            self.color_nasse_others = 'rgb(85,87,83)'
            self.color_anawin = 'rgb(204,0,0)'
            self.color_lists_titles = 'rgb(85,87,83)'
            self.color_quran= 'rgb(85,87,83)'
            self.background_quran= 'rgb(252,234,174)'
            self.background_lists_titles = 'rgb(253,253,215)'
            self.background_lists_parts = 'rgb(252,234,174)'
            self.background_lists_books = 'rgb(253,253,215)'
            self.background_nasse_books = 'rgb(253,253,215)'
            self.background_nasse_others = 'rgb(253,253,215)'
            self.background_anawin = 'rgb(253,253,215)'
            self.color_selected = 'rgb(52,52,52)'
            self.background_selected = 'rgb(221,221,221)'
            self.color_hover = 'rgb(52,52,52)'
            self.background_hover = 'rgb(221,221,221)'
            self.color_searched = 'rgb(85,87,83)'
            self.background_searched = 'rgb(243,201,96)'
        elif asm_config.getn('theme') == 1:
            self.color_lists_parts = 'rgb(32,74,155)'
            self.color_lists_books = 'rgb(32,74,135)'
            self.color_nasse_books = 'rgb(52,101,164)'
            self.color_nasse_others = 'rgb(52,101,164)'
            self.color_anawin = 'rgb(204,0,0)'
            self.color_lists_titles = 'rgb(85,87,83)'
            self.color_quran= 'rgb(85,87,83)'
            self.background_quran= 'rgb(252,234,174)'
            self.background_lists_titles = 'rgb(243,243,243)'
            self.background_lists_parts = 'rgb(233,233,233)'
            self.background_lists_books = 'rgb(243,243,243)'
            self.background_nasse_books = 'rgb(243,243,243)'
            self.background_nasse_others = 'rgb(243,243,243)'
            self.background_anawin = 'rgb(243,243,243)'
            self.color_selected = 'rgb(52,52,52)'
            self.background_selected = 'rgb(221,221,221)'
            self.color_hover = 'rgb(52,52,52)'
            self.background_hover = 'rgb(221,221,221)'
            self.color_searched = 'rgb(32,74,135)'
            self.background_searched = 'rgb(254,250,135)'
        elif asm_config.getn('theme') == 2:
            self.color_lists_parts = 'rgb(120,10,10)'
            self.color_lists_books = 'rgb(150,10,10)'
            self.color_nasse_books = 'rgb(92,53,102)'
            self.color_nasse_others = 'rgb(92,53,102)'
            self.color_anawin = 'rgb(204,0,0)'
            self.color_lists_titles = 'rgb(150,10,10)'
            self.color_quran= 'rgb(150,10,10)'
            self.background_quran= 'rgb(252,234,174)'
            self.background_lists_titles = 'rgb(255,225,225)'
            self.background_lists_parts = 'rgb(235,205,205)'
            self.background_lists_books = 'rgb(255,225,225)'
            self.background_nasse_books = 'rgb(255,225,225)'
            self.background_nasse_others = 'rgb(255,225,225)'
            self.background_anawin = 'rgb(255,225,225)'
            self.color_selected = 'rgb(255,255,255)'
            self.background_selected = 'rgb(249,124,124)'
            self.color_hover = 'rgb(255,255,255)'
            self.background_hover = 'rgb(249,124,124)'
            self.color_searched = 'rgb(92,53,102)'
            self.background_searched = 'rgb(254,250,135)'
        elif asm_config.getn('theme') == 3:
            self.color_lists_parts = 'rgb(20,47,28)'
            self.color_lists_books = 'rgb(32,64,0)'
            self.color_nasse_books = 'rgb(32,64,0)'
            self.color_nasse_others = 'rgb(32,64,0)'
            self.color_anawin = 'rgb(134,9,21)'
            self.color_lists_titles = 'rgb(32,64,0)'
            self.color_quran= 'rgb(32,64,0)'
            self.background_quran= 'rgb(252,234,174)'
            self.background_lists_titles = 'rgb(217,255,188)'
            self.background_lists_parts = 'rgb(158,193,122)'
            self.background_lists_books = 'rgb(217,255,188)'
            self.background_nasse_books = 'rgb(217,255,188)'
            self.background_nasse_others = 'rgb(217,255,188)'
            self.background_anawin = 'rgb(217,255,188)'
            self.color_selected = 'rgb(255,255,255)'
            self.background_selected = 'rgb(0,56,0)'
            self.color_hover = 'rgb(255,255,255)'
            self.background_hover = 'rgb(0,56,0)'
            self.color_searched = 'rgb(32,64,0)'
            self.background_searched = 'rgb(254,250,135)'
        elif asm_config.getn('theme') == 4:
            self.color_lists_parts = 'rgb(211,215,207)'
            self.color_lists_books = 'rgb(211,215,207)'
            self.color_nasse_books = 'rgb(238,238,236)'
            self.color_nasse_others = 'rgb(211,215,207)'
            self.color_anawin = 'rgb(252,234,174)'
            self.color_lists_titles = 'rgb(211,215,207)'
            self.color_quran= 'rgb(211,215,207)'
            self.background_quran= 'rgb(52,101,164)'
            self.background_lists_titles = 'rgb(92,53,102)'
            self.background_lists_parts = 'rgb(117,80,123)'
            self.background_lists_books = 'rgb(92,53,102)'
            self.background_nasse_books = 'rgb(92,53,102)'
            self.background_nasse_others = 'rgb(92,53,102)'
            self.background_anawin = 'rgb(92,53,102)'
            self.color_selected = 'rgb(46,52,54)'
            self.background_selected = 'rgb(186,189,182)'
            self.color_hover = 'rgb(46,52,54)'
            self.background_hover = 'rgb(186,189,182)'
            self.color_searched = 'rgb(238,238,236)'
            self.background_searched = 'rgb(143,89,2)'
        elif asm_config.getn('theme') == 5:
            self.color_lists_parts = 'rgb(211,215,207)'
            self.color_lists_books = 'rgb(211,215,207)'
            self.color_nasse_books = 'rgb(186,189,182)'
            self.color_nasse_others = 'rgb(186,189,182)'
            self.color_anawin = 'rgb(233,185,110)'
            self.color_lists_titles = 'rgb(211,215,207)'
            self.color_quran= 'rgb(211,215,207)'
            self.background_quran= 'rgb(46,52,54)'
            self.background_lists_titles = 'rgb(64,64,64)'
            self.background_lists_parts = 'rgb(60,60,60)'
            self.background_lists_books = 'rgb(64,64,64)'
            self.background_nasse_books = 'rgb(64,64,64)'
            self.background_nasse_others = 'rgb(64,64,64)'
            self.background_anawin = 'rgb(64,64,64)'
            self.color_selected = 'rgb(46,52,54)'
            self.background_selected = 'rgb(186,189,182)'
            self.color_hover = 'rgb(46,52,54)'
            self.background_hover = 'rgb(186,189,182)'
            self.color_searched = 'rgb(186,189,182)'
            self.background_searched = 'rgb(0,0,0)'
        elif asm_config.getn('theme') == 6:
            self.color_lists_parts = asm_config.getv('color_lists_parts')
            self.color_lists_books = asm_config.getv('color_lists_books')
            self.color_nasse_books = asm_config.getv('color_nasse_books')
            self.color_nasse_others = asm_config.getv('color_nasse_others')
            self.color_anawin = asm_config.getv('color_anawin')
            self.color_lists_titles = asm_config.getv('color_lists_titles')
            self.color_quran= asm_config.getv('color_quran')
            self.background_quran= asm_config.getv('background_quran') 
            self.background_lists_titles = asm_config.getv('background_lists_titles') 
            self.background_lists_parts = asm_config.getv('background_lists_parts') 
            self.background_lists_books = asm_config.getv('background_lists_books')
            self.background_nasse_books = asm_config.getv('background_nasse_books')
            self.background_nasse_others = asm_config.getv('background_nasse_others')
            self.background_anawin = asm_config.getv('background_anawin')
            self.color_selected = asm_config.getv('color_selected')
            self.background_selected = asm_config.getv('background_selected')
            self.color_hover = asm_config.getv('color_hover')
            self.background_hover = asm_config.getv('background_hover')
            self.color_searched = asm_config.getv('color_searched')
            self.background_searched = asm_config.getv('background_searched')
        
    
    def __init__(self, parent):
        self.parent = parent
        self.refresh()
        
    def refresh(self, *a):
        self.apply_preference()
        szfont, fmfont = asm_customs.split_font(self.font_window)
        data = '''
        * {
        font-family: "'''+fmfont+'''";
        font-size: '''+szfont+'''px;}'''
        screen = self.parent.get_screen()
        css_provider = Gtk.CssProvider()
        context = self.parent.get_style_context()
        css_provider.load_from_data(data.encode('utf8'))
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)