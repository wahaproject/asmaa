# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from os.path import join
import os, re
from gi.repository import Gtk, GObject, Pango, GLib
import asm_path
import asm_config
import asm_popup
import asm_araby
import asm_customs
from asm_viewer import OpenBook
from asm_tablabel import TabLabel
from asm_contacts import bookDB, Othman, listDB
import pickle
import sqlite3

# class عارض نتائج البحث-------------------------------------------------------------------

class ShowResult(Gtk.VPaned):
   
    def __init__(self, parent):
        self.db = None
        self.db_list = listDB()
        self.text = ""
        self.parent = parent
        self.cursive = False
        self.results_books = []
        self.stop_n = 1
        self.build()
    
    def change_font(self, *a):
        ls0 = [self.tree_results]
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
        #---------------------------------------------------
        ls1 = [self.view_nasse]
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
        #---------------------------------------------------
        self.view_title_tag.set_property('foreground', self.parent.theme.color_anawin)
        self.view_quran_tag.set_property('foreground', self.parent.theme.color_quran)
        self.view_terms_tag.set_property('foreground', self.parent.theme.color_anawin)
        self.view_search_tag.set_property('foreground', self.parent.theme.color_searched)
        self.view_title_tag.set_property('font', self.parent.theme.font_anawin)
        self.view_quran_tag.set_property('font', self.parent.theme.font_quran)
        self.view_title_tag.set_property('background', self.parent.theme.background_anawin)
        self.view_quran_tag.set_property('paragraph-background', self.parent.theme.background_quran)
        self.view_terms_tag.set_property('background', self.parent.theme.background_anawin)
        self.view_search_tag.set_property('background', self.parent.theme.background_searched)
    
    def show_bitaka(self, *a):
        if self.db.info_book() == None:
            text_info = self.nm_book
        else: text_info = self.db.info_book()
        return text_info
    
    def back_to_old(self, *a):
        return
        
    def advance_to_new(self, *a):
        return
    
    def show_result(self, *a):
        model, i = self.sel_result.get_selected()
        if i:
            if self.db != None:
                self.db.close_db()
                del self.db
            id_page = model.get_value(i, 0)
            self.id_book = model.get_value(i, 6)
            self.book = self.db_list.file_book(self.id_book)
            self.nm_book = model.get_value(i, 2)
            self.db = bookDB(self.book, self.id_book)
            self.show_page(id_page)
    
    def search(self, text, dict_perf, dict_field, selected_books):
        s = 0
        self.n_r = 1 # a عدد النتائج
        for book in selected_books:
            if self.stop_n == 0: break
            id_book = book[2]
            nm_book = book[0]
            #if self.db_list.is_indexed(id_book):
            #    self.search_in_index(id_book, text, dict_perf, dict_field, 1000) 
            #else: 
            self.search_in_book(id_book, nm_book, text, dict_perf, dict_field)
            self.progress.set_fraction(float(s)/(float(len(selected_books))))
            s += 1
        self.progress.set_fraction(0.0)
        self.hb_stop.hide()
        if len(self.store_results)>0:
            for a in self.store_results:
                self.results_books.append([a[0], a[1], a[2], a[3], a[4], a[5], a[6]])
            output = open(join(asm_path.HOME_DIR, 'searchs', u'آخر بحث.pkl'), 'wb')
            pickle.dump((text,self.results_books), output)
            output.close()
    
    def search_in_index(self, id_book, text, dict_perf, dict_field, limit):
        from asm_indexer import SearchIndexed
        search_in_indexed = SearchIndexed()
        filebook = self.db_list.file_book(id_book)
        db = bookDB(filebook, id_book)
        results = search_in_indexed.search_in_book(id_book, text, dict_perf, dict_field, limit)        
    
    def search_in_book(self, id_book, nm_book, text, dict_perf, dict_field):
        text = asm_araby.fuzzy_plus(text)
        self.text = text
        self.cursive = dict_perf['cursive']
        text = text.replace('"','')
        text = text.replace("'","")
        ls_term = []
        if dict_field['nass']: 
            field = 'nass'
            table = 'pages'
        else: 
            field = 'tit'
            table = 'titles'
        if dict_perf['with_tachkil'] == True: 
            cond = '{} LIKE ?'.format(field,)
        else:
            cond = 'fuzzy({}) LIKE ?'.format(field,)
        if dict_perf['identical'] == True:  pfx, sfx = '% ', ' %'
        else: pfx, sfx = '%', '%'
        if dict_perf['cursive'] == True:
            condition = 'fuzzy({}) LIKE ?'.format(field,)
            ls_term.append(pfx+text+sfx)
        else: 
            for a in text.split(u' '):
                ls_term.append(pfx+a+sfx)
            if dict_perf['one_term'] == True:
                condition = ' OR '.join([cond]*len(ls_term))
            else :
                condition = ' AND '.join([cond]*len(ls_term))
        book = self.db_list.file_book(id_book)
        con = sqlite3.connect(book)
        con.create_function('fuzzy', 1, asm_araby.fuzzy_plus)
        cur = con.cursor()
        if table == 'pages': len_book = len(cur.execute('SELECT id FROM pages').fetchall())
        else: len_book = len(cur.execute('SELECT id FROM titles').fetchall())
        parts = int(len_book/200)
        remainder = len_book-(200*parts)
        v = 0
        while v in range(parts+1):
            while (Gtk.events_pending()): Gtk.main_iteration()
            p1 = v*200
            p2 = (v+1)*200
            if v < parts:
                cond = 'id BETWEEN {} and {}'.format(p1, p2)
            elif v == parts:
                cond = 'id BETWEEN {} and {}'.format(p1, remainder)
            elif v > parts:
                pass  
            if table == 'pages':
                cur.execute("""SELECT id, part, page FROM pages WHERE {} AND {}""".format(cond, condition), ls_term)
                i_pgs = cur.fetchall()
                for i in i_pgs:
                    j = i[0]
                    try: pg = int(i[2])
                    except: pg = 1
                    try: pr = int(i[1])
                    except: pr = 1
                    cur.execute('SELECT tit FROM titles WHERE id<=?', (j,)) 
                    try: tit = cur.fetchall()[-1][0]
                    except: tit = '......'
                    self.store_results.append([j, self.n_r, nm_book, tit, pr, pg, id_book])
                    self.n_r += 1
                    self.lab_n_result.set_text('عدد النتائج : {}'.format(self.n_r-1, ))
            else:
                cur.execute("""SELECT id, tit FROM titles WHERE {} AND {}""".format(cond, condition), ls_term)
                i_anawins = cur.fetchall()
                for i in i_anawins:
                    self.store_results.append([i[0], self.n_r, nm_book, i[1], 0, 0, id_book])
                    self.n_r += 1
                    self.lab_n_result.set_text('عدد النتائج : {}'.format(self.n_r-1, ))
            v += 1
        cur.close()
        con.close()
   
    def sav_result_cb(self, *a):
        nm = self.sav_result_entry.get_text()
        if nm == u"":
            asm_customs.erro(self.parent, "أدخل الاسم أولا.")
        elif nm in os.listdir(join(asm_path.HOME_DIR, 'searchs')): 
            asm_customs.erro(self.parent, "يوجد بحث محفوظ بنفس الاسم !!")
        else:
            output = open(join(asm_path.HOME_DIR, 'searchs', nm+u'.pkl'), 'wb')
            pickle.dump((self.text, self.results_books), output)
            output.close()
        self.sav_result_entry.set_text("")

    
    def first_page(self, *a):
        if self.tree_results.get_selection().count_selected_rows() == 1:
            self.show_page(self.db.first_page())
    
    def previous_page(self, *a):
        if self.tree_results.get_selection().count_selected_rows() == 1:
            self.show_page(self.db.previous_page(self.current_id))
    
    def next_page(self, *a):
        if self.tree_results.get_selection().count_selected_rows() == 1:
            self.show_page(self.db.next_page(self.current_id))
    
    def last_page(self, *a):
        if self.tree_results.get_selection().count_selected_rows() == 1:
            self.show_page(self.db.last_page())
    
    def show_page(self, id_page):
        self.all_in_page = self.db.get_text_body(id_page)#rowid, id, text, part, page, hno, sora, aya, na
        self.view_nasse_bfr.set_text(self.all_in_page[2])
        titles = self.db.titles_page(self.all_in_page[1])
        asm_customs.with_tag(self.view_nasse_bfr, self.view_title_tag, titles)
        self.is_tafsir(self.all_in_page)
        self.current_id = self.all_in_page[0]
        text = self.parent.entry_search.get_text()
        if len(text) >= 2 and text != u"ال": 
            self.search_now(text)
        self.show_term_search()
        
    def show_term_search(self, *a):
        search_tokens = []
        nasse0 = self.view_nasse_bfr.get_text(self.view_nasse_bfr.get_start_iter(), 
                                            self.view_nasse_bfr.get_end_iter(),True)
        for text in self.text.split(' '):
            new_term = u''
            for l in text:
                new_term += u'({}(\u0651)?([\u064b\u064c\u064d\u064e\u064f\u0650\u0652])?)'.format(l, )
            new_term = new_term.replace(u'ا', u'[اأإؤءئى]')
            new_term = new_term.replace(u'ه', u'[هة]')
            re_term = re.compile(u'({})'.format(new_term,))
            r_findall = re_term.findall(nasse0)
            for r in r_findall:
                try: 
                    if r[0] not in search_tokens: search_tokens.append(r[0])
                except: pass
        asm_customs.with_tag(self.view_nasse_bfr, self.view_search_tag, search_tokens, 1, self.view_nasse)
    
    def is_tafsir(self, all_in_page):
        try: sora, aya, na = all_in_page[6], all_in_page[7], all_in_page[8]
        except: sora = 0
        if sora > 0 and sora < 115:
            try: na = int(na)
            except: na = 1
            nasse_quran = ' '.join(Othman().get_ayat(sora,aya,aya+na))
            self.view_nasse_bfr.insert(self.view_nasse_bfr.get_start_iter(), u" \nـــــــــــــــــــ\n")
            self.view_nasse_bfr.insert_with_tags(self.view_nasse_bfr.get_start_iter(), nasse_quran, self.view_quran_tag)
    
    def search_in_result(self, *a):
        text = self.sav_result_entry.get_text()
        if text == u"":
            asm_customs.erro(self.parent, "أدخل كلمة للبحث أولا.")
            return
        sr = ShowResult(self.parent)
        self.parent.viewerbook.append_page(sr,TabLabel(sr, u'بحث عن :'+text))
        self.parent.viewerbook.set_current_page(-1)
        n = 0
        s = 0
        for a in self.store_results:
            while (Gtk.events_pending()): Gtk.main_iteration()
            n += 1
            if self.stop_n == 0: break
            book = self.db_list.file_book(a[6])
            con = sqlite3.connect(book)
            con.create_function('fuzzy', 1, asm_araby.fuzzy_plus)
            cur = con.cursor()
            cur.execute('SELECT id FROM pages WHERE id=? AND fuzzy(nass) LIKE ?', (a[0], '%'+text+'%'))
            if len(cur.fetchall()) > 0:
                s += 1
                sr.store_results.append([a[0], s, a[2], a[3], a[4], a[5], a[6]])
            sr.progress.set_fraction(float(n)/(float(len(self.store_results))))
            sr.lab_n_result.set_text('عدد النتائج : {}'.format(s, ))
        sr.progress.set_fraction(0.0)
        sr.hb_stop.hide()
        if len(sr.store_results)>0:
            for a in sr.store_results:
                sr.results_books.append([a[0], a[1], a[2], a[3], a[4], a[5], a[6]])
            output = open(join(asm_path.HOME_DIR, 'searchs', u'آخر بحث.pkl'), 'wb')
            pickle.dump((text,sr.results_books), output)
            output.close()

    def open_new_tab(self, *a):
        if self.tree_results.get_selection().count_selected_rows() == 1:
            n = self.parent.viewerbook.get_n_pages()
            for s in range(n):
                ch = self.parent.viewerbook.get_nth_page(s)
                if self.parent.viewerbook.get_tab_label(ch).nm == self.nm_book:
                    self.parent.viewerbook.set_current_page(s)
                    self.parent.notebook.set_current_page(1)
                    return
            sr = OpenBook(self.parent, self.book, self.id_book)
            self.parent.viewerbook.append_page(sr,TabLabel(sr, self.nm_book))
            self.parent.viewerbook.set_current_page(-1)
            self.parent.notebook.set_current_page(1)
            sr.set_index()
            sr.show_page(self.all_in_page[1])
    
    def stop_search(self, *a):
        self.stop_n = 0
        self.hb_stop.hide()
        
    def search_on_active(self, text):
        self.search_on_page(text)
    
    def search_on_page(self, text):
        if self.tree_results.get_selection().count_selected_rows() == 1:
            self.show_page(self.all_in_page[1])
            self.search_now(text)
        
    def search_now(self, text):
        search_tokens = []
        nasse = self.view_nasse_bfr.get_text(self.view_nasse_bfr.get_start_iter(), 
                                            self.view_nasse_bfr.get_end_iter(),True)
        if text == u'': 
            return
        else:
            text = text.strip()
            ls_term = asm_araby.fuzzy(text).split(u' ')
        for text in ls_term:
            if len(text) == 1 or text == u"ال": continue
            new_term = u''
            for l in text:
                new_term += u'({}(\u0651)?([\u064b\u064c\u064d\u064e\u064f\u0650\u0652])?)'.format(l, )
            new_term = new_term.replace(u'ا', u'[اأإؤءئى]')
            new_term = new_term.replace(u'ه', u'[هة]')
            re_term = re.compile(u'({})'.format(new_term,))
            r_findall = re_term.findall(nasse)
            for r in r_findall:
                if r[0] not in search_tokens: search_tokens.append(r[0])
        asm_customs.with_tag(self.view_nasse_bfr, self.view_search_tag, search_tokens, 1, self.view_nasse)
    
    def convert_browse(self, *a):
        return
    
    def build(self, *a):
        Gtk.VPaned.__init__(self)
        vb = Gtk.VBox(False, 0)
        self.view_nasse = asm_customs.ViewClass()
        self.view_nasse.set_name('View')
        self.view_nasse_bfr = self.view_nasse.get_buffer()
        self.view_nasse.connect_after("populate-popup", asm_popup.populate_popup, self.parent)
        self.view_title_tag = self.view_nasse_bfr.create_tag("title")
        self.view_quran_tag = self.view_nasse_bfr.create_tag("quran")
        self.view_search_tag = self.view_nasse_bfr.create_tag("search")
        self.view_terms_tag = self.view_nasse_bfr.create_tag("terms")
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_nasse)
        self.pack1(scroll, True, False)
        hb = Gtk.HBox(False, 7)
        open_in_tab = Gtk.ToolButton(stock_id=Gtk.STOCK_FILE)
        open_in_tab.set_tooltip_text('افتح في لسان مستقل')
        open_in_tab.connect('clicked', self.open_new_tab)
        hb.pack_start(open_in_tab, False, False, 0)
        sav_result_btn = Gtk.ToolButton(stock_id=Gtk.STOCK_SAVE)
        sav_result_btn.set_tooltip_text('حفظ نتائج البحث الحالي باسم')
        hb.pack_start(sav_result_btn, False, False, 0)
        sav_result_btn.connect('clicked', self.sav_result_cb)
        self.sav_result_entry = Gtk.Entry()
        hb.pack_start(self.sav_result_entry, False, False, 0)
        self.search_result_btn = Gtk.ToolButton(stock_id=Gtk.STOCK_FIND)
        self.search_result_btn.set_tooltip_text('بحث في نتائج البحث')
        hb.pack_start(self.search_result_btn, False, False, 0)
        self.search_result_btn.connect('clicked', self.search_in_result)
        self.lab_n_result = Gtk.Label('عدد النتائج : 0')
        hb.pack_start(self.lab_n_result, False, False, 0)
        self.hb_stop = Gtk.HBox(False, 7)
        btn_stop = asm_customs.tool_button(join(asm_path.ICON_DIR, u'stp.png'), 'أوقف عملية البحث', self.stop_search)
        self.hb_stop.pack_start(btn_stop, False, False, 0)
        self.progress = Gtk.ProgressBar()
        self.hb_stop.pack_start(self.progress, True, True, 0)
        hb.pack_start(self.hb_stop, True, True, 0)
        vb.pack_start(hb, False, False, 5)
        
        self.store_results = Gtk.ListStore(int,int,str,str,int,int, int)
        self.tree_results = Gtk.TreeView()
        self.tree_results.set_name('Tree')
        self.tree_results.set_model(self.store_results)
        self.sel_result = self.tree_results.get_selection()
        self.tree_results.connect("cursor-changed", self.show_result)
        self.tree_results.set_grid_lines(Gtk.TreeViewGridLines.HORIZONTAL)
        raq = Gtk.TreeViewColumn('#', Gtk.CellRendererText(), text=1)
        self.tree_results.append_column(raq)
        books = Gtk.TreeViewColumn('الكتاب', Gtk.CellRendererText(), text=2)
        self.tree_results.append_column(books)
        elbab = Gtk.TreeViewColumn('الباب', Gtk.CellRendererText(), text=3)
        self.tree_results.append_column(elbab)
        elbaher = Gtk.TreeViewColumn('الجزء', Gtk.CellRendererText(), text=4)
        self.tree_results.append_column(elbaher)
        elgharadh = Gtk.TreeViewColumn('الصفحة', Gtk.CellRendererText(), text=5)
        self.tree_results.append_column(elgharadh)
        elgharadh.set_expand(True)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_results)
        scroll.set_size_request(-1, 200)
        vb.pack_start(scroll, True, True, 0)
        self.pack2(vb, False, True)
        self.change_font()
        self.show_all()
        
