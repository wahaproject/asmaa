# -*- coding: utf-8 -*-
from gi.repository import Gtk, Pango
from gi.repository import GdkPixbuf
from Asmaa.asm_contacts import listDB
from Asmaa.asm_viewer import OpenBook
from Asmaa.asm_tablabel import TabLabel
import Asmaa.asm_path as asm_path
import Asmaa.asm_config as asm_config
import Asmaa.asm_customs as asm_customs
import pickle
from os.path import join
from os import remove


COL_NAME = 0
COL_PIXBUF = 1
COL_ID = 2


# class نافذة قائمة الكتب-----------------------------------------------------------------------

class ListBooks(Gtk.HBox):
    
    def __init__(self, parent):
        self.parent = parent
        self.db = listDB()
        try: self.last_books = pickle.load(open((join(asm_path.DATA_DIR_rw, u'last-books.pkl')), "rb"))
        except: self.last_books = []
        self.build()
   
    def load_list(self, *a):
        self.store_parts_list.clear()
        self.store_parts_icon.clear()
        groups = self.db.all_parts()
        for a in groups:
            self.store_parts_icon.append([a[1], self.particon, a[0]])
            self.store_parts_list.append([a[0], a[1], self.particon1])

        
    def select_row(self, tree, tree_sel): 
        model, i = tree_sel.get_selected()
        if i:
            id_book = model.get_value(i, 0)
            nm_book = model.get_value(i, 1)
            book = self.db.file_book(id_book)
            text_info = self.db.info_book(book)[3]
            if text_info == None:
                text_info = nm_book
            self.view_info_bfr.set_text(text_info)
    
    def add_to_lasts(self, id_book):
        if len(self.last_books) == 20: self.last_books.pop(0)
        if id_book in self.last_books:
            self.last_books.remove(id_book)
        self.last_books.append(id_book)
        try: 
            output = open(join(asm_path.DATA_DIR_rw, u'last-books.pkl'), 'wb')
            pickle.dump(self.last_books, output)
            output.close()
        except: pass
        self.load_last()
           
    
    def avtive_row_parts(self, *a): 
        model, i = self.sel_parts.get_selected()
        if i:
            self.store_books_list.clear()
            id_part = model.get_value(i, 0)
            books_part = self.db.books_part(id_part) 
            self.nb.set_current_page(3)
            v = 0
            for bk in books_part:
                v += 1
                if v%200 == 199: 
                    while (Gtk.events_pending()): Gtk.main_iteration()
                self.store_books_list.append([bk[0], bk[1], self.bookicon1]) 
            self.parent.go_parts.show_all()
            
    def avtive_row_books(self, *a): 
        model, i = self.sel_books.get_selected()
        if i:
            id_book = model.get_value(i, 0)
            nm_book = model.get_value(i, 1)
            my_book = self.db.file_book(id_book)
            self.open_book(my_book, nm_book, id_book)
            self.add_to_lasts(id_book)
        
    def open_book(self, my_book, nm_book, id_book):
        n = self.parent.viewerbook.get_n_pages()
        for s in range(n):
            ch = self.parent.viewerbook.get_nth_page(s)
            if self.parent.viewerbook.get_tab_label(ch).nm == nm_book:
                self.parent.viewerbook.set_current_page(s)
                self.parent.notebook.set_current_page(1)
                return
        sr = OpenBook(self.parent, my_book, id_book)
        self.parent.viewerbook.append_page(sr,TabLabel(sr, nm_book))
        self.parent.viewerbook.set_current_page(-1)
        self.parent.notebook.set_current_page(1)
        sr.set_index()
    
    # a دوال المفضلة-------------------------------------------------------------------
                
    def rm_fav_one(self, *a):
        model, i = self.sel_favorite.get_selected()
        if i:
            msg = asm_customs.sure(self.parent, "هل تريد مسح الكتاب المحدد من المفضلة")
            if msg == Gtk.ResponseType.YES:
                id_book = model.get_value(i,0)
                check = self.db.out_favorite(id_book)
                if check == None:
                    model.remove(i)
    
    def ok_fav(self, *a):
        model, i = self.sel_favorite.get_selected()
        if i:
            id_book = model.get_value(i,0)
            nm_book = model.get_value(i,1)
            my_book = self.db.file_book(id_book)
            self.open_book(my_book, nm_book, id_book)
            self.add_to_lasts(id_book)
    
    def load_fav(self, *a):
        self.store_favorite.clear()
        ls = self.db.favorite_books()
        for a in ls:
            self.store_favorite.append([a[0], a[1]])
        
    # a دوال الكتب الأخيرة-------------------------------------------------------------------
                
    def rm_last_all(self, *a):
        msg = asm_customs.sure(self.parent, "هل تريد مسح قائمة الكتب المفتوحة أخيرا")
        if msg == Gtk.ResponseType.YES:
            remove(join(asm_path.DATA_DIR_rw, u'last-books.pkl'))
            self.last_books = []
            self.store_last.clear()
    
    def ok_last(self, *a):
        model, i = self.sel_last.get_selected()
        if i:
            id_book = model.get_value(i,0)
            nm_book = model.get_value(i,1)
            my_book = self.db.file_book(id_book)
            self.open_book(my_book, nm_book, id_book)
            self.add_to_lasts(id_book)
    
    def load_last(self, *a):
        self.store_last.clear()
        for a in reversed(self.last_books):
            book = self.db.tit_book(a)
            if book:
                self.store_last.append([book[0], book[1]])
    
    def search_on_page(self, text):
        if self.nb.get_current_page() in [0, 1]:
            self.search_item_cb(text)
        elif self.nb.get_current_page() in [2, 3]:
            self.search_list_cb(text)
    
    def search_on_active(self, text):
        self.search_on_page(text)
        
    def search_list_cb(self, text):
        if text == '':
            self.nb.set_current_page(2)
        else:
            books = self.db.search_books(text)
            self.store_books_list.clear()
            for a in books:
                self.store_books_list.append([a[0], a[1], self.bookicon1]) 
            self.nb.set_current_page(3)
            self.parent.go_parts.show_all()
    
    def search_item_cb(self, text):
        if text == '':
            self.nb.set_current_page(0)
        else:
            books = self.db.search_books(text)
            self.store_books_icon.clear()
            for a in books:
                self.store_books_icon.append([a[1], self.bookicon, a[0]]) 
            self.nb.set_current_page(1)  
            self.parent.go_parts.show_all()      
    
    def item_part_active(self, widget, path):
        item = widget.get_selected_items()
        model = widget.get_model()
        id_part = model[item[0]][COL_ID]
        self.store_books_icon.clear()
        books_part = self.db.books_part(id_part)
        self.nb.set_current_page(1)
        widget.show_all()
        v = 0
        for bk in books_part:
            v += 1
            if v%200 == 199: 
                while (Gtk.events_pending()): Gtk.main_iteration()
            self.store_books_icon.append([bk[1], self.bookicon, bk[0]]) 
        self.parent.go_parts.show_all()
    
    def item_book_select(self, widget):
        item = widget.get_selected_items() 
        if len(item) > 0:
            model = widget.get_model()
            id_book = model[item[0]][COL_ID]
            nm_book = model[item[0]][COL_NAME]
            my_book = self.db.file_book(id_book)
            text_info = self.db.info_book(my_book)[3]
            if text_info == None:
                text_info = nm_book
            self.view_info_bfr.set_text(text_info)
            if self.select_book == nm_book:
                self.open_book(my_book, nm_book, id_book)
                self.add_to_lasts(id_book)
            else: self.select_book = nm_book
   
    def back_cb(self, *a):
        if self.nb.get_current_page() == 1:
            self.nb.set_current_page(0)
        elif self.nb.get_current_page() == 3:   
            self.nb.set_current_page(2)
        self.parent.go_parts.hide()
    
    def change_icon_spacing(self, iconview):
        return
      
    def build(self, *a):
        self.select_part = u''
        self.select_book = u''
        Gtk.HBox.__init__(self, False, 3)
        self.set_border_width(3)
        self.vbox_side = Gtk.VBox(False, 0)
        
        # a أيقونات الكتب--------------------------
        self.vbox_iconview = Gtk.VBox(False, 5)
        self.nb = Gtk.Notebook()
        self.nb.set_show_tabs(False)
        vbox = Gtk.VBox(False, 0) 
        self.particon = GdkPixbuf.Pixbuf.new_from_file_at_size(join(asm_path.ICON_DIR, 'Groups-128.png'), 128, 128)
        self.bookicon = GdkPixbuf.Pixbuf.new_from_file_at_size(join(asm_path.ICON_DIR, 'Book-128.png'), 96, 96)
        sw = Gtk.ScrolledWindow()
        vbox.pack_start(sw, True, True, 0)
        self.store_parts_icon = Gtk.ListStore(str, GdkPixbuf.Pixbuf, int)
        iconView_parts = Gtk.IconView()
        iconView_parts.set_reorderable(True)
        iconView_parts.set_model(self.store_parts_icon)
        iconView_parts.override_font(Pango.FontDescription('KacstOne 20'))
        iconView_parts.set_text_column(COL_NAME)
        iconView_parts.set_pixbuf_column(COL_PIXBUF)
        iconView_parts.set_item_width(150)
        iconView_parts.set_row_spacing(50)
        iconView_parts.connect("item-activated", self.item_part_active)
        sw.add(iconView_parts)
        iconView_parts.grab_focus()
        self.nb.append_page(vbox, Gtk.Label('0'))
        
        vbox = Gtk.VBox(False, 0);  
        sw = Gtk.ScrolledWindow()
        vbox.pack_start(sw, True, True, 0)
        self.store_books_icon = Gtk.ListStore(str, GdkPixbuf.Pixbuf, int)
        iconView_books = Gtk.IconView()
        iconView_books.set_model(self.store_books_icon)
        iconView_books.override_font(Pango.FontDescription('KacstOne 16'))
        iconView_books.set_text_column(COL_NAME)
        iconView_books.set_pixbuf_column(COL_PIXBUF)
        iconView_books.connect("selection_changed", self.item_book_select)
        iconView_books.set_item_width(120)
        iconView_books.set_row_spacing(40)
        sw.add(iconView_books)
        iconView_books.grab_focus()
        self.nb.append_page(vbox, Gtk.Label('1'))
        self.vbox_iconview.pack_start(self.nb, True, True, 0)
        
        # a قائمة الكتب----------------------------
        self.particon1 = GdkPixbuf.Pixbuf.new_from_file_at_size(join(asm_path.ICON_DIR, 'Groups-128.png'), 32, 32)
        self.bookicon1 = GdkPixbuf.Pixbuf.new_from_file_at_size(join(asm_path.ICON_DIR, 'Book-128.png'), 24, 24)
        scroll = Gtk.ScrolledWindow()
        self.tree_parts = asm_customs.TreeParts()
        self.tree_parts.set_headers_visible(False)
        self.sel_parts = self.tree_parts.get_selection()
        cell = Gtk.CellRendererText()
        cell.set_property("ellipsize", Pango.EllipsizeMode.END)
        kal = Gtk.TreeViewColumn('الأقسام')    
        icon_renderer = Gtk.CellRendererPixbuf();
        kal.pack_start(icon_renderer, False);
        kal.pack_start(cell, False);
        kal.add_attribute(icon_renderer, "pixbuf", 2);
        kal.add_attribute(cell, "text", 1);   

        self.tree_parts.connect("row-activated", self.avtive_row_parts)
        self.tree_parts.append_column(kal)
        self.store_parts_list = Gtk.ListStore(int, str, GdkPixbuf.Pixbuf)
        scroll.add(self.tree_parts)
        self.tree_parts.set_model(self.store_parts_list)
        self.load_list()
        self.nb.append_page(scroll, Gtk.Label('2'))
        
        scroll = Gtk.ScrolledWindow()
        self.tree_books = asm_customs.TreeBooks()
        self.tree_books.set_headers_visible(False)
        self.sel_books = self.tree_books.get_selection()
        cell = Gtk.CellRendererText()
        cell.set_property("ellipsize", Pango.EllipsizeMode.END)
        kal = Gtk.TreeViewColumn('الكتب')    
        icon_renderer = Gtk.CellRendererPixbuf();
        kal.pack_start(icon_renderer, False);
        kal.pack_start(cell, False);
        kal.add_attribute(icon_renderer, "pixbuf", 2);
        kal.add_attribute(cell, "text", 1);   
        self.tree_books.connect("row-activated", self.avtive_row_books)
        self.tree_books.append_column(kal)
        self.store_books_list = Gtk.ListStore(int, str, GdkPixbuf.Pixbuf)
        scroll.add(self.tree_books)
        self.tree_books.set_model(self.store_books_list)
        self.nb.append_page(scroll, Gtk.Label('3'))
        
        # a بطاقة كتاب--------------------------------
        self.view_info = asm_customs.ViewBitaka()
        self.view_info_bfr = self.view_info.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_info)
        scroll.set_size_request(250, 200)
        self.vbox_side.pack_start(scroll, False, False, 0)
        
        # a ------------------------------------------
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)
        
        # a الكتب الأخيرة------------------------------
        vbox = Gtk.Box(spacing=2,orientation=Gtk.Orientation.VERTICAL)
