# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import Gtk, Gdk, GLib, GObject, Pango
from asm_contacts import bookDB, Othman, listDB
import asm_path
import asm_config
import asm_araby
import asm_popup
import asm_customs
from os.path import basename
import re

# class صفحة الكتب المفتوحة-----------------------------------------------------------------------

class ViewerBooks(Gtk.Notebook):
    
    # a التصفح--------------------------------------------
    
    def convert_browse(self, *a):
        for n in range(self.get_n_pages()):
            ch = self.get_nth_page(n)
            ch.convert_browse()
        
    def first_page(self, *a):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.first_page()
    
    def previous_page(self, *a):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.previous_page()
    
    def next_page(self, *a):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.next_page()
    
    def last_page(self, *a):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.last_page()
        
    def back_to_old(self, *a):
        n = self.get_current_page()
        ch = self.get_nth_page(n) 
        ch.back_to_old()
        
    def advance_to_new(self, *a):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.advance_to_new()
    
    def hide_index(self, *a):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        if ch.hp.get_position() <= 1:
            ch.hp.set_position(200)
        else: ch.hp.set_position(1)
    
    def search_on_page(self, text):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.search_on_page(text)
    
    def search_on_active(self, text):
        n = self.get_current_page()
        ch = self.get_nth_page(n)
        ch.search_on_active(text)
    
    def set_tashkil(self, *a):
        for n in range(self.get_n_pages()):
            ch = self.get_nth_page(n)
            ch.set_tashkil()
    
    def __init__(self, parent):
        self.session = [[], None]
        Gtk.Notebook.__init__(self)
#        self.set_border_width(5)
        self.set_scrollable(True)
        self.parent = parent
        def add(widget, n, d):
            try: self.session[0].append(n.id_book)
            except: pass
        self.connect("page-added", add)
        def rmv(widget, n, d):
            try: self.session[0].remove(n.id_book)
            except: pass
            if self.get_n_pages() == 0:
                self.parent.notebook.set_current_page(0)
                if self.parent.notebook.get_current_page() == 1: 
                    self.parent.opened.remove(1)
        self.connect("page-removed", rmv)
        def sth(widget, n, d):
            self.session[-1] = d
        self.connect("switch-page", sth)
        self.show_all()    

# class  الكتاب المفتوح-----------------------------------------------------------------------

