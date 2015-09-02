# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import Gtk, Gdk, Pango
from Asmaa.asm_contacts import bookDB, Othman, listDB
from Asmaa.asm_viewer import OpenBook
from Asmaa.asm_tablabel import TabLabel
import Asmaa.asm_path as asm_path
import Asmaa.asm_araby as asm_araby
import Asmaa.asm_customs as asm_customs
from os.path import join, basename
import os, re


ACCEL_CTRL_KEY, ACCEL_CTRL_MOD = Gtk.accelerator_parse("<Ctrl>")

# class صفحة تحرير كتاب-----------------------------------------------------------------------

class EditBook(Gtk.VBox):
    
    def close_db(self, *a):
        self.all_pages = []
        self.modified_pages = {}
        self.opened_new = []
        self.opened_old = []
        if self.db != None:
            self.db.close_db()
            del self.db
    
    def __init__(self, parent):
        Gtk.VBox.__init__(self, False, 3)
        self.set_border_width(5)
        self.parent = parent
        self.othman = Othman()
        self.db_list = listDB()
        self.db = None
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.build()
    
    # a التصفح--------------------------------------------

    def index_highlight(self, model, path, i, page_id):
        pid = model.get(i,0)[0]
        if pid == page_id: 
            self.tree_index.scroll_to_cell(path)
            self.sel_index.select_path(path)
            return False
        elif pid < page_id:
            return False
        else:
            return True

    def first_page(self, *a):
        self.current_id = 0
        self.show_page()
        i = self.store_index.get_iter_first()
        p = self.store_index.get_path(i)
        self.tree_index.scroll_to_cell(p)
        self.sel_index.select_path(p)
    
    def previous_page(self, *a):
        if self.current_id > 0: 
            self.current_id -= 1
        self.show_page()
        try: self.store_index.foreach(self.index_highlight, self.all_pages[self.current_id][0])
        except: pass
    
    def next_page(self, *a):
        if self.current_id < len(self.all_pages)-1: 
            self.current_id += 1
        self.show_page()
        try: self.store_index.foreach(self.index_highlight, self.all_pages[self.current_id][0])
        except: pass
    
    def last_page(self, *a):
        self.current_id = len(self.all_pages)-1
        self.show_page()
        try: self.store_index.foreach(self.index_highlight, self.all_pages[self.current_id][0])
        except: pass
    
    def back_to_old(self, *a):
        if len(self.opened_old) == 1: return
        n = self.opened_old.pop()
        self.show_page(self.opened_old[-1])
        self.opened_new.append(n)
        
    def advance_to_new(self, *a):
        if len(self.opened_new) == 0: return
        n = self.opened_new.pop()
        self.show_page(n)
        if n != self.opened_old[-1]: self.opened_old.append(n)
    
    def set_index(self, *a):
        self.store_index.clear()
        self.list_index = self.db.index_book()
        self.hp.set_position(200)
        v = 0
        for i in self.list_index:
            v += 1
            if v%1000 == 999: 
                while (Gtk.events_pending()): Gtk.main_iteration()
            self.store_index.append(None, [i[1], ('      '*(i[3]-1))+i[2]])
    
    
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
            for a in self.all_pages:
                if a[0] == id_page:
                    self.current_id = self.all_pages.index(a)
                    break
            self.show_page()
    
    def search_on_active(self, text):
        return
    
    def search_on_page(self, text):
        self.show_page(self.all_in_page[1])
        search_tokens = []
        nasse = self.view_nasse_bfr.get_text(self.view_nasse_bfr.get_start_iter(), 
                                            self.view_nasse_bfr.get_end_iter(),True).split()
        if text == u'': 
            return
        else:
            txt = asm_araby.fuzzy(text)
            for term in nasse: 
                if txt in asm_araby.fuzzy(term):
                    search_tokens.append(term)
        asm_customs.with_tag(self.view_nasse_bfr, self.view_search_tag, search_tokens, 1)
            
    def show_page(self, id_page=0):
        self.view_nasse_bfr.handler_block(self.editpg)
        if id_page == 0: id_page = self.all_pages[self.current_id][0]
        if id_page in self.modified_pages.keys():
            self.view_nasse_bfr.set_text(self.modified_pages[id_page])
        else:
            self.all_in_page = self.db.get_text_body(id_page)#rowid, id, text, part, page, hno, sora, aya, na
            self.view_nasse_bfr.set_text(self.all_in_page[2])
        self.ent_page.set_text(str(self.all_pages[self.current_id][2]))
        self.ent_part.set_text(str(self.all_pages[self.current_id][1]))
        self.scroll_nasse.get_vadjustment().set_value(0.0)
        self.view_nasse_bfr.handler_unblock(self.editpg)
        if len(self.opened_old) == 0: self.opened_old.append(id_page)
        elif id_page != self.opened_old[-1]: self.opened_old.append(id_page)
    
    def show_bitaka(self, *a):
        if self.db.info_book() == None:
            text_info = self.nm_book
        else: text_info = self.db.info_book()
        return text_info
    
    def show_book(self, *a):
        n = self.parent.viewerbook.get_n_pages()
        for s in range(n):
            ch = self.parent.viewerbook.get_nth_page(s)
            if self.parent.viewerbook.get_tab_label(ch).nm == self.nm_book:
                self.parent.viewerbook.get_tab_label(ch).close_tab()
        sr = OpenBook(self.parent, self.book, self.id_book)
        self.parent.viewerbook.append_page(sr,TabLabel(sr, self.nm_book))
        self.parent.viewerbook.set_current_page(-1)
        self.parent.notebook.set_current_page(1)
        sr.set_index()
        
    def add_book(self, book, id_book, id_page):
        self.current_id = id_page-1
        self.modified_pages = {}
        self.opened_new = []
        self.opened_old = []
        self.id_book = id_book
        self.book = book
        self.new_book = book+u'.new'
        self.nm_book = basename(book)[:-4]
        self.db = bookDB(book, id_book)
        self.all_pages = self.db.all_page()
        self.n_all_page = len(self.all_pages)+1
        self.set_index()
        self.show_page(id_page)
        try: self.store_index.foreach(self.index_highlight, id_page)
        except: pass
    
    def change_font(self, *a):
        self.view_search_tag.set_property('background', self.parent.theme.color_fnd)

    def populate_popup(self, view, menu):
        for a in menu.get_children():
            a.destroy()
        buff = view.get_buffer()
        f1 = Gtk.MenuItem('اجعل النص المحدد عنوانا')
        menu.append(f1)
        f1.set_sensitive(False)
        model, i = self.sel_index.get_selected()
        if i:
            pgid = model.get_value(i, 0)
            if pgid == self.all_pages[self.current_id][0]:
                imenu = Gtk.Menu()
                f1.set_submenu(imenu)
                fm1 = Gtk.MenuItem('قبل العنوان المحدد')
                fm1.connect("activate", self.add_title_before)
                imenu.append(fm1)
                fm1.show()
                fm2 = Gtk.MenuItem('بعد العنوان المحدد')
                imenu.append(fm2)
                iimenu = Gtk.Menu()
                fm2.set_submenu(iimenu)
                fm21 = Gtk.MenuItem('قسيما لسابقه')
                fm21.connect("activate", self.add_title_after, 0)
                iimenu.append(fm21)
                fm21.show()
                fm22 = Gtk.MenuItem('ابنا لسابقه')
                fm22.connect("activate", self.add_title_after, 1)
                iimenu.append(fm22)
                fm22.show()
                fm2.show()
            else:
                f1.connect("activate", self.add_title_after)
        else:
            f1.connect("activate", self.add_title_after)
                
        f1.show()
        f2 = Gtk.MenuItem('أضف صفحة قبل')
        menu.append(f2)
        f2.show()
        f3 = Gtk.MenuItem('أضف صفحة بعد')
        menu.append(f3)
        f3.show()
        c1 = Gtk.SeparatorMenuItem()
        menu.append(c1)
        c1.show()
        f4 = Gtk.MenuItem('احذف هذه الصفحة')
        menu.append(f4)
        f4.show()
        
        if buff.get_has_selection():
            f1.set_sensitive(True)
        f2.connect("activate", self.add_page, 0)
        f3.connect("activate", self.add_page, 1)
        f4.connect("activate", self.del_page)
    
    def add_title_before(self, *a):
        start_iter, end_iter = self.view_nasse_bfr.get_selection_bounds()
        sel_text = self.view_nasse_bfr.get_text(start_iter, end_iter, True).strip()
        model, i = self.sel_index.get_selected()
        if i:
            p = model.get_path(i)
            v = model.get_value(i, 1)
            n = v.count('      ')
            self.store_index.insert_before(None, i, [self.all_pages[self.current_id][0], ('      '*(n))+sel_text])
            self.sel_index.select_path(p)
            self.tree_index.scroll_to_cell(p)
        else:
            self.store_index.append(None, [self.all_pages[self.current_id][0], sel_text])
    
    def add_title_after(self, item, s=0):
        start_iter, end_iter = self.view_nasse_bfr.get_selection_bounds()
        sel_text = self.view_nasse_bfr.get_text(start_iter, end_iter, True).strip()
        model, i = self.sel_index.get_selected()
        if i:
            p = model.get_path(i)
            v = model.get_value(i, 1)
            n = v.count('      ')
            i0 = self.store_index.insert_after(None, i, [self.all_pages[self.current_id][0], ('      '*(n+s))+sel_text])
            p = model.get_path(i0)
            self.sel_index.select_path(p)
            self.tree_index.scroll_to_cell(p)
        else:
            self.store_index.append(None, [self.all_pages[self.current_id][0], sel_text])
        
    def add_page(self, w, v):
        self.all_pages.insert(self.current_id+v, [self.n_all_page, self.all_pages[self.current_id][1], 
                                                  self.all_pages[self.current_id][2]+v])
        self.modified_pages[self.all_pages[self.current_id+v][0]] = ''
        for a in range(self.current_id+v+1, len(self.all_pages)):
            if self.all_pages[a][1] == self.all_pages[self.current_id][1]:
                self.all_pages[a] = [self.all_pages[a][0], self.all_pages[a][1], self.all_pages[a][2]+1]
        self.current_id = self.current_id+v
        self.show_page()
        self.n_all_page += 1
        
    def del_titles_with_pages(self, model, path, i, page_id):
        pid = model.get(i,0)[0]
        if pid == page_id: 
            model.remove(i)
    
    def del_page(self, *a):
        id_page = self.all_pages[self.current_id][0]
        del self.all_pages[self.current_id]
        for a in range(self.current_id, len(self.all_pages)):
            if self.all_pages[a][1] == self.all_pages[self.current_id][1]:
                self.all_pages[a] = [self.all_pages[a][0], self.all_pages[a][1], self.all_pages[a][2]-1]
        if id_page == 1: 
            p = 0
            self.current_id = 0
        else: 
            p = id_page-1
            self.current_id -= 1
            for a in self.store_index:
                if id_page == a[0]:
                    try: self.store_index.foreach(self.del_titles_with_pages, id_page)
                    except: pass
        self.show_page(p)
        
    def change_n_page(self, *a):
        n_page = int(self.ent_page.get_text())
        n_part = int(self.ent_part.get_text())
        v = 0
        for a in range(self.current_id, len(self.all_pages)):
            if self.all_pages[a][1] <= n_part:
                self.all_pages[a] = [self.all_pages[a][0], n_part, n_page+v]
                v += 1
        
    def on_button_press(self, widget, event):
        if event.button == 3:
            self.popup.show_all()
            self.popup.popup(None, None, None, None, 3,
                             Gtk.get_current_event_time())
        elif event.button == 1 and event.get_click_count()[1] == 2:
            self.ok_index()
   
    def edit_page(self, *a):
        self.modified_pages[self.all_pages[self.current_id][0]] = self.view_nasse_bfr.get_text(self.view_nasse_bfr.get_start_iter(),
                            self.view_nasse_bfr.get_end_iter(), False)
    
    def mod_child(self, i, i0):
        v0 = self.store_index.get_value(i0, 1)
        n0 = v0.count('      ')
        v = self.store_index.get_value(i, 1)
        n = v.count('      ')
        if n0-n >= 2:
            self.store_index.set_value(i0, 1, ('      '*(n0-1))+v0.strip())
        i00 = self.store_index.iter_next(i0)
        if i00:
            self.mod_child(i, i00)
    
    def make_parent(self, *a):
        model, i = self.sel_index.get_selected()
        if i:
            v = model.get_value(i, 1)
            n = v.count('      ')
            if n == 0: return
            model.set_value(i, 1, ('      '*(n-1))+v.strip())
            i0 = model.iter_next(i)
            if i0:
                self.mod_child(i, i0)
            
    def make_child(self, *a):
        model, i = self.sel_index.get_selected()
        if i:
            if not model.iter_previous(i): return
            i0 = model.iter_previous(i)
            v0 = model.get_value(i0, 1)
            n0 = v0.count('      ')
            v = model.get_value(i, 1)
            n = v.count('      ')
            if n == n0+1: return
            model.set_value(i, 1, ('      '*(n+1))+v.strip())
    
    def up_row(self, *a):
        model, i = self.sel_index.get_selected()
        if i:
            i0 = model.iter_previous(i)
            v0 = model.get_value(i0, 1)
            n0 = v0.count('      ')
            v = model.get_value(i, 1)
            model.set_value(i, 1, ('      '*(n0))+v.strip())
            model.move_before(i, i0)
            
    def down_row(self, *a):
        model, i = self.sel_index.get_selected()
        if i:
            i0 = model.iter_next(i)
            v0 = model.get_value(i0, 1)
            n0 = v0.count('      ')
            v = model.get_value(i, 1)
            n = v.count('      ')
            if n-n0 >= 2:
                model.set_value(i, 1, ('      '*(n0+1))+v.strip())
            model.move_after(i, i0)
    
    def del_row(self, *a):
        model, i = self.sel_index.get_selected()
        if i:
            model.remove(i)

    def rename_tit(self, cell, path, new_text):
        n = self.store_index[path][1].count('      ')
        self.store_index[path][1] = ('      '*(n))+new_text.strip()
        return
    
    def save_book(self, *a):
        page_dict = {}
        res = asm_customs.sure(self.parent, 'هل أكملت جميع التغييرات المبتغاة وتريد الحفظ؟')
        if res == Gtk.ResponseType.YES:
            self.db.cur.execute("BEGIN;")
            self.db.cur.execute('ATTACH ? as f',(self.new_book,))
            for tb in asm_customs.schema.keys():
                self.db.cur.execute('CREATE TABLE IF NOT EXISTS f.{} ({})'.format(tb, asm_customs.schema[tb]))
            for i in ['main', 'shorts', 'shrooh', 'com']:
                self.db.cur.execute("INSERT INTO f.{} SELECT * FROM main.{}".format(i,i))
            pg = 0
            while pg in range(len(self.all_pages)):
                if self.all_pages[pg][0] <= len(self.db.list_pages):
                    all_in_page = self.db.get_text_body(self.all_pages[pg][0])
                    text = all_in_page[2]
                    hno, sora, aya, na = all_in_page[5:]
                else: 
                    text = u''
                    hno, sora, aya, na = [0, 0, 0, 0]
                if self.all_pages[pg][0] in self.modified_pages.keys():
                    text = self.modified_pages[self.all_pages[pg][0]]
                part, page = self.all_pages[pg][1], self.all_pages[pg][2]
                self.db.cur.execute('INSERT INTO f.pages VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                                    (pg+1, text, part, page, hno, sora, aya, na))
                page_dict[self.all_pages[pg][0]] = pg+1
                pg += 1
            for ti in self.store_index:
                try: self.db.cur.execute('INSERT INTO f.titles VALUES (?, ?, ?, ?)', 
                                         (page_dict[ti[0]], ti[1].strip(), ti[1].count('      ')+1, 0))
                except: continue
            self.db.con.commit()
            self.db.cur.execute('DETACH f')
            os.unlink(self.book)
            os.rename(self.new_book, self.book)
    
    def replace_all(self, *a):
        if self.parent.notebook.get_current_page() == 7:
            dlg = Gtk.Dialog(parent=self.parent)
            dlg.set_icon_name("asmaa")
            dlg.set_title('إيجاد واستبدال')
            text_old = Gtk.Entry()
            text_old.set_placeholder_text('النص القديم')
            if self.view_nasse_bfr.get_has_selection():
                sel = self.view_nasse_bfr.get_selection_bounds()
                text = self.view_nasse_bfr.get_text(sel[0], sel[1],True)
                text_old.set_text(text)
            text_new = Gtk.Entry()
            text_new.set_placeholder_text('النص الجديد')
            use_re = Gtk.CheckButton('استعمل التعبيرات المنتظمة')
            clo = asm_customs.ButtonClass("إغلاق")
            clo.connect('clicked',lambda *a: dlg.destroy())
            rpl = asm_customs.ButtonClass("استبدل الكل")
            def replace_cb(widget):
                old_t = self.view_nasse_bfr.get_text(self.view_nasse_bfr.get_start_iter(),
                                self.view_nasse_bfr.get_end_iter(), False)
                if use_re.get_active():
                    new_t = re.sub(text_old.get_text(), text_new.get_text(), old_t)
                else:
                    new_t = old_t.replace(text_old.get_text(), text_new.get_text())
                self.view_nasse_bfr.set_text(new_t)
            rpl.connect('clicked', replace_cb)
            hb = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
            box = dlg.vbox
            box.set_border_width(5)
            hb.pack_start(rpl, False, False, 0)
            hb.pack_end(clo, False, False, 0)
            box.pack_start(text_old, False, False, 3)
            box.pack_start(text_new, False, False, 3)
            box.pack_start(use_re, False, False, 3)
            box.pack_end(hb, False, False, 0)
            dlg.show_all()
       
    def undo_cb(self, *a):
        id_page = self.all_pages[self.current_id][0]
        if id_page in self.modified_pages.keys():
            del self.modified_pages[id_page]
        self.show_page(id_page)
       
    def build(self, *a):
        self.vadjustment_page = 0.0
        self.hp = Gtk.HPaned()
        
        # a الفهرس-----------------------------------
        vbox = Gtk.VBox(False, 3)
        self.tree_index = Gtk.TreeView()
        self.tree_index.override_font(Pango.FontDescription('KacstOne 13'))
        cell = Gtk.CellRendererText()
        cell.set_property( 'editable', True )
        cell.connect('edited', self.rename_tit)
        kal = Gtk.TreeViewColumn('الفهرس', cell, text=1)
        self.tree_index.append_column(kal)
        self.store_index = Gtk.TreeStore(int, str)
        self.tree_index.set_model(self.store_index)
        self.sel_index = self.tree_index.get_selection()
        self.tree_index.connect("button-press-event", self.on_button_press)
        self.tree_index.connect("cursor-changed", self.ok_index)
        self.scroll_index = Gtk.ScrolledWindow()
        self.scroll_index.set_shadow_type(Gtk.ShadowType.IN)
        self.scroll_index.add(self.tree_index)
        self.scroll_index.get_hadjustment().set_value(0.0) 
        vbox.pack_start(self.scroll_index, True, True, 0)
        #--- Popup menu
        self.popup = Gtk.Menu()
        f1 = Gtk.ImageMenuItem('اجعله أبا')
        f1.connect('activate', self.make_parent)
        self.popup.append(f1)
        f2 = Gtk.ImageMenuItem('اجعله ابنا')
        f2.connect('activate', self.make_child)
        self.popup.append(f2)
        f3 = Gtk.ImageMenuItem('ارفعه سطرا')
        f3.connect('activate', self.up_row)
        self.popup.append(f3)
        f4 = Gtk.ImageMenuItem('اخفضه سطرا')
        f4.connect('activate', self.down_row)
        self.popup.append(f4)
        f5 = Gtk.ImageMenuItem('احذف')
        f5.connect('activate', self.del_row)
        self.popup.append(f5)
        self.popup.show_all()
        
        hbox = Gtk.HBox(False, 3)
        img = Gtk.Image.new_from_file(join(asm_path.ICON_DIR, 'right.png'))
        toright = Gtk.ToolButton()
        toright.set_icon_widget(img)
        toright.set_tooltip_text('اجعله أبا')
        toright.connect('clicked', self.make_parent)
        hbox.pack_start(toright, False, False, 0)
        
        img = Gtk.Image.new_from_file(join(asm_path.ICON_DIR, 'left.png'))
        toleft = Gtk.ToolButton()
        toleft.set_icon_widget(img)
        toleft.set_tooltip_text('اجعله ابنا')
        toleft.connect('clicked', self.make_child)
        hbox.pack_start(toleft, False, False, 0)
        
        img = Gtk.Image.new_from_file(join(asm_path.ICON_DIR, 'up.png'))
        toup = Gtk.ToolButton()
        toup.set_icon_widget(img)
        toup.set_tooltip_text('ارفعه سطرا')
        toup.connect('clicked', self.up_row)
        hbox.pack_start(toup, False, False, 0)
        
        img = Gtk.Image.new_from_file(join(asm_path.ICON_DIR, 'down.png'))
        todown = Gtk.ToolButton()
        todown.set_icon_widget(img)
        todown.set_tooltip_text('اخفضه سطرا')
        todown.connect('clicked', self.down_row)
        hbox.pack_start(todown, False, False, 0)
        
        img = Gtk.Image.new_from_file(join(asm_path.ICON_DIR, 'remove.png'))
        toremove = Gtk.ToolButton()
        toremove.set_icon_widget(img)
        toremove.set_tooltip_text('احذف عنوانا')
        toremove.connect('clicked', self.del_row)
        hbox.pack_start(toremove, False, False, 0)
        
        vbox.pack_start(hbox, False, False, 0)
        self.hp.pack1(vbox, True, True)
        
        # a عارض النص-----------------------------------
        vbox = Gtk.VBox(False, 3)
        self.view_nasse = Gtk.TextView()
        self.view_nasse.set_right_margin(10)
        self.view_nasse.set_left_margin(10)
        self.view_nasse.set_wrap_mode(Gtk.WrapMode.WORD)
        self.view_nasse.override_font(Pango.FontDescription('KacstOne 15'))
        self.view_nasse_bfr = self.view_nasse.get_buffer()
        self.view_nasse.connect_after("populate-popup", self.populate_popup)
        self.editpg = self.view_nasse_bfr.connect_after("changed", self.edit_page)
        self.view_title_tag = self.view_nasse_bfr.create_tag("title")
        self.view_quran_tag = self.view_nasse_bfr.create_tag("quran")
        self.view_search_tag = self.view_nasse_bfr.create_tag("search")
        self.view_terms_tag = self.view_nasse_bfr.create_tag("terms")
        self.scroll_nasse = Gtk.ScrolledWindow()
        self.scroll_nasse.set_shadow_type(Gtk.ShadowType.IN)
        self.scroll_nasse.add(self.view_nasse)
        vbox.pack_start(self.scroll_nasse, True, True, 0)
        hbox = Gtk.HBox(False, 3)
        self.page_n = Gtk.Label('الصفحة')
        hbox.pack_start(self.page_n, False, False, 0) 
        self.ent_page = Gtk.Entry()
        self.ent_page.set_width_chars(5)
        hbox.pack_start(self.ent_page, False, False, 0)
        self.part_n = Gtk.Label('الجزء') 
        self.ent_part = Gtk.Entry()
        self.ent_part.set_width_chars(5) 
        hbox.pack_start(self.part_n, False, False, 0)
        hbox.pack_start(self.ent_part, False, False, 0) 
        self.move_btn = Gtk.ToolButton(stock_id=Gtk.STOCK_EDIT)
        self.move_btn.set_tooltip_text('تغيير رقم الجزء والصفحة')
        self.move_btn.connect('clicked', self.change_n_page)
        hbox.pack_start(self.move_btn, False, False, 2)
        
        vbox.pack_start(hbox, False, False, 0)
        
        self.hp.pack2(vbox, True, False)
        self.pack_start(self.hp, True, True, 0)
        self.show_all()
        self.change_font()
        self.parent.axl.connect(Gdk.KEY_f, ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE, self.replace_all)