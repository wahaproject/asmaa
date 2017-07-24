# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from gi.repository import Gtk, Pango
import asm_popup
import asm_path
import asm_config
import asm_araby
import asm_customs
from asm_contacts import Othman, listDB, bookDB
from asm_edit_tafsir import ListTafasir
import re

# class نافذة التفسير---------------------------------------------------------    

class Tafsir(Gtk.HBox):
    
    def show_tafsir(self, tafsir, sura, aya):
        self.aya_now = aya
        self.db = bookDB(asm_path.TAFSIR_DB, -1)
        if tafsir != None:
            if tafsir != -1:
                self.db.close_db()
                del self.db
                book = self.listbook.file_book(tafsir)
                self.db = bookDB(book, tafsir)
        id_page = self.db.page_ayat(sura, aya)
        self.show_page(id_page)
    
    def mov_browse(self, id_page):
        self.suras.handler_block(self.change_sura)
        self.ayas.handler_block(self.change_aya)
        self.all_in_page = self.db.get_text_body(id_page)#rowid, id, text, part, page, hno, sora, aya, na
        if self.all_in_page in [None, "", 0] or self.all_in_page[7] in [None, "", 0]: 
            self.suras.set_active(-1)
            self.ayas.set_sensitive(False)
        elif self.notebook.get_current_page() == 0: 
            if self.all_in_page[6] >= 1 and self.suras.get_active() != self.all_in_page[6]-1:
                self.suras.set_active(self.all_in_page[6]-1)
                self.ayas.set_sensitive(True)
                ayat = asm_customs.value_active(self.suras, 2)
                adj = self.ayas.get_adjustment()
                if ayat == None: ayat = 100
                adj.set_upper(ayat)
                adj.set_value(1)
            if self.aya_now in range(self.all_in_page[7], self.all_in_page[7]+self.all_in_page[8]):
                self.ayas.set_value(self.aya_now)
            else: self.ayas.set_value(self.all_in_page[7])
                
        self.suras.handler_unblock(self.change_sura)
        self.ayas.handler_unblock(self.change_aya)
        
    def show_page(self, id_page):
        self.all_in_page = self.db.get_text_body(id_page)#rowid, id, text, part, page, hno, sora, aya, na
        self.current_id = self.all_in_page[0]
        self.part_now = self.all_in_page[3]
        self.page_now = self.all_in_page[4]
        self.view_tafsir_bfr.set_text(self.all_in_page[2])
        text = self.parent.entry_search.get_text()
        if len(text) >= 2 and text != u"ال": 
            self.search_now(text)
        try: sora, aya, na = self.all_in_page[6], self.all_in_page[7], self.all_in_page[8]
        except: sora = 0
        if sora > 0 and sora < 115:
            try: na = int(na)
            except: na = 1
            tafsir_quran = ' '.join(self.othman.get_ayat(sora,aya,aya+na))
            self.view_tafsir_bfr.insert(self.view_tafsir_bfr.get_start_iter(), u" \nـــــــــــــــــــ\n")
            self.view_tafsir_bfr.insert_with_tags(self.view_tafsir_bfr.get_start_iter(), 
                                                  tafsir_quran, self.view_quran_tag)
        # add to list browse
        if len(self.opened_old) == 0: 
            self.opened_old.append([id_page, self.tafsirs.get_active()])
        elif ([id_page, self.tafsirs.get_active()]) != self.opened_old[-1]: 
            self.opened_old.append([id_page, self.tafsirs.get_active()])
        # change n aya and n sura
        self.mov_browse(id_page)
        self.scroll_nasse.get_vadjustment().set_value(0.0)
        
    def ok_result(self, *a):
        model, i = self.sel_search.get_selected()
        if i:
            sura = model.get_value(i,0)
            aya = model.get_value(i,1)
            tafsir = asm_customs.value_active(self.tafsirs1, 0)
            self.show_tafsir(tafsir, sura, aya)
                
    def near_page(self, v):
        self.size_font += v
        self.view_tafsir.override_font(Pango.FontDescription("{}".format(self.size_font,))) 
    
    def select_tafsir(self, *a):
        self.nm_book = asm_customs.value_active(self.tafsirs, 1)
        tafsir = asm_customs.value_active(self.tafsirs, 0)
        sura = asm_customs.value_active(self.suras, 0)
        aya = self.ayas.get_value()
        self.show_tafsir(tafsir, sura, aya)
    
    def select_sura(self, w):
        self.ayas.set_sensitive(True)
        sura = asm_customs.value_active(w, 0)
        ayat = asm_customs.value_active(w, 2)
        adj = self.ayas.get_adjustment()
        adj.set_upper(ayat)
        adj.set_value(1)
        tafsir = asm_customs.value_active(self.tafsirs, 0)
        self.show_tafsir(tafsir, sura, 1)
        
    def select_aya(self, w):
        sura = asm_customs.value_active(self.suras, 0)
        aya = int(w.get_text())
        adj = self.ayas.get_adjustment()
        if aya > adj.get_upper(): aya = adj.get_upper()
        tafsir = asm_customs.value_active(self.tafsirs, 0)
        self.show_tafsir(tafsir, sura, aya)
    
    def first_page(self, *a):
        self.show_page(self.db.first_page())
    
    def previous_page(self, *a):
        self.show_page(self.db.previous_page(self.current_id))
    
    def next_page(self, *a):
        self.show_page(self.db.next_page(self.current_id))
    
    def last_page(self, *a):
        self.show_page(self.db.last_page())
    
    def back_to_old(self, *a):
        if len(self.opened_old) == 1: return
        n = self.opened_old.pop()
        self.tafsirs.set_active(self.opened_old[-1][1])
        self.show_page(self.opened_old[-1][0])
        self.opened_new.append(n)
        
    def advance_to_new(self, *a):
        if len(self.opened_new) == 0: return
        n = self.opened_new.pop()
        self.tafsirs.set_active(n[1])
        self.show_page(n[0])
        if n != self.opened_old[-1]: self.opened_old.append(n)
    
    def search_on_quran(self, *a):
        text = self.search_entry.get_text()
        if len(text) >= 3:
            all_ayat = Othman().search('"'+text+'"')
            self.store_search.clear()
            if len(all_ayat) == 0:
                asm_customs.erro(self.parent, 'لا يوجد نتيجة'); return
            else: 
                for ayat in all_ayat:
                    i_sura = ayat[0]
                    i_ayat = ayat[1]
                    suras_names = Othman().get_suras_names()
                    sura = suras_names[i_sura-1]
                    self.store_search.append(None, [i_sura, i_ayat, sura[1]])
    
    def search_on_active(self, text):
        return
    
    def search_on_page(self, text):
        self.show_page(self.all_in_page[1])
        self.search_now(text)
        
    def search_now(self, text):
        search_tokens = []
        nasse = self.view_tafsir_bfr.get_text(self.view_tafsir_bfr.get_start_iter(), 
                                            self.view_tafsir_bfr.get_end_iter(),True)
        if text == '': 
            return
        else:
            text = text.strip()
            ls_term = asm_araby.fuzzy(text).split(' ')
        for text in ls_term:
            if len(text) == 1 or text == u"ال": continue
            new_term = ''
            for l in text:
                new_term += '({}(\u0651)?([\u064b\u064c\u064d\u064e\u064f\u0650\u0652])?)'.format(l, )
            new_term = new_term.replace('ا', '[اأإؤءئى]')
            new_term = new_term.replace('ه', '[هة]')
            re_term = re.compile('({})'.format(new_term,))
            r_findall = re_term.findall(nasse)
            for r in r_findall:
                if r[0] not in search_tokens: search_tokens.append(r[0])
        asm_customs.with_tag(self.view_tafsir_bfr, self.view_search_tag, search_tokens, 1, self.view_tafsir)
                    
    def change_font(self, *a):
        self.view_quran_tag.set_property('foreground', self.parent.theme.color_quran) 
        self.view_quran_tag.set_property("paragraph-background", self.parent.theme.background_quran)
        self.view_quran_tag.set_property('font', self.parent.theme.font_quran)
        self.view_search_tag.set_property('foreground', self.parent.theme.color_searched)
        self.view_search_tag.set_property('background', self.parent.theme.background_searched)
    
    def load_list(self, *a):
        self.store_tafasir = []
        list_tafsir = eval(asm_config.getv('list_tafsir'))
        if list_tafsir[2] == 0:
            all_tafsir = self.listbook.all_tafsir()
            for a in all_tafsir: 
                self.store_tafasir.append(a)
        elif list_tafsir[2] == 1:
            for a in list_tafsir[1]:
                if self.listbook.tit_book(a) != None and len(self.listbook.tit_book(a)) > 1:
                    self.store_tafasir.append([a, self.listbook.tit_book(a)[1]])
        self.store_tafasir.insert(0, [-1, 'التفسير الميسر'])
        self.n_warp = list_tafsir[0]+1
        
    def refresh_list(self, *a):
        model = self.tafsirs.get_model()
        model1 = self.tafsirs1.get_model()
        model.clear()
        model1.clear()
        list_tafsir = eval(asm_config.getv('list_tafsir'))
        model.append([-1, 'التفسير الميسر', 0])
        model1.append([-1, 'التفسير الميسر', 0])
        for a in list_tafsir[1]:
            model.append([a, self.listbook.tit_book(a)[1], 0])
            model1.append([a, self.listbook.tit_book(a)[1], 0])
        self.tafsirs.set_active(0)
        self.tafsirs1.set_active(0)
        self.tafsirs.set_wrap_width(list_tafsir[0]+1)
        self.tafsirs1.set_wrap_width(list_tafsir[0]+1)
        self.tafsirs.show_all()
        self.tafsirs1.show_all()
        
    def show_modif_list_tafsir(self, *a):
        ListTafasir(self.parent)
        return
    
    def __init__(self, parent):
        self.db = None
        self.current_id = 1
        self.part_now = 1
        self.page_now = 1
        self.nm_book = 'التفسير الميسر'
        self.parent = parent
        self.othman = Othman()
        self.listbook = listDB()
        sura_list = self.othman.get_suras_names()
        self.opened_new = []
        self.opened_old = []
        Gtk.HBox.__init__(self, False, 0)
        vbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        
        self.notebook = Gtk.Notebook()
        self.notebook.set_show_tabs(False)
        vb = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        vb.set_border_width(5)
        self.load_list()
        self.tafsirs = asm_customs.combo(self.store_tafasir, 'التفسير')
        self.tafsirs.set_wrap_width(self.n_warp)
        vb.pack_start(self.tafsirs, False, False, 0)
        self.tafsirs.set_active(0)
        
        adj = Gtk.Adjustment(1, 1, 7, 1, 5.0, 0.0)
        self.ayas = Gtk.SpinButton()
        self.ayas.set_adjustment(adj)
        self.ayas.set_value(1.0)
        self.ayas.connect('activate', self.select_aya)
        
        hb, self.suras = asm_customs.combo(sura_list, 'السورة')
        self.suras.set_wrap_width(10)
        vb.pack_start(hb, False, False, 0)
        self.suras.set_active(0)
        
        hb = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        lab = Gtk.Label('الآيــــة')
        self.ayas.set_wrap(True)
        self.ayas.set_size_request(140, -1)
        hb.pack_start(lab, False, False, 0)
        hb.pack_end(self.ayas, False, False, 0)
        vb.pack_start(hb, False, False, 0)
        
        show_search = Gtk.Button('أظهر البحث')
        def show_search_cb(w):
            self.notebook.set_current_page(1)
            self.ok_result()
        show_search.connect('clicked', show_search_cb)
        vb.pack_end(show_search, False, False, 0)
        modif_list_tafsir = Gtk.Button('تعديل قائمة التفاسير')
        modif_list_tafsir.connect('clicked', self.show_modif_list_tafsir)
        vb.pack_end(modif_list_tafsir, False, False, 0)
        self.notebook.append_page(vb, Gtk.Label('تصفح'))
        
        vb = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        vb.set_border_width(5)
        
        self.tafsirs1 = asm_customs.combo(self.store_tafasir, 'التفسير')
        self.tafsirs1.set_wrap_width(self.n_warp)
        vb.pack_start(self.tafsirs1, False, False, 0)
        self.tafsirs1.set_active(0)
        
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text('بحث في القرآن')
        self.search_entry.connect('activate', self.search_on_quran)
        hbox = Gtk.HBox(False, 2)
        hbox.pack_start(self.search_entry, True, True, 0)
        vb.pack_start(hbox, False, False, 0)
        
        self.store_search = Gtk.TreeStore(int, int, str)
        self.tree_search = Gtk.TreeView()
        self.tree_search.set_name('Tree')
        self.tree_search.set_model(self.store_search)
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('السورة', cell, text=2)
        self.tree_search.append_column(column)
        cell = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('الآية', cell, text=1)
        self.tree_search.append_column(column)
        self.sel_search = self.tree_search.get_selection()
        self.tree_search.connect("cursor-changed", self.ok_result)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_search)
        
        show_browse = Gtk.Button('أظهر التصفح')
        def show_browse_cb(w):
            self.notebook.set_current_page(0)
            self.select_tafsir()
        show_browse.connect('clicked', show_browse_cb)
        vb.pack_end(show_browse, False, False, 0)
        
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vb.pack_start(scroll, True, True, 0)
        self.notebook.append_page(vb, Gtk.Label('بحث'))
        vbox.pack_start(self.notebook, True, True, 0)
        self.pack_start(vbox, False, False, 0)
        
        self.view_tafsir = asm_customs.ViewClass()
        self.view_tafsir.set_name('View')
        self.view_tafsir_bfr = self.view_tafsir.get_buffer()
        self.view_tafsir.connect_after("populate-popup", asm_popup.populate_popup, self.parent)
        self.view_quran_tag = self.view_tafsir_bfr.create_tag("quran")
        self.view_search_tag = self.view_tafsir_bfr.create_tag("search")
        self.change_font()
        self.scroll_nasse = Gtk.ScrolledWindow()
        self.scroll_nasse.set_shadow_type(Gtk.ShadowType.IN)
        self.scroll_nasse.add(self.view_tafsir)
        self.pack_start(self.scroll_nasse, True, True, 0)
        
        self.tafsirs.connect('changed', self.select_tafsir)
        self.tafsirs1.connect('changed', self.ok_result)
        self.change_sura = self.suras.connect('changed', self.select_sura)
        self.change_aya = self.ayas.connect('value-changed', self.select_aya)
        self.show_all()
        self.select_aya(self.ayas)