# class نافذة البحث-------------------------------------------------------------------

class Searcher(Gtk.Dialog):
   
    def __init__(self, parent):
        self.parent = parent
        self.db = listDB()
        self.selected_books = []
        self.build()
   
    def load_books(self, *a):
        self.store_books.clear()
        groups = self.db.all_parts()
        for a in groups:
            aa = self.store_books.append(None, [None, a[1], a[0]])
            books = self.db.books_part(a[0])
            for b in books:
                self.store_books.append(aa, [None, b[1], b[0]])
    
    def select_o(self, model, path, i, bool1):
        bool0 = model.get_value(i,0)
        if bool0 != bool1: 
            model.set_value(i,0, bool1)
            self.add_to_listbooks(model, i, bool1)
            return False
    
    def select_all(self, btn):
        if btn.get_title() == u"علّم جميع الكتب":
            self.store_books.foreach(self.select_o, True)
            btn.set_title(u"ألغ تعليم الجميع")
        else:
            self.store_books.foreach(self.select_o, False)
            btn.set_title(u"علّم جميع الكتب")

        
    def select_field(self, btn, *a):
        nm = btn.get_name()
        self.dict_field[nm] = btn.get_active()
        
    def select_field_index(self, btn, *a):
        nm = btn.get_name()
        self.dict_field_index[nm] = btn.get_active()
           
    def select_perf(self, btn):
        nm = btn.get_name()
        self.dict_perf[nm] = btn.get_active()
        
    def select_perf_index(self, btn):
        nm = btn.get_name()
        self.dict_perf_index[nm] = btn.get_active()
    
    def fixed_toggled_field(self, cell, path, model):
        itr = model.get_iter((path),)
        fixed = model.get_value(itr, 0)
        fixed = not fixed
        model.set(itr, 0, fixed)
    
    def fixed_toggled(self, cell, path, model):
        itr = model.get_iter((path),)
        fixed = model.get_value(itr, 0)
        if model.iter_has_child(itr):
            n_iters = self.store_books.iter_n_children(itr)
            d = 0
            while d in range(n_iters):
                iter1 = model.get_iter((int(path),d),)
                fixed1 = model.get_value(iter1, 0)
                fixed1 = not fixed
                model.set(iter1, 0, fixed1)
                self.add_to_listbooks(model, iter1, fixed1)
                d += 1
        fixed = not fixed
        model.set(itr, 0, fixed)
        self.add_to_listbooks(model, itr, fixed)
    
    def add_all_list(self,*a):
        for w in range(len(self.store_fields)):
            if self.store_fields[w][0] == True:
                nm_field = self.store_fields[w][1]
                if nm_field == u"المفضلة":
                    list_fav = listDB().favorite_books()
                    for a in list_fav:
                        if a not in self.selected_books:
                            nm_book = a[1]
                            id_book = a[0]
                            nm_group = listDB().group_book(a[0])
                            self.selected_books.append([nm_book, nm_group, id_book])
                else:
                    store = pickle.load(open(join(asm_path.LIBRARY_DIR, u'fields-search', nm_field+u'.pkl'), "rb"))
                    for a in store:
                        if a not in self.selected_books:
                            nm_book = a[0]
                            nm_group = a[1]
                            id_book = a[2]
                            self.selected_books.append([nm_book, nm_group, id_book])
        
    def add_to_listbooks(self, model, itr, fixed):
        nm_book = model.get_value(itr, 1)
        id_book = model.get_value(itr, 2)
        i = model.iter_parent(itr)
        if i != None: 
            nm_group = model.get_value(i, 1)
            if fixed: 
                self.columntext1.set_title(u"ألغ تعليم الجميع")
                if [nm_book, nm_group, id_book] not in self.selected_books:
                    self.selected_books.append([nm_book, nm_group, id_book])
            else:
                if [nm_book, nm_group, id_book] in self.selected_books:
                    self.selected_books.remove([nm_book, nm_group, id_book])
                if len(self.selected_books) == 0: self.columntext1.set_title(u"علّم جميع الكتب")
    
    def search(self, *a):
        self.add_all_list()
        text = self.entry_search.get_text()
        if text == u'':
            asm_customs.erro(self.parent, 'أدخل النص المراد البحث عنه')
        if self.stack.get_visible_child_name() == "n1":
            asm_config.setv('search', 0)
            if self.selected_books == []:
                asm_customs.erro(self.parent, 'أنت لم تحدد أين ستبحث')
            else:
                try:
                    if len(self.list_terms) == 50: self.list_terms.pop(0)
                    if text in self.list_terms: self.list_terms.remove(text)
                    self.list_terms.append(text)
                    output = open(join(asm_path.HOME_DIR, u'last-terms.pkl'), 'wb')
                    pickle.dump(self.list_terms, output)
                    output.close()
                except: pass
                self.hide()
                self.parent.notebook.set_current_page(1)
                sr = ShowResult(self.parent)
                self.parent.viewerbook.append_page(sr,TabLabel(sr, u'بحث عن :'+text))
                self.parent.viewerbook.set_current_page(-1)
                sr.search(text, self.dict_perf, self.dict_field, self.selected_books)
        else:
            asm_config.setv('search', 1)
    
    # a دوال البحث في قائمة الكتب
    
    def search_in_index(self, model, path, i, my_books):
        txt = model.get(i,1)[0]
        text, model0, path0, i0 = my_books
        if asm_araby.fuzzy(text) in asm_araby.fuzzy(txt) and path.compare(path0) > 0: 
            self.tree_books.expand_to_path(path)
            self.tree_books.scroll_to_cell(path)
            self.sel_books.select_path(path)
            return True 
        else:
            return False
    
    def search_entry_cb(self, *a):
        text = self.ent_search.get_text()
        model = self.store_books
        i = model.get_iter_first()
        path = model.get_path(i)
        try: self.store_books.foreach(self.search_in_index, [text, model, path, i])
        except: pass
    
    def search_cb(self, *a):
        model, i = self.sel_books.get_selected()
        if not i:
            i = model.get_iter_first()
        path = model.get_path(i)
        text = self.ent_search.get_text()
        if text == u'': return
        try: self.store_books.foreach(self.search_in_index, [text, model, path, i])
        except: pass
    
    def save_fields(self, *a):
        if len(self.selected_books) == 0: 
            asm_customs.erro(self.parent, "لا يوجد أي كتاب محدد!")
            return
        nm = self.ent_field.get_text()
        output = open(join(asm_path.LIBRARY_DIR, u'fields-search', nm+u'.pkl'), 'wb')
        pickle.dump(self.selected_books, output)
        output.close()
        self.ent_field.set_text('')
        self.load_fields()
    
    def load_fields(self, *a):
        self.store_fields.clear()
        self.store_fields.append([None, u"المفضلة"])
        for a in os.listdir(join(asm_path.LIBRARY_DIR, u'fields-search')):
            if a[-4:] == u'.pkl':
                a = a.replace(u'.pkl', u'')
                self.store_fields.append([None, a])
    
    def del_history(self, *a):
        self.list_terms = []
        output = open(join(asm_path.HOME_DIR, u'last-terms.pkl'), 'wb')
        pickle.dump(self.list_terms, output)
        output.close()
        self.list_ts.clear()
        asm_customs.info(self.parent, "تمّ مسح الكلمات المبحوث عنها سابقاً")
        
    def build(self, *a):
        Gtk.Dialog.__init__(self, parent=self.parent)
        self.set_border_width(3)
        self.set_icon_name("asmaa")
        area = self.get_content_area()
        area.set_spacing(3)
        
        hb_bar = Gtk.HeaderBar()
        hb_bar.set_show_close_button(True)
        self.set_titlebar(hb_bar)
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(1000)
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)
#        hb_bar.pack_end(stack_switcher)
        vbox1 = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        vbox2 = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        
        self.set_size_request(600,450)
        self.connect('delete-event', lambda w,*a: w.hide() or True)
        #---------------------------------------------------
        hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        self.entry_search = Gtk.SearchEntry()