#        vbox.set_border_width(3)
        self.tree_last = asm_customs.TreeIndex()
        self.tree_last.set_headers_visible(False)
        self.tree_last.set_size_request(250, -1)
        self.sel_last = self.tree_last.get_selection()
        cell = Gtk.CellRendererText()
        kal = Gtk.TreeViewColumn('الكتب الأخيرة', cell, text=1)
        self.tree_last.append_column(kal)
        self.store_last = Gtk.ListStore(int, str)
        self.load_last()
        self.tree_last.set_model(self.store_last)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_last)
        self.tree_last.connect("row-activated", self.ok_last)
        vbox.pack_start(scroll, True, True, 0)

        remove_all = Gtk.Button("مسح القائمة")
        remove_all.connect('clicked', self.rm_last_all)
        vbox.pack_start(remove_all, False, False, 0)
        stack.add_titled(vbox, 'n0', 'الكتب الأخيرة')
        
        # a المفضلة-----------------------------------
        vbox = Gtk.Box(spacing=2,orientation=Gtk.Orientation.VERTICAL)
#        vbox.set_border_width(3)
        self.tree_favorite = asm_customs.TreeIndex()
        self.tree_favorite.set_headers_visible(False)
        self.tree_favorite.set_size_request(250, -1)
        self.sel_favorite = self.tree_favorite.get_selection()
        cell = Gtk.CellRendererText()
        kal = Gtk.TreeViewColumn('الكتب المفضلة', cell, text=1)
        self.tree_favorite.append_column(kal)
        self.store_favorite = Gtk.ListStore(int, str)
        self.load_fav()
        self.tree_favorite.set_model(self.store_favorite)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_favorite)
        self.tree_favorite.connect("row-activated", self.ok_fav)
        vbox.pack_start(scroll, True, True, 0)
        
        self.tree_books.connect("cursor-changed", self.select_row, self.sel_books)
        self.tree_last.connect("cursor-changed", self.select_row, self.sel_last)
        self.tree_favorite.connect("cursor-changed", self.select_row, self.sel_favorite)
        
        remove_one = Gtk.Button("حذف من المفضلة")
        remove_one.connect('clicked', self.rm_fav_one)
        vbox.pack_start(remove_one, False, False, 0)
        stack.add_titled(vbox, 'n1', 'الكتب المفضلة')
        
        hbox = Gtk.Box(spacing=2,orientation=Gtk.Orientation.HORIZONTAL)
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        hbox.pack_start(stack_switcher, True, False, 0)
        self.vbox_side.pack_start(hbox, False, False, 3)
        self.vbox_side.pack_start(stack, True, True, 0)
        
        self.pack_start(self.vbox_iconview, True, True, 0)
        self.pack_start(self.vbox_side, False, False, 0)
        self.show_all()
        
        #-----------------------------------------
        if asm_config.getn('view_books') == 0:
            pass
        else:
            self.nb.set_current_page(2)
