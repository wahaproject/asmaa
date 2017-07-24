# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from gi.repository import Gtk
import asm_stemming
import asm_araby
import asm_customs
from asm_contacts import DictDB

# class نافذة المعجم---------------------------------------------------------    

class Explanatory(Gtk.HBox):
    
    def show_charh(self, *a):
        model, i = self.sel_dict.get_selected()
        if i:
            p = model.get_path(i)
            if model.iter_has_child(i) :
                if self.tree_dict.row_expanded(p):
                    self.tree_dict.collapse_row(p)
                else: self.tree_dict.expand_row(p, False) 
            else:
                term = model.get_value(i,0)
                charh = self.mydict.show_charh(term)
                self.view_dict_bfr.set_text(charh[0][0]) 
    
    def search_on_page(self, text):
        self.show_charh()
        search_tokens = []
        nasse = self.view_dict_bfr.get_text(self.view_dict_bfr.get_start_iter(), 
                                            self.view_dict_bfr.get_end_iter(),True).split()
        if text == u'': 
            for a in self.all_term:
                txt = asm_araby.fuzzy(a)
                for term in nasse: 
                    if txt in asm_araby.fuzzy(term):
                        search_tokens.append(term)
        else:
            txt = asm_araby.fuzzy(text)
            for term in nasse: 
                if txt in asm_araby.fuzzy(term):
                    search_tokens.append(term)
        asm_customs.with_tag(self.view_dict_bfr, self.search_tag, search_tokens)
    
    def search_on_active(self, text):
        if text == u'': return
        elif len(text) < 3: 
            asm_customs.erro(self.parent, 'أدخل كلمة بها أكثر من حرفين للبحث عنها')
            return
        all_root, all_term = asm_stemming.get_root(u''+text)
        self.tree_dict.collapse_all()
        self.store_dict.clear()
        self.view_dict_bfr.set_text('')
        if len(all_root) == 0: asm_customs.erro(self.parent, 'لا يوجد نتيجة'); return
        for text in all_root: 
            self.store_dict.append(None, [text])
        self.all_term = all_term
                
#    def near_page(self, v):
#        self.size_font += v
#        self.view_dict.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
    
    def move_in_page(self, v):
        model, i = self.sel_dict.get_selected()
        if i:
            p = model.get_path(i).get_indices()[0]
            if p+v == -1 or p+v == len(model): return
            i1 = model.get_iter((p+v,))
            self.tree_dict.get_selection().select_iter(i1)
            self.tree_dict.scroll_to_cell((p+v,))
        elif len(self.tree_dict.get_model()) == 0: return
        else:
            i2 = model.get_iter((0,))
            self.tree_dict.get_selection().select_iter(i2)
            self.tree_dict.scroll_to_cell((0,))
        self.show_charh()
    
    def show_index(self, f_letter):
        self.tree_dict.collapse_all()
        self.store_dict.clear()
        self.view_dict_bfr.set_text('')
        all_index = self.mydict.all_index(f_letter)
        if len(all_index) > 0:
            for a in all_index:
                self.store_dict.append(None, [a[0]])
    
    def select_letter(self, btn):
        letter = btn.get_active_text()
        f_letter = letter[0]
        self.show_index(f_letter)
    
    def __init__(self, parent):
        self.parent = parent
        self.mydict = DictDB()
        #self.size_font = int(self.parent.theme.font_text_book[-2:])
        self.all_term = []
        Gtk.HBox.__init__(self, False, 3)
        self.set_border_width(3)
        letters = [u"ألف",u"باء",u'تاء',u'ثاء',u'جيم',u'حاء',u'خاء',u'دال',u'ذال',u'راء',u'زاي',u'سين',u'شين',u'صاد' ,
            u'ضاد',u'طاء',u'ظاء',u'عين',u'غين',u'فاء',u'قاف',u'كاف',u'لام',u'ميم',u'نون',u'هاء',u'واو',u'ياء']
        vbox = Gtk.VBox(False, 3)
        btn_letters = Gtk.ComboBoxText()
        btn_letters.set_wrap_width(5)
        for a in letters:
            btn_letters.append_text(a)
        btn_letters.connect('changed', self.select_letter)
        self.tree_dict = Gtk.TreeView()
        self.tree_dict.set_name('Tree')
        self.sel_dict = self.tree_dict.get_selection()
        cell = Gtk.CellRendererText()
        kal = Gtk.TreeViewColumn('الجذور', cell, text=0)
        self.tree_dict.append_column(kal)
        self.store_dict = Gtk.TreeStore(str)
        self.tree_dict.set_model(self.store_dict)
        scroll = Gtk.ScrolledWindow()
        scroll.set_size_request(150,  -1)
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_dict)
        self.tree_dict.connect("cursor-changed", lambda *a: self.search_on_page(u""))
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(btn_letters, False, False, 0)
        vbox.pack_start(scroll, True, True, 0)
        
        self.view_dict = asm_customs.ViewClass()
        self.view_dict.set_name('View')
        self.view_dict_bfr = self.view_dict.get_buffer()
        self.search_tag = self.view_dict_bfr.create_tag("search")
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_dict)
        self.pack_start(vbox, False, False, 0)
        self.pack_start(scroll, True, True, 0)
        
        self.show_all()
        