class OpenBook(Gtk.VBox):
    
    def __init__(self, parent, book, id_book):
        Gtk.VBox.__init__(self, False, 3)
        self.db_list = listDB()
        self.parent = parent
        self.othman = Othman()
        self.id_book = id_book
        self.book = book
        self.nm_book = basename(book)[:-4]
        self.db = bookDB(book, id_book)
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.current_id = 1
        self.opened_new = []
        self.opened_old = []
        self.build()
    
    def set_tashkil(self, *a):
        self.show_page(self.all_in_page[1])
        if asm_config.getn('tashkil') == 0: now_text = asm_araby.stripHarakat(self.all_in_page[2])
        else: now_text = self.all_in_page[2]
        ch = self.stack.get_visible_child_name()
        if ch == "n1": 
            self.view_nasse_bfr1.set_text(now_text)
            self.view_nasse_bfr1.insert(self.view_nasse_bfr1.get_end_iter(), " \n")
        else:
            self.view_nasse_bfr2.set_text(now_text)
            self.view_nasse_bfr2.insert(self.view_nasse_bfr2.get_end_iter(), " \n")
    
    def show_bitaka(self, *a):
        box = Gtk.Box(spacing=5,orientation=Gtk.Orientation.VERTICAL)
        bitaka_book = self.db.info_book()[3]
        info_book = self.db.info_book()[4]
        dlg = Gtk.Dialog(parent=self.parent)
        dlg.set_icon_name("asmaa")
        dlg.set_default_size(450, 300)
        area = dlg.get_content_area()
        area.set_spacing(6)
        
        hb_bar = Gtk.HeaderBar()
        hb_bar.set_show_close_button(True)
        dlg.set_titlebar(hb_bar)
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        hb_bar.set_custom_title(stack_switcher)

        self.view_info = asm_customs.ViewClass()
        self.view_info.set_name('View')
        self.view_info_bfr = self.view_info.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_info)
        stack.add_titled(scroll, 'n1',' بطاقة')
        self.view_info_bfr.set_text(bitaka_book)
        
        self.view_info1 = asm_customs.ViewClass()
        self.view_info1.set_name('View')
        self.view_info_bfr1 = self.view_info1.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_info1)
        stack.add_titled(scroll, 'n2', 'نبذة')
        self.view_info_bfr1.set_text(info_book)
        #-----------------------------------------
        ls2 = [self.view_info, self.view_info1]
        for a in ls2:
            szfont, fmfont = asm_customs.split_font(self.parent.theme.font_nasse_others)
            data = '''
            * {
            font-family: "'''+fmfont+'''";
            font-size: '''+szfont+'''px;
            color: '''+asm_customs.rgb(self.parent.theme.color_nasse_others)+''';
            background-color: '''+asm_customs.rgb(self.parent.theme.background_nasse_others)+''';
            }
            #View text selection, #View:selected  {
            color: '''+asm_customs.rgb(self.parent.theme.color_selected)+''';
            background-color: '''+asm_customs.rgb(self.parent.theme.background_selected)+''';
            }
            '''
            css_provider = Gtk.CssProvider()
            context = a.get_style_context()
            css_provider.load_from_data(data.encode('utf8'))
            context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        box.pack_start(stack, True, True, 0)
        area.pack_start(box, True, True, 0)
        dlg.show_all()
    
    def change_font(self, *a):
        ls0 = [self.tree_index, self.tree_search]
        for a in ls0:
            szfont, fmfont = asm_customs.split_font(self.parent.theme.font_lists_titles)
            data = '''
            * {
            font-family: "'''+fmfont+'''";
            font-size: '''+szfont+'''px;
            }
            #Tree:selected {
            color: '''+asm_customs.rgb(self.parent.theme.color_selected)+''';
            background-color: '''+asm_customs.rgb(self.parent.theme.background_selected)+''';
            }
            #Tree:hover {
            color: '''+asm_customs.rgb(self.parent.theme.color_hover)+''';
            background-color: '''+asm_customs.rgb(self.parent.theme.background_hover)+''';
            }
            #Tree {
            color: '''+asm_customs.rgb(self.parent.theme.color_lists_titles)+''';
            background-color: '''+asm_customs.rgb(self.parent.theme.background_lists_titles)+''';
            }'''
            css_provider = Gtk.CssProvider()
            context = a.get_style_context()
            css_provider.load_from_data(data.encode('utf8'))
            context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        #-----------------------------------------
        ls1 = [self.view_nasse1, self.view_nasse2]
        for a in ls1:
            szfont, fmfont = asm_customs.split_font(self.parent.theme.font_nasse_books)
            data = '''
            * {
            font-family: "'''+fmfont+'''";
            font-size: '''+szfont+'''px;
            color: '''+asm_customs.rgb(self.parent.theme.color_nasse_books)+''';
            background-color: '''+asm_customs.rgb(self.parent.theme.background_nasse_books)+''';
            }
            #View text selection, #View:selected  {
            color: '''+asm_customs.rgb(self.parent.theme.color_selected)+''';
            background-color: '''+asm_customs.rgb(self.parent.theme.background_selected)+''';
            }
            '''
            css_provider = Gtk.CssProvider()
            context = a.get_style_context()
            css_provider.load_from_data(data.encode('utf8'))
            context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        #-----------------------------------------------
        self.view_title_tag1.set_property('foreground', self.parent.theme.color_anawin)
        self.view_quran_tag1.set_property('foreground', self.parent.theme.color_quran)
        self.view_terms_tag1.set_property('foreground', self.parent.theme.color_anawin)
        self.view_title_tag2.set_property('foreground', self.parent.theme.color_anawin)
        self.view_quran_tag2.set_property('foreground', self.parent.theme.color_quran)
        self.view_terms_tag2.set_property('foreground', self.parent.theme.color_anawin)
        self.view_search_tag1.set_property('foreground', self.parent.theme.color_searched)
        self.view_search_tag2.set_property('foreground', self.parent.theme.color_searched)
        self.view_title_tag1.set_property('font', self.parent.theme.font_anawin)
        self.view_quran_tag1.set_property('font', self.parent.theme.font_quran)
        self.view_title_tag2.set_property('font', self.parent.theme.font_anawin)
        self.view_quran_tag2.set_property('font', self.parent.theme.font_quran)
        self.view_quran_tag2.set_property("paragraph-background", self.parent.theme.background_quran)
        self.view_quran_tag1.set_property("paragraph-background", self.parent.theme.background_quran)
        self.view_search_tag1.set_property('background', self.parent.theme.background_searched)
        self.view_search_tag2.set_property('background', self.parent.theme.background_searched)
        self.view_title_tag1.set_property('background', self.parent.theme.background_anawin)
        self.view_terms_tag1.set_property('background', self.parent.theme.background_anawin)
        self.view_title_tag2.set_property('background', self.parent.theme.background_anawin)
        self.view_terms_tag2.set_property('background', self.parent.theme.background_anawin)
    
    def search_on_active(self, text):
        if text == '': return
        self.store_search.clear()
        self.scroll_index.hide()
        self.scroll_search.show_all()
        phrase = '''fuzzy(nass) LIKE ? ESCAPE "|"'''
        text = asm_araby.fuzzy(text)
        self.search_tokens = asm_araby.tokenize_search(text)
        phrase2 = list(map(lambda phrase: '%'+phrase.replace('|','||').replace('%','|%')+'%', self.search_tokens))
        if len(phrase2) < 1: return []
        condition = ' AND '.join([phrase]*len(phrase2))
        self.db.search(text, self.store_search, condition, phrase2)
        if len(self.store_search) == 0:
            self.hide_search()
            asm_customs.erro(self.parent, 'لا يوجد نتائج')
            return
        self.hp.set_position(200)
        
    def hide_search(self, *a):
        self.scroll_index.show_all()
        self.scroll_search.hide()
        if len(self.list_index) > 1:
            self.hp.set_position(200)
        else:
            self.hp.set_position(1)
        self.entry_index.set_text('')
        
    def search_on_page(self, text):
        self.show_page(self.all_in_page[1])
        self.search_now(text)
        
    def search_now(self, text):
        search_tokens1 = []
        search_tokens2 = []
        star_iter1 = self.view_nasse_bfr1.get_start_iter()
        end_iter1 = self.view_nasse_bfr1.get_end_iter()
        star_iter2 = self.view_nasse_bfr2.get_start_iter()
        end_iter2 = self.view_nasse_bfr2.get_end_iter()
        self.view_nasse_bfr1.remove_tag_by_name("search1", star_iter1, end_iter1)
        self.view_nasse_bfr2.remove_tag_by_name("search2", star_iter2, end_iter2)
        nasse1 = self.view_nasse_bfr1.get_text(star_iter1, end_iter1, True)
        nasse2 = self.view_nasse_bfr2.get_text(star_iter2, end_iter2, True)
        if text == '': 
            return
        else:
            text = text.strip()
            ls_term = asm_araby.fuzzy(text).split(' ')
        for text in ls_term:
            if len(text) == 1 or text == "ال": continue
            new_term = ''
            for l in text:
                new_term += '({}(\u0651)?([\u064b\u064c\u064d\u064e\u064f\u0650\u0652])?)'.format(l, )
            new_term = new_term.replace('ا', '[اأإؤءئى]')
            new_term = new_term.replace('ه', '[هة]')
            re_term = re.compile('({})'.format(new_term,))
            r_findall1 = re_term.findall(nasse1)
            r_findall2 = re_term.findall(nasse2)
            for r in r_findall1:
                if r[0] not in search_tokens1: search_tokens1.append(r[0])
            for r in r_findall2:
                if r[0] not in search_tokens2: search_tokens2.append(r[0])
        asm_customs.with_tag(self.view_nasse_bfr1, self.view_search_tag1, search_tokens1, 1, self.view_nasse1)
        asm_customs.with_tag(self.view_nasse_bfr2, self.view_search_tag2, search_tokens2, 1, self.view_nasse2)


    # a التصفح--------------------------------------------

    def index_highlight(self, model, path, i, page_id):
        pid = model.get(i,0)[0]
        if pid == page_id: 
            self.tree_index.expand_to_path(path)
            self.tree_index.scroll_to_cell(path)
            self.sel_index.select_path(path)
            return True 
        else:
            return False

    def first_page(self, *a):
        self.stack.set_transition_type(self.style_browse_prev)
        if self.db.first_page() == self.all_in_page[1]: return
        self.show_page(self.db.first_page())
        id_page = self.all_in_page[1]
        try: self.store_index.foreach(self.index_highlight, id_page)
        except: pass
        ch = self.stack.get_visible_child_name()
        if ch == "n1": self.stack.set_visible_child_name("n2")
        else: self.stack.set_visible_child_name("n1")
        GObject.timeout_add(200, self.reset_event)
    
    def previous_page(self, *a):
        self.stack.set_transition_type(self.style_browse_prev)
        if self.db.previous_page(self.current_id) == self.all_in_page[1]: return
        self.show_page(self.db.previous_page(self.current_id))
        id_page = self.all_in_page[1]
        try: self.store_index.foreach(self.index_highlight, id_page)
        except: pass
        ch = self.stack.get_visible_child_name()
        if ch == "n1": self.stack.set_visible_child_name("n2")
        else: self.stack.set_visible_child_name("n1")
        GObject.timeout_add(200, self.reset_event)
    
    def next_page(self, *a):
        self.stack.set_transition_type(self.style_browse_next)
        if self.db.next_page(self.current_id) == self.all_in_page[1]: return
        self.show_page(self.db.next_page(self.current_id))
        id_page = self.all_in_page[1]
        try: self.store_index.foreach(self.index_highlight, id_page)
        except: pass
        ch = self.stack.get_visible_child_name()
        if ch == "n1": self.stack.set_visible_child_name("n2")
        else: self.stack.set_visible_child_name("n1")
        GObject.timeout_add(200, self.reset_event)
    
    def last_page(self, *a):
        self.stack.set_transition_type(self.style_browse_next)
        if self.db.last_page() == self.all_in_page[1]: return
        self.show_page(self.db.last_page())
        id_page = self.all_in_page[1]
        try: self.store_index.foreach(self.index_highlight, id_page)
        except: pass
        ch = self.stack.get_visible_child_name()
        if ch == "n1": self.stack.set_visible_child_name("n2")
        else: self.stack.set_visible_child_name("n1")
        GObject.timeout_add(200, self.reset_event)
    
    def back_to_old(self, *a):
        if len(self.opened_old) == 1: return
        n = self.opened_old.pop()
        self.stack.set_transition_type(self.style_browse_prev)
        self.show_page(self.opened_old[-1])
        ch = self.stack.get_visible_child_name()
        if ch == "n1": self.stack.set_visible_child_name("n2")
        else: self.stack.set_visible_child_name("n1")
        self.opened_new.append(n)
        
    def advance_to_new(self, *a):
        if len(self.opened_new) == 0: return
        n = self.opened_new.pop()
        self.stack.set_transition_type(self.style_browse_prev)
        self.show_page(n)
        ch = self.stack.get_visible_child_name()
        if ch == "n1": self.stack.set_visible_child_name("n2")
        else: self.stack.set_visible_child_name("n1")
        if n != self.opened_old[-1]: self.opened_old.append(n)
    
    def set_index(self, *a):
        self.store_index.clear()
        self.list_index = self.db.index_book()
        iters = [None]
        last_iter = None
        last_level = 0
        last_id = self.db_list.get_last(self.id_book)
        if last_id == None or last_id[0] == 0: 
            self.show_page(self.db.first_page()) 
        else:
            self.show_page(last_id[0]) 
        self.stack.set_visible_child_name("n2")
        #-----------------------------------
        if len(self.list_index) > 1:
            self.hp.set_position(200)
        else:
            self.hp.set_position(1)
        v = 0
        for i in self.list_index:
            v += 1
            if v%1000 == 999: 
                while (Gtk.events_pending()): Gtk.main_iteration()
            level = i[3]
            if level > last_level: iters.append(last_iter)
            elif level < last_level:
                for j in range(last_level-level): iters.pop()
            try :
                last_iter = self.store_index.append(iters[-1], [i[1], i[2]])
            except :
                pass
            last_level = level
    
    def ok_index(self, *a):  
        model, i = self.sel_index.get_selected()
        if i:
            p = model.get_path(i)
            if model.iter_has_child(i) :
                if self.tree_index.row_expanded(p):
                    self.tree_index.collapse_row(p)
                else: 
                    self.tree_index.expand_row(p, False)
            id_page = model.get_value(i, 0)
            tit = model.get_value(i, 1)

            if self.current_id < id_page: self.stack.set_transition_type(self.style_browse_next)
            elif self.current_id > id_page: self.stack.set_transition_type(self.style_browse_prev)
            elif self.current_id == id_page: return
            self.show_page(id_page)
            ch = self.stack.get_visible_child_name()
            if ch == "n1": 
                self.stack.set_visible_child_name("n2")
                asm_customs.with_tag(self.view_nasse_bfr1, self.title_select_tag1, [tit,], 0, self.view_nasse1)
            else: 
                self.stack.set_visible_child_name("n1")
                asm_customs.with_tag(self.view_nasse_bfr2, self.title_select_tag2, [tit,], 0, self.view_nasse2)
            GObject.timeout_add(200, self.reset_event)
            
   
    def ok_search(self, *a):  
        model, i = self.sel_search.get_selected()
        if i:
            p = model.get_path(i)
            if model.iter_has_child(i) :
                if self.tree_search.row_expanded(p):
                    self.tree_search.collapse_row(p)
                else: self.tree_search.expand_row(p, False)
            id_page = model.get_value(i, 0)
            
            if self.current_id < id_page: self.stack.set_transition_type(self.style_browse_next)
            elif self.current_id > id_page: self.stack.set_transition_type(self.style_browse_prev)
            elif self.current_id == id_page: return
            self.show_page(id_page)
            ch = self.stack.get_visible_child_name()
            if ch == "n1": 
                self.stack.set_visible_child_name("n2")
            else: 
                self.stack.set_visible_child_name("n1")
    
    def show_page(self, id_page):
        self.all_in_page = self.db.get_text_body(id_page)#rowid, id, text, part, page, hno, sora, aya, na
        if asm_config.getn('tashkil') == 0: now_text = asm_araby.stripHarakat(self.all_in_page[2])
        else: now_text = self.all_in_page[2]
        self.has_commment(id_page)
        titles = self.db.titles_page(self.all_in_page[1])
        ch = self.stack.get_visible_child_name()
        if ch == "n1": 
            self.view_nasse_bfr2.set_text(now_text)
            self.view_nasse_bfr2.insert(self.view_nasse_bfr2.get_end_iter(), " \n")
            try: asm_customs.with_tag(self.view_nasse_bfr2, self.view_title_tag2, titles)
            except: pass 
        else:
            self.view_nasse_bfr1.set_text(now_text)
            self.view_nasse_bfr1.insert(self.view_nasse_bfr1.get_end_iter(), " \n")
            try: asm_customs.with_tag(self.view_nasse_bfr1, self.view_title_tag1, titles)
            except: pass
        self.is_tafsir(self.all_in_page)
        self.current_id = self.all_in_page[0]
        self.ent_page.set_text(str(self.all_in_page[4]))
        self.ent_part.set_text(str(self.all_in_page[3]))
        text = self.parent.entry_search.get_text()
        if len(text) >= 2 and text != "ال": 
            self.search_now(text)
        if len(self.opened_old) == 0: self.opened_old.append(id_page)
        elif id_page != self.opened_old[-1]: self.opened_old.append(id_page)
        self.stack.show_all()
        self.scroll_nasse1.get_vadjustment().set_value(0.0)
        self.scroll_nasse2.get_vadjustment().set_value(0.0)
    
    def reset_event(self, *a):
        self.scroll_nasse1.get_vadjustment().set_lower(True)
        self.scroll_nasse2.get_vadjustment().set_lower(True)
        self.scroll_nasse1.get_vadjustment().set_value(0.0)
        self.scroll_nasse2.get_vadjustment().set_value(0.0)
    
    def scroll_event(self, sc, ev):
        if asm_config.getn('mouse_browse') == 0: return
        vadj = sc.get_vadjustment()
        p = vadj.get_page_size()
        m = vadj.get_upper()-p
        v = vadj.get_value()
        if m == v:
            if self.vadj_page_next == 5:
                self.next_page()
                self.vadj_page_next = 0
            else:
                self.vadj_page_next += 1
        elif v <= 1.0:
            if self.vadj_page_prev == 5:
                if ev.get_scroll_deltas()[2] == -1.0:
                    self.previous_page()
                if ev.get_scroll_deltas()[2] == 1.0:
                    self.next_page()
                self.vadj_page_prev = 0
            else:
                self.vadj_page_prev += 1
        else:
            self.vadj_page_next = 0
            self.vadj_page_prev = 0
    
    def convert_browse(self, *a):
        ls = [1, 2, 5, 10, 15, 20, 30]
        self.stack.set_transition_duration(ls[asm_config.getn('time_browse')]*100)
        GObject.source_remove(self.timeo)
        self.timeo = GLib.timeout_add(100/((asm_config.getn('auto_browse'))*8), self.autoScroll, None)
        if asm_config.getn('style_browse') == 0:
            self.style_browse_next = Gtk.StackTransitionType.NONE
            self.style_browse_prev = Gtk.StackTransitionType.NONE
        elif asm_config.getn('style_browse') == 1:
            self.style_browse_next = Gtk.StackTransitionType.CROSSFADE
            self.style_browse_prev = Gtk.StackTransitionType.CROSSFADE
        elif asm_config.getn('style_browse') == 2:
            self.style_browse_next = Gtk.StackTransitionType.SLIDE_LEFT
            self.style_browse_prev = Gtk.StackTransitionType.SLIDE_RIGHT
        elif asm_config.getn('style_browse') == 3:
            self.style_browse_next = Gtk.StackTransitionType.SLIDE_UP
            self.style_browse_prev = Gtk.StackTransitionType.SLIDE_DOWN 
    
    def has_commment(self, id_page):
        if self.db.show_comment(id_page) != None and self.db.show_comment(id_page) != []:
            img = Gtk.Image.new_from_icon_name('view-paged-symbolic', 2)
        else:
            img = Gtk.Image.new_from_icon_name('document-new-symbolic', 2)
        self.comment_btn.set_image(img)
        self.comment_btn.show_all()
    
    def is_tafsir(self, all_in_page):
        try: sora, aya, na = int(all_in_page[6]), int(all_in_page[7]), all_in_page[8]
        except: sora = 0
        if sora > 0 and sora < 115:
            try: na = int(na)
            except: na = 1
            nasse_quran = ' '.join(self.othman.get_ayat(sora,aya,aya+na))
            ch = self.stack.get_visible_child_name()
            if ch == "n2":
                self.view_nasse_bfr1.insert(self.view_nasse_bfr1.get_start_iter(), " \n")
                self.view_nasse_bfr1.insert_with_tags(self.view_nasse_bfr1.get_start_iter(), 
                                                 nasse_quran, self.view_quran_tag1)
            else:
                self.view_nasse_bfr2.insert(self.view_nasse_bfr2.get_start_iter(), " \n")
                self.view_nasse_bfr2.insert_with_tags(self.view_nasse_bfr2.get_start_iter(), 
                                                 nasse_quran, self.view_quran_tag2)
    
    #aمؤقت-------------------------------
    def dialog_move_to_page(self, *a):
        dlg = Gtk.Dialog(parent=self.parent)
        dlg.set_icon_name("asmaa")
        dlg.set_position(Gtk.WindowPosition.MOUSE)
        dlg.set_title('انتقل إلى صفحة محدّدة')
        parts_all, pages_all = self.db.parts_pages(self.all_in_page[3])
        ent_page = Gtk.Entry()
        lab_page = Gtk.Label(u"عدد الصفحات "+str(pages_all))
        ent_page.set_text(str(self.all_in_page[4]))
        ent_part = Gtk.Entry()
        lab_part = Gtk.Label(u"عدد الأجزاء "+str(parts_all))
        ent_part.set_text(str(self.all_in_page[3]))
        clo = asm_customs.ButtonClass("ألغ")
        clo.connect('clicked',lambda *a: dlg.destroy())
        move = Gtk.Button("انتقل")
        def replace_cb(widget):
            n_page = int(ent_page.get_text())
            n_part = int(ent_part.get_text())
            id_page = self.db.go_to_page(n_part, n_page)
            if id_page == None: 
                for n in range(20):
                    id_page = self.db.go_to_nearer_page(n_part, n_page, n+1)
                    if id_page != None: break
            if id_page == None: 
                asm_customs.erro(self.parent, "لا يمكن الذهاب إلى الصفحة المحددة")
                return
            if self.current_id < id_page[0]: self.stack.set_transition_type(self.style_browse_next)
            elif self.current_id > id_page[0]: self.stack.set_transition_type(self.style_browse_prev)
            elif self.current_id == id_page[0]: return
            self.show_page(id_page[0])
            ch = self.stack.get_visible_child_name()
            if ch == "n1": 
                self.stack.set_visible_child_name("n2")
            else: 
                self.stack.set_visible_child_name("n1")
            dlg.destroy()
        move.connect('clicked', replace_cb)
        ent_page.connect('activate', replace_cb)
        ent_part.connect('activate', replace_cb)
        box = dlg.vbox
        box.set_border_width(5)
        hb = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(ent_page, False, False, 3)
        hb.pack_start(lab_page, False, False, 3)
        box.pack_start(hb, False, False, 3)
        hb = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(ent_part, False, False, 3)
        hb.pack_start(lab_part, False, False, 3)
        box.pack_start(hb, False, False, 3)
        hb = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(move, False, False, 0)
        hb.pack_end(clo, False, False, 0)
        box.pack_end(hb, False, False, 0)
        dlg.show_all()
    
    def move_to_page(self, *a):
        parts_all, pages_all = self.db.parts_pages(self.all_in_page[3])
        self.lab_page_move.set_label("عدد الصفحات "+str(pages_all))
        self.lab_part_move.set_label("عدد الأجزاء "+str(parts_all))
        self.ent_page_move.set_text(str(self.all_in_page[4]))
        self.ent_part_move.set_text(str(self.all_in_page[3]))
    
    def search_entry(self, *a):
        text = asm_araby.fuzzy(self.entry_index.get_text())
        if text == '':
            self.scroll_index.show_all()
            self.scroll_search.hide()
        else:
            self.scroll_index.hide()
            titles = self.db.search_index(text)
            self.store_search.clear()
            c = 1
            for a in titles:
                self.store_search.append([a[0], c, a[1], '', 0, 0, '', 0]) 
                c += 1
            self.scroll_search.show_all()
    
    def autoScroll(self, *a):
        if not self.autoScrolling: return True
        ch = self.stack.get_visible_child_name()
        if ch == "n1":
            vadj = self.scroll_nasse1.get_vadjustment()
        else:
            vadj = self.scroll_nasse2.get_vadjustment()
        m = vadj.get_upper()-vadj.get_page_size()
        n = min(m, vadj.get_value()+0.1)
        if n == m: self.btn_autoScroll.set_active(False)
        vadj.set_value(n)
        return True
    
    def autoScrollCb(self, b, *a):
        self.autoScrolling = b.get_active()
        
    # a تحرير الكتاب المفتوح----------------------------------
    
    def editbk_cb(self, *a):
        if asm_path.can_modify(self.parent):
            msg = asm_customs.sure(self.parent, 'عملية تعديل الكتاب عملية دقيقة،\nأي خطأ قد يؤدي لتلف الكتاب،\nهل تريد الاستمرار؟')
            if msg == Gtk.ResponseType.YES:         
                self.parent.editbook.close_db()
                book = self.db_list.file_book(self.id_book)
                self.parent.editbook.add_book(book, self.id_book, self.all_in_page[1])
                self.parent.notebook.set_current_page(7)
    
    def comment_cb(self, *a):
        if asm_path.can_modify(self.parent):
            # interface--------------------------------------
            box = Gtk.Box(spacing=5,orientation=Gtk.Orientation.VERTICAL)
            dlg = Gtk.Dialog(parent=self.parent)
            dlg.set_icon_name("asmaa")
            dlg.set_default_size(380, 300)
            area = dlg.get_content_area()
            area.set_spacing(6)
            
            hb_bar = Gtk.HeaderBar()
            hb_bar.set_show_close_button(True)
            dlg.set_titlebar(hb_bar)
            hb_bar.set_title('التعليق')
            
            view_comment = Gtk.TextView()
            view_comment_bfr = view_comment.get_buffer()
            scroll = Gtk.ScrolledWindow()
            scroll.set_shadow_type(Gtk.ShadowType.IN)
            scroll.add(view_comment)
            # functions------------------------------------
            id_page = self.all_in_page[1]
            def add_widget():
                dlg.show_all()
                if self.db.show_comment(id_page) != None and self.db.show_comment(id_page) != []:
                    update_btn.show_all()
                    delete_btn.show_all()
                    save_btn.hide()
                    view_comment_bfr.set_text(self.db.show_comment(id_page)[0])
                else:
                    save_btn.show_all()
                    update_btn.hide()
                    delete_btn.hide()
            #-----------------------    
            def save_cb(w):
                comment = view_comment_bfr.get_text(view_comment_bfr.get_start_iter(),
                                view_comment_bfr.get_end_iter(), False)
                if comment == '': return
                self.db.add_comment(id_page, comment)
                add_widget()
                img = Gtk.Image.new_from_icon_name('view-paged-symbolic', 2)
                self.comment_btn.set_image(img)
                self.comment_btn.show_all()
            #------------------------    
            def update_cb(w):
                comment = view_comment_bfr.get_text(view_comment_bfr.get_start_iter(),
                                view_comment_bfr.get_end_iter(), False)
                self.db.update_comment(id_page, comment)
            #-------------------------
            def delete_cb(w):
                self.db.remove_comment(id_page)
                view_comment_bfr.set_text('')
                add_widget()
                img = Gtk.Image.new_from_icon_name('document-new-symbolic', 2)
                self.comment_btn.set_image(img)
                self.comment_btn.show_all()
            #-----------------------------------
            save_btn = asm_customs.ButtonClass("حفظ")
            save_btn.connect('clicked', save_cb)
            update_btn = asm_customs.ButtonClass("حفظ")
            update_btn.connect('clicked', update_cb)
            delete_btn = asm_customs.ButtonClass("حذف")
            delete_btn.connect('clicked', delete_cb)
            hbox = Gtk.Box(spacing=0,orientation=Gtk.Orientation.HORIZONTAL)
            Gtk.StyleContext.add_class(hbox.get_style_context(), "linked")
            hbox.pack_start(update_btn, False, False, 0)
            hbox.pack_start(delete_btn, False, False, 0)
            hb_bar.pack_start(hbox)
            hb_bar.pack_start(save_btn)
            #----------------------------
            box.pack_start(scroll, True, True, 0)
            area.pack_start(box, True, True, 0)
            #dlg.show_all()
            add_widget()
        
    def build(self, *a):
        self.vadj_page_next = 0
        self.vadj_page_prev= 0
        self.hp = Gtk.HPaned()
        self.parent.connect("check-resize", self.convert_browse)
        
        # a الفهرس-----------------------------------
        vbox = Gtk.VBox(False, 0)
        self.tree_index = Gtk.TreeView()
        self.tree_index.set_name('Tree')
        cell = Gtk.CellRendererText()
        cell.set_property("ellipsize", Pango.EllipsizeMode.END)
        kal = Gtk.TreeViewColumn('الفهرس', cell, text=1)
        self.tree_index.append_column(kal)
        self.store_index = Gtk.TreeStore(int, str)
        self.tree_index.set_model(self.store_index)
        self.sel_index = self.tree_index.get_selection()
        self.tree_index.connect("cursor-changed", self.ok_index)
        self.scroll_index = Gtk.ScrolledWindow()
        self.scroll_index.set_shadow_type(Gtk.ShadowType.IN)
        self.scroll_index.add(self.tree_index)
        #self.scroll_index.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.AUTOMATIC)
        self.scroll_index.get_hadjustment().set_value(0.0) 
        vbox.pack_start(self.scroll_index, True, True, 0)
        #----------------------------------------------
        self.tree_search = Gtk.TreeView()
        self.tree_search.set_name('Tree')
        cell = Gtk.CellRendererText()
        raq = Gtk.TreeViewColumn('الرقم', cell, text=1)
        self.tree_search.append_column(raq)
        cell = Gtk.CellRendererText()
        cell.set_property("ellipsize", Pango.EllipsizeMode.END)
        kal = Gtk.TreeViewColumn('أغلق النتائج', cell, text=2)
        kal.set_expand(True)
        kal.set_clickable(True)
        kal.connect('clicked', self.hide_search)
        self.tree_search.append_column(kal)
        self.store_search = Gtk.ListStore(int, int, str, str, int, int, str, int)
        self.tree_search.set_model(self.store_search)
        self.sel_search = self.tree_search.get_selection()
        self.tree_search.connect("cursor-changed", self.ok_search)
        self.scroll_search = Gtk.ScrolledWindow()
        self.scroll_search.set_shadow_type(Gtk.ShadowType.IN)
        self.scroll_search.add(self.tree_search)
        self.scroll_search.get_hadjustment().set_value(0.0) 
        vbox.pack_start(self.scroll_search, True, True, 0)
        
        try: self.entry_index = Gtk.SearchEntry()
        except: self.entry_index = Gtk.Entry()
        self.entry_index.set_placeholder_text('بحث في الفهرس')
        self.entry_index.connect('changed', self.search_entry)
        vbox.pack_start(self.entry_index, False, False, 3)
        self.hp.pack1(vbox, True, True)
        
        # a عارض النص-----------------------------------
        vbox = Gtk.VBox(False, 0)
        self.stack = Gtk.Stack()
        vbox.pack_start(self.stack, True, True, 0)
        #-------------------------------------
        self.view_nasse1 = asm_customs.ViewClass()
        self.view_nasse1.set_name('View')
        self.view_nasse_bfr1 = self.view_nasse1.get_buffer()
        self.view_nasse1.connect_after("populate-popup", asm_popup.populate_popup, self.parent)
        #self.view_nasse1.connect('button-press-event', self.sss)
        self.scroll_nasse1 = Gtk.ScrolledWindow()
        #self.scroll_nasse1.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll_nasse1.set_shadow_type(Gtk.ShadowType.IN)
        self.scroll_nasse1.add(self.view_nasse1)
        self.scroll_event_name1 = self.scroll_nasse1.connect('scroll-event', self.scroll_event)
        self.view_title_tag1 = self.view_nasse_bfr1.create_tag("title1")
        self.view_quran_tag1 = self.view_nasse_bfr1.create_tag("quran1")
        self.view_search_tag1 = self.view_nasse_bfr1.create_tag("search1")
        self.view_terms_tag1 = self.view_nasse_bfr1.create_tag("terms1")
        self.title_select_tag1 = self.view_nasse_bfr1.create_tag("tit_select1")
        self.stack.add_named(self.scroll_nasse1, 'n1')
        #-------------------------------------
        self.view_nasse2 = asm_customs.ViewClass()
        self.view_nasse2.set_name('View')
        self.view_nasse_bfr2 = self.view_nasse2.get_buffer()
        self.view_nasse2.connect_after("populate-popup", asm_popup.populate_popup, self.parent)
        self.scroll_nasse2 = Gtk.ScrolledWindow()
        #self.scroll_nasse2.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll_nasse2.set_shadow_type(Gtk.ShadowType.IN)
        self.scroll_nasse2.add(self.view_nasse2)
        self.scroll_event_name2 = self.scroll_nasse2.connect('scroll-event', self.scroll_event)
        self.view_title_tag2 = self.view_nasse_bfr2.create_tag("title2")
        self.view_quran_tag2 = self.view_nasse_bfr2.create_tag("quran2")
        self.view_search_tag2 = self.view_nasse_bfr2.create_tag("search2")
        self.view_terms_tag2 = self.view_nasse_bfr2.create_tag("terms2")
        self.title_select_tag2 = self.view_nasse_bfr2.create_tag("tit_select2")
        self.stack.add_named(self.scroll_nasse2, 'n2')
        #----------------------------------------
        hbox = Gtk.HBox(False, 3)
        hbox.set_border_width(3)
        hbox.pack_start(Gtk.Label('('), False, False, 0) 
        self.ent_page = Gtk.Label()
        hbox.pack_start(self.ent_page, False, False, 0)
        hbox.pack_start(Gtk.Label('/'), False, False, 0) 
        self.ent_part = Gtk.Label()
        hbox.pack_start(self.ent_part, False, False, 0) 
        hbox.pack_start(Gtk.Label(')'), False, False, 0)
        
        move_btn = Gtk.MenuButton()
        img = Gtk.Image.new_from_icon_name('go-jump-symbolic', 2)
        move_btn.set_image(img)
        self.popover = Gtk.Popover()
        move_btn.set_popover(self.popover)
        self.ent_page_move = Gtk.Entry()
        self.ent_part_move = Gtk.Entry()
        self.lab_page_move = Gtk.Label("عدد الصفحات ")
        self.lab_part_move = Gtk.Label("عدد الأجزاء ")
        move = Gtk.Button("انتقل")
        def replace_cb(widget):
            n_page = int(self.ent_page_move.get_text())
            n_part = int(self.ent_part_move.get_text())
            id_page = self.db.go_to_page(n_part, n_page)
            if id_page == None: 
                for n in range(20):
                    id_page = self.db.go_to_nearer_page(n_part, n_page, n+1)
                    if id_page != None: break
            if id_page == None: 
                asm_customs.erro(self.parent, "لا يمكن الذهاب إلى الصفحة المحددة")
                return
            if self.current_id < id_page[0]: self.stack.set_transition_type(self.style_browse_next)
            elif self.current_id > id_page[0]: self.stack.set_transition_type(self.style_browse_prev)
            elif self.current_id == id_page[0]: return
            self.show_page(id_page[0])
            ch = self.stack.get_visible_child_name()
            if ch == "n1": 
                self.stack.set_visible_child_name("n2")
            else: 
                self.stack.set_visible_child_name("n1")
            self.popover.hide()
        move.connect('clicked', replace_cb)
        self.ent_page_move.connect('activate', replace_cb)
        self.ent_part_move.connect('activate', replace_cb)
        box = Gtk.Box(spacing=5,orientation=Gtk.Orientation.VERTICAL)
        box.set_border_width(5)
        hb = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(self.ent_page_move, False, False, 3)
        hb.pack_start(self.lab_page_move, False, False, 3)
        box.pack_start(hb, False, False, 3)
        hb = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(self.ent_part_move, False, False, 3)
        hb.pack_start(self.lab_part_move, False, False, 3)
        box.pack_start(hb, False, False, 3)
        hb = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(move, False, False, 0)
        box.pack_end(hb, False, False, 0)
        move_btn.connect("clicked", self.move_to_page)
        box.show_all()
        self.popover.add(box)
        move_btn.set_tooltip_text('الانتقال إلى الصفحة المحددة')
        hbox.pack_start(move_btn,False,False,10)

        btnbox_action = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(btnbox_action.get_style_context(), "linked")
        
        self.comment_btn = Gtk.Button() 
        self.comment_btn.set_tooltip_text("أظهر التعليق")
        self.comment_btn.connect('clicked', self.comment_cb)
        btnbox_action.pack_start(self.comment_btn, False, False, 0)
        vbox.pack_start(hbox, False, False, 0)
        self.btn_autoScroll = Gtk.ToggleButton()
        img = Gtk.Image.new_from_icon_name('media-seek-forward-symbolic-rtl', 2)
        self.btn_autoScroll.add(img)
        self.btn_autoScroll.set_tooltip_text("استعراض آلي")
        btnbox_action.pack_start(self.btn_autoScroll, False, False, 0 )
        hbox.pack_start(btnbox_action, False, False, 0 )
        self.autoScrolling = False
        self.btn_autoScroll.connect("clicked", self.autoScrollCb)
        self.timeo = GLib.timeout_add(100/((asm_config.getn('auto_browse'))*8), self.autoScroll, None)
        
        btnbox_info = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(btnbox_info.get_style_context(), "linked")
        
        bitaka = Gtk.Button()
        bitaka.set_tooltip_text("بطاقة عن الكتاب")
        bitaka.connect('clicked', self.show_bitaka)
        img = Gtk.Image.new_from_icon_name('dialog-information-symbolic', 2)
        bitaka.set_image(img)
        btnbox_info.pack_start(bitaka, False, False, 0 ) 
        edit_book = Gtk.Button()
        edit_book.set_tooltip_text("تحرير الكتاب الحاليّ")
        edit_book.connect('clicked', self.editbk_cb)
        img = Gtk.Image.new_from_icon_name('text-editor-symbolic', 2)
        edit_book.set_image(img)
        btnbox_info.pack_start(edit_book, False, False, 0 ) 
        hbox.pack_end(btnbox_info, False, False, 0 ) 
        
        self.convert_browse()
        self.hp.pack2(vbox, True, False)
        self.pack_start(self.hp, True, True, 0)
        self.show_all()
        self.scroll_search.hide()
        self.change_font()