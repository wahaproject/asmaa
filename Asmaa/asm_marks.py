# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from gi.repository import Gtk
from Asmaa.asm_viewer import OpenBook
from Asmaa.asm_tablabel import TabLabel
import Asmaa.asm_config as asm_config
import Asmaa.asm_customs as asm_customs
from Asmaa.asm_contacts import listDB

class SavedMarks(Gtk.Dialog):
    
    def ok_m(self,*a):
        (model, i) = self.tree_sav.get_selection().get_selected()
        if i:
            self.destroy()
            id_page = model.get_value(i,0)
            id_book = model.get_value(i,2)
            book = listDB().file_book(id_book)
            nm_book = model.get_value(i,1)
            n = self.parent.viewerbook.get_n_pages()
            for s in range(n):
                ch = self.parent.viewerbook.get_nth_page(s)
                if self.parent.viewerbook.get_tab_label(ch).nm == nm_book:
                    self.parent.viewerbook.set_current_page(s)
                    self.parent.notebook.set_current_page(1)
                    return
            sr = OpenBook(self.parent, book, id_book)
            sr.show_page(id_page)
            self.parent.viewerbook.append_page(sr,TabLabel(sr, nm_book))
            self.parent.viewerbook.set_current_page(-1)
            self.parent.notebook.set_current_page(1)
            sr.set_index()
    
    def remove_iter(self, *a):
        (model, i) = self.tree_sav.get_selection().get_selected()
        if i:
            id_poem = model.get_value(i,0)
            for a in self.list_marks:
                if a[0] == id_poem :
                    s = self.list_marks.index(a)
                    self.list_marks.pop(s)
                    model.remove(i)
                    marks = repr(self.list_marks)
                    asm_config.setv('marks', marks)
    
    def remove_iters(self, *a):
        asm_config.setv('marks', '[]')
        self.list_marks = []
        self.store_sav.clear()
    
    def __init__(self, parent):
        self.parent = parent
        self.list_marks = eval(asm_config.getv('marks'))
        Gtk.Dialog.__init__(self, parent=self.parent)
        self.set_icon_name("asmaa")
        
        hb_bar = Gtk.HeaderBar()
        hb_bar.set_show_close_button(True)
        self.set_titlebar(hb_bar)
        hb_bar.set_title('المواضع المحفوظة')
        self.set_default_size(350, 300)
        box = self.vbox
        box.set_spacing(3)
        self.store_sav = Gtk.ListStore(int, str, int)
        for a in self.list_marks:
            self.store_sav.append(a)
        self.tree_sav = asm_customs.TreeIndex()
        self.tree_sav.connect("row-activated", self.ok_m)
        column = Gtk.TreeViewColumn('الكتاب',Gtk.CellRendererText(),text = 1)
        self.tree_sav.append_column(column)
        column = Gtk.TreeViewColumn('الموضع',Gtk.CellRendererText(),text = 0)
        self.tree_sav.append_column(column)
        self.tree_sav.set_model(self.store_sav)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_sav)
        
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(hbox.get_style_context(), "linked")
        remove = asm_customs.ButtonClass("حذف")
        remove.connect('clicked', self.remove_iter)
        hbox.pack_start(remove, False, False, 0)
        remove_all = asm_customs.ButtonClass("مسح")
        remove_all.connect('clicked', self.remove_iters)
        hbox.pack_start(remove_all, False, False, 0)
        hb_bar.pack_start(hbox)
        box.pack_start(scroll, True, True, 0)
        self.show_all()