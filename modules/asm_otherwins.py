# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from asm_dict import Explanatory
from asm_author import Author
from asm_tarjama import Tarjama
from gi.repository import Gtk


class OtherWins(Gtk.Notebook):

    
    def search_on_page(self, text):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.search_on_page(text)
    
    def search_on_active(self, text):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.search_on_active(text)
    
    def __init__(self, parent):
        Gtk.Notebook.__init__(self)
        self.parent = parent
        lab = Gtk.Label('مختار الصحاح')
        lab.set_size_request(150, -1)
        self.dictpage = Explanatory(self.parent)
        self.append_page(self.dictpage, lab)
        lab = Gtk.Label('رواة التهذيبين')
        lab.set_size_request(150, -1)
        self.tarjamapage = Tarjama(self.parent)
        self.append_page(self.tarjamapage, lab)
        lab = Gtk.Label('تراجم المؤلفين')
        lab.set_size_request(150, -1)
        self.authorpage = Author(self.parent)
        self.append_page(self.authorpage, lab)
        def switch(widget, page, n):
            ss = [u"بحث عن كلمة",u"بحث عن راوٍ",u"بحث عن مؤلف"]
            text = ss[n]
            self.parent.entry_search.set_placeholder_text(text)
        self.connect("switch-page", switch)
        self.show_all() 