#        self.entry_search.set_size_request(400,-1)
        try: self.list_terms = pickle.load(open(join(asm_path.HOME_DIR, u'last-terms.pkl'), "rb"))
        except: self.list_terms = []
        completion = Gtk.EntryCompletion()
        self.list_ts = Gtk.ListStore(str)
        for a in self.list_terms:
            self.list_ts.append([a])
        completion.set_model(self.list_ts)
        completion.set_text_column(0)
        self.entry_search.set_completion(completion)
        self.entry_search.set_size_request(500,-1)
        self.entry_search.connect('activate', self.search)
        self.entry_search.set_placeholder_text('أدخل النص المراد البحث عنه')
        self.btn_search = asm_customs.ButtonClass('بحث')
        hb_bar.pack_start(self.btn_search)
        hb_bar.pack_start(self.entry_search)
        self.btn_search.connect('clicked', self.search)
        vbox1.pack_start(hbox, False, False, 0)
        #-------------------------------------------------------
        hbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        vbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        hb = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        self.ent_search = Gtk.SearchEntry()
        self.ent_search.set_placeholder_text('بحث عن كتاب')
        self.ent_search.connect('changed', self.search_entry_cb)
        hb.pack_end(self.ent_search, False, False, 0)
        self.ent_search.connect('activate', self.search_cb)
        vbox.pack_start(hb, False, False, 0)
        hbox.pack_start(vbox, False, False, 0)
        self.store_fields = Gtk.ListStore(GObject.TYPE_BOOLEAN, GObject.TYPE_STRING)
        self.load_fields()
        self.tree_fields = Gtk.TreeView(self.store_fields)
        self.tree_fields.set_rules_hint(True)
        celltext = Gtk.CellRendererText()
        celltext.set_property("ellipsize", Pango.EllipsizeMode.END)
        celltoggle = Gtk.CellRendererToggle()
        celltoggle.set_property('activatable', True)
        columntoggle = Gtk.TreeViewColumn("اختر", celltoggle)
        columntext = Gtk.TreeViewColumn("النطاق", celltext, text = 1 )
        columntext.set_expand(True)
        columntoggle.add_attribute( celltoggle, "active", 0)
        celltoggle.connect('toggled', self.fixed_toggled_field, self.store_fields)
        self.tree_fields.append_column(columntoggle)
        self.tree_fields.append_column(columntext)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_fields)
        vbox.pack_start(scroll,True, True, 0)
        
        self.store_books = Gtk.TreeStore(GObject.TYPE_BOOLEAN, GObject.TYPE_STRING, GObject.TYPE_INT)
        self.load_books()
        self.tree_books = Gtk.TreeView()
        self.tree_books.set_model(self.store_books)
        self.sel_books = self.tree_books.get_selection()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_books)
        scroll.set_size_request(200, -1)
        celltext = Gtk.CellRendererText()
        celltext.set_property("ellipsize", Pango.EllipsizeMode.END)
        celltoggle = Gtk.CellRendererToggle()
        celltoggle.set_property('activatable', True)
        columntoggle = Gtk.TreeViewColumn("ضمّ", celltoggle)
        columntoggle.set_clickable(True)
        columntoggle.connect('clicked', lambda *a:
                             self.tree_books.collapse_all()) 
        self.columntext1 = Gtk.TreeViewColumn("علّم جميع الكتب", celltext, text = 1 )
        self.columntext1.set_clickable(True)
        self.columntext1.connect('clicked', self.select_all) 
        self.columntext1.set_expand(True)
        columntoggle.add_attribute( celltoggle, "active", 0)
        celltoggle.connect('toggled', self.fixed_toggled, self.store_books)
        self.tree_books.append_column(columntoggle)
        self.tree_books.append_column(self.columntext1)
        hbox.pack_start(scroll, True, True, 0)
        vbox1.pack_start(hbox, True, True, 0)
        #-------------------------------------------------------
        expander = Gtk.Expander.new("خيارات متقدمة")
        notebk = Gtk.Notebook()
        expander.add(notebk)
        box = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        box.set_border_width(7)
        notebk.append_page(box, Gtk.Label('مجالات البحث'))
        self.dict_field = {'nass':True, 'tit':False}
        self.in_nasse = Gtk.RadioButton.new_with_label_from_widget(None, u'في النصوص')
        self.in_nasse.set_name('nass')
        box.pack_start(self.in_nasse, False, False, 0)
        self.in_nasse.connect('toggled', self.select_field, 1)
        self.in_title = Gtk.RadioButton.new_with_label_from_widget(self.in_nasse, u'في العناوين')
        self.in_title.set_name('tit')
        box.pack_start(self.in_title, False, False, 0)
        self.in_title.connect('toggled', self.select_field, 2)

        box = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        box.set_border_width(7)
        notebk.append_page(box, Gtk.Label('خيارات البحث'))
        self.dict_perf = {}
        for a in [[u'بدون لواصق', u'identical'],
        [u'عبارة متصلة', u'cursive'], 
        [u'إحدى الكلمات', u'one_term'],  
        [u'مع التشكيل', u'with_tachkil']]:
            btn = Gtk.CheckButton(a[0])
            btn.set_name(a[1])
            box.pack_start(btn, False, False, 0)
            btn.connect('toggled', self.select_perf)
            self.dict_perf[a[1]] = False
        
        box = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        box.set_border_width(7)
        notebk.append_page(box, Gtk.Label('حفظ النطاقات'))
        sav_field = Gtk.Button('حفظ النطاق المحدد')
        sav_field.set_tooltip_text("حفظ نطاق البحث المحدد حالياً")
        hb = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(sav_field,False, False, 0)
        sav_field.connect('clicked', self.save_fields)
        self.ent_field = Gtk.Entry()
        self.ent_field.set_placeholder_text('اسم النطاق')
        hb.pack_start(self.ent_field,False, False, 0)
        box.pack_start(hb, False, False, 0)
        
        hb = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        rm_field = Gtk.Button('حذف النطاق المحدد')
        hb.pack_start(rm_field,False, False, 0)
        box.pack_start(hb, False, False, 0) 
        def rm_field_cb(widget, *a):
            model, i = self.tree_fields.get_selection().get_selected()
            if i:
                nm = model.get_value(i, 1)
                if nm == u"المفضلة": return
                os.remove(join(asm_path.LIBRARY_DIR, u'fields-search', nm+'.pkl')) 
                model.remove(i)
        rm_field.connect('clicked', rm_field_cb)
        
                
        box = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        box.set_border_width(7)
        notebk.append_page(box, Gtk.Label('خيارات أخرى'))
        del_term = Gtk.Button('مسح الكلمات المحفوظة')
        hb = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(del_term,False, False, 0)
        del_term.connect('clicked', self.del_history)
        box.pack_start(hb, False, False, 0)
        vbox1.pack_start(expander, False, False, 0)
        self.stack.add_titled(vbox1, 'n1', 'بحث عادي')
        
        hbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        box = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        box.set_border_width(7)
        self.dict_field_index = {'nass':True, 'tit':False}
        self.in_nasse_index = Gtk.RadioButton.new_with_label_from_widget(None, u'في النصوص')
        self.in_nasse_index.set_name('nass')
        box.pack_start(self.in_nasse_index, False, False, 0)
        self.in_nasse_index.connect('toggled', self.select_field_index, 1)
        self.in_title_index = Gtk.RadioButton.new_with_label_from_widget(self.in_nasse_index, u'في العناوين')
        self.in_title_index.set_name('tit')
        box.pack_start(self.in_title_index, False, False, 0)
        self.in_title_index.connect('toggled', self.select_field_index, 2)
        hbox.pack_start(box, False, False, 0)

        box = Gtk.Box(spacing=7,orientation=Gtk.Orientation.VERTICAL)
        box.set_border_width(7)
        self.dict_perf_index = {}
        for a in [[u'بدون لواصق', u'identical'],
        [u'عبارة متصلة', u'cursive'], 
        [u'إحدى الكلمات', u'one_term'],  
        [u'مع التشكيل', u'with_tachkil']]:
            btn = Gtk.CheckButton(a[0])
            btn.set_name(a[1])
            box.pack_start(btn, False, False, 0)
            btn.connect('toggled', self.select_perf_index)
            self.dict_perf_index[a[1]] = False
        hbox.pack_start(box, False, False, 0)
        
        vbox2.pack_start(hbox,True, True, 0)
        self.stack.add_titled(vbox2, 'n2', 'بحث مفهرس')
        if asm_config.getn('search') == 0:
            self.stack.set_visible_child_name("n1")
        else:
            self.stack.set_visible_child_name("n2")
        self.stack.show_all()
        area.pack_start(self.stack, True, True, 0)
