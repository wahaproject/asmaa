# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from gi.repository import Gtk, Pango
import Asmaa.asm_araby as asm_araby
import Asmaa.asm_customs as asm_customs
from Asmaa.asm_contacts import AuthorDB

# class نافذة المؤلفين---------------------------------------------------------    

class Author(Gtk.HPaned):
    
    def visible_cb(self, model, itr, data):
        if len(self.theword) == 0: return
        if asm_araby.fuzzy(self.theword[0]) in asm_araby.fuzzy(model.get_value(itr, 2)):
            return True
        else: return False
    
    def search_on_active(self, text):
        return
    
    def search_on_page(self, text):
        self.theword = [text]
        self.modelfilter.refilter()
    
    def show_author(self, *a):
        model, i = self.sel_author.get_selected()
        if i:
            id_auth = model.get_value(i,0)
            auth = self.db.info_auth(id_auth)[2]
            if auth == '': auth = self.db.info_auth(id_auth)[3]
            self.view_author_bfr.set_text(auth)

#    def near_page(self, v):
#        self.size_font += v
#        self.view_author.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
    
    def change_font(self, *a):
        self.view_author_tag.set_property('foreground', self.parent.theme.color_tit)
        self.view_author_tag.set_property('font', self.parent.theme.font_tit)
    
    def __init__(self, parent):
        self.parent = parent
        self.db = AuthorDB()
        #self.size_font = int(self.parent.theme.font_nass[-2:])
        Gtk.HPaned.__init__(self)
        self.set_border_width(3)
        
        self.tree_author = asm_customs.TreeIndex()
        self.sel_author = self.tree_author.get_selection()
        cell = Gtk.CellRendererText()
        cell.set_property("ellipsize", Pango.EllipsizeMode.END)
        kal = Gtk.TreeViewColumn('المؤلفين', cell, text=1)
        self.tree_author.append_column(kal)
        self.store_author = Gtk.TreeStore(int, str, str)
        authors = self.db.all_author()
        self.modelfilter = self.store_author.filter_new()
        self.names_list = []
        for a in authors:
            self.store_author.append(None, a)
            self.names_list.append(a[2])
        self.theword = self.names_list[:]
        self.modelfilter.set_visible_func(self.visible_cb, self.theword) 
        self.tree_author.set_model(self.modelfilter)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_author)
        self.tree_author.connect("cursor-changed", self.show_author)
        self.pack1(scroll, True, True)
        
        self.view_author = asm_customs.ViewClass()
        self.view_author_bfr = self.view_author.get_buffer()
        self.view_author_tag = self.view_author_bfr.create_tag("author")
        self.change_font()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_author)
        self.pack2(scroll, True, True)
        self.set_position(250)
        
        self.show_all()