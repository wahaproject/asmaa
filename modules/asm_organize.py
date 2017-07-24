# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
#a############################################################################

from os.path import join, exists
from os import mkdir, rename, listdir, unlink
from shutil import rmtree, copyfile
from asm_contacts import listDB
from gi.repository import Gtk, Pango
import asm_customs
import asm_path
import asm_araby
from asm_edit_bitaka import EditBitaka
from asm_edit_tafsir import EditTafsir
from asm_count import Count

# class صفحة التعديل--------------------------------------------------

class Organize(Gtk.Box):
    
    def visible_cb(self, model, itr, data):
        if len(self.theword) == 0: return
        if asm_araby.fuzzy(self.theword[0]) in asm_araby.fuzzy(model.get_value(itr, 1)):
            return True
        else: return False
        
    def search_on_active(self, text):
        self.search_on_page(text)
        
    def search_on_page(self, text):
        self.theword = [text]
        self.modelfilter.refilter()
    
    def __init__(self, parent):
        self.parent = parent
        self.db = listDB()
        self.mycount = Count()
        self.size_font = asm_customs.split_font(self.parent.theme.font_nasse_books)[0]
        self.list_modifieds = []
        self.build()
    
    def add_to_favory(self, *a):
        model, i = self.sel_book.get_selected()
        if i:
            id_book = model.get_value(i, 0)
            nm_book = model.get_value(i, 1)
            check = self.db.to_favorite(id_book)
            if check == None: 
                asm_customs.info(self.parent, u'تم إضافة كتاب "{}" للمفضلة'.format(nm_book,))
            self.parent.list_books.load_fav()
    
    def modify_data(self, *a):
        asm_customs.info(self.parent, 'تم تعديل البيانات بنجاح'); return
    
    def remove_group(self,*a):
        model, i = self.sel_group.get_selected()
        id_group = model.get_value(i, 0)
        nm_group = model.get_value(i, 1)
        if i:
            msg = asm_customs.sure(self.parent, u'''
            سيتم حذف قسم "{}"
            مع جميع كتبه، هل تريد الاستمرار ؟
            '''.format(nm_group,))
            if msg == Gtk.ResponseType.YES:
                check = self.db.remove_group(id_group)
                if check == None:
                    rmtree(join(asm_path.BOOK_DIR, nm_group))
                    self.refresh_groups()
       
    def remove_book(self,*a):
        model0, i0 = self.sel_group.get_selected()
        nm_group = model0.get_value(i0, 1)
        model, i = self.sel_book.get_selected()
        if i:
            id_book = model.get_value(i, 0)
            nm_book = model.get_value(i, 1)
            msg = asm_customs.sure(self.parent, u'''
            سيتم حذف كتاب "{}"
            هل تريد الاستمرار ؟
            '''.format(nm_book,))
            if msg == Gtk.ResponseType.YES:
                check = self.db.remove_book(id_book)
                if check == None:
                    unlink(join(asm_path.BOOK_DIR, nm_group, nm_book+u'.asm'))
                    self.ok_group()
    
    def ok_book(self, *a):
        model, i = self.sel_book.get_selected()
        if i:
            nm_book = model.get_value(i, 1)
            self.entry_book.set_text(nm_book)
            self.id_book = model.get_value(i, 0)
            self.notebk.set_current_page(1)
    
    def ok_group(self, *a):
        model, i = self.sel_group.get_selected()
        if i:
            id_group = model.get_value(i, 0)
            books = self.db.books_part(id_group)
            self.store_books.clear()
            self.names_list = []
            self.modelfilter = self.store_books.filter_new()
            for a in books:
                self.store_books.append([a[0], a[1]])
                self.names_list.append(a[1])
            self.theword = self.names_list[:]
            self.modelfilter.set_visible_func(self.visible_cb, self.theword) 
            self.tree_books.set_model(self.modelfilter)
            self.notebk.set_current_page(0)
    
    def choose_part(self, parent, msg):
        dlg = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL, Gtk.MessageType.WARNING,
                             Gtk.ButtonsType.YES_NO)
        dlg.set_markup(msg)
        ls = []
        for a in self.db.all_parts():
            ls.append([a[0], a[1]])
        hb, parts_g = asm_customs.combo(ls, u'')
        parts_g.set_active(0)
        self.received_part_name = asm_customs.value_active(parts_g, 1)
        self.received_part_id = asm_customs.value_active(parts_g)
        def sel_part(w):
            self.received_part_name = asm_customs.value_active(parts_g, 1)
            self.received_part_id = asm_customs.value_active(parts_g)
        parts_g.connect('changed', sel_part)
        area = dlg.get_content_area()
        area.set_spacing(7)
        hbox = Gtk.HBox(False, 7)
        hbox.pack_end(hb, False, False, 0)
        area.pack_start(hbox, False, False, 0)
        area.show_all()
        r = dlg.run()
        dlg.destroy()
        return r
    
    def merge_group_cb(self, *a):
        model, i = self.sel_group.get_selected()
        id_old = model.get_value(i, 0)
        old_group = model.get_value(i, 1)
        if i:
            msg = self.choose_part(self.parent, 'هل تريد دمج القسم المحدد مع هذا القسم ؟')
            if msg == Gtk.ResponseType.YES:
                for v in listdir(join(asm_path.BOOK_DIR, old_group)):
                    copyfile(join(asm_path.BOOK_DIR, old_group, v),
                              join(asm_path.BOOK_DIR, self.received_part_name, v))
                self.db.merge_group(id_old, self.received_part_id)
                rmtree(join(asm_path.BOOK_DIR, old_group))
                self.refresh_groups()
    
    def move_book_cb(self, *a):
        model0, i0 = self.sel_group.get_selected()
        old_group = model0.get_value(i0, 1)
        model, i = self.sel_book.get_selected()
        if i:
            msg = self.choose_part(self.parent, 'هل تريد نقل الكتاب المحدد إلى هذا القسم ؟')
            if msg == Gtk.ResponseType.YES:
                id_book = model.get_value(i, 0)
                nm_book = model.get_value(i, 1)
                self.db.change_group(id_book, self.received_part_id)
                copyfile(join(asm_path.BOOK_DIR, old_group, nm_book+u'.asm'), 
                         join(asm_path.BOOK_DIR, self.received_part_name, nm_book+u'.asm'))
                unlink(join(asm_path.BOOK_DIR, old_group, nm_book+u'.asm'))
                asm_customs.info(self.parent, u'تم نقل الكتاب "{}" إلى قسم "{}"'.format(nm_book, self.received_part_name))
                self.ok_group()
      
    def refresh_groups(self, *a):
        self.store_group.clear()
        for a in self.db.all_parts():
            self.store_group.append([a[0], a[1]])
        self.parent.list_books.load_list()
    
    def new_group(self, *a):
        new_grp = self.entry_group.get_text()
        if new_grp == '': return
        if exists(join(asm_path.BOOK_DIR, new_grp)): return
        check = self.db.add_part(new_grp)
        if type(check) == int:
            if not exists(join(asm_path.BOOK_DIR, new_grp)):
                mkdir(join(asm_path.BOOK_DIR, new_grp))
            self.refresh_groups()
        self.entry_group.set_text('')
            
    def rename_group(self, *a):
        new_grp = self.entry_group.get_text()
        if new_grp == '': return
        model, i = self.sel_group.get_selected()
        id_group = model.get_value(i, 0)
        if i:
            nm_group = model.get_value(i, 1)
        check = self.db.rename_part(new_grp, nm_group)
        if check == None:
            rename(join(asm_path.BOOK_DIR, nm_group), join(asm_path.BOOK_DIR, new_grp))
            self.refresh_groups()
    
    def move_group(self, btn, v):
        model, i = self.sel_group.get_selected()
        if i:
            if v == 1:
                i0 = model.iter_next(i)
                model.move_after(i, i0)
            if v == -1:
                i0 = model.iter_previous(i)
                model.move_before(i, i0)
        ls = []
        b = 0
        for a in self.store_group:
            b += 1
            ls.append([b, a[1]])
        self.db.organiz_groups(ls)
      
    def rename_book(self, *a):
        model0, i0 = self.sel_group.get_selected()
        nm_group = model0.get_value(i0, 1)
        model, i = self.sel_book.get_selected()
        if i:
            nm_book = model.get_value(i, 1)
            new_bk = self.entry_book.get_text()
            if new_bk == '' or new_bk == nm_book: return
            check = self.db.rename_book(new_bk, nm_book)
            self.db.rename_book_in_main(join(asm_path.BOOK_DIR, nm_group, nm_book+u'.asm'), new_bk)
            if check == None:
                rename(join(asm_path.BOOK_DIR, nm_group, nm_book+u'.asm'), 
                       join(asm_path.BOOK_DIR, nm_group, new_bk+u'.asm'))
    
    def edit_tafsir_cb(self, *a):
        book = self.db.file_book(self.id_book)
        info = self.db.info_book(book)
        if info[8] != 1:
            msg = asm_customs.sure(self.parent, 'هذا الكتاب ليس تفسيرا هل تريد جعله كذلك')
            if msg == Gtk.ResponseType.YES:
                self.db.make_tafsir(book, self.id_book)
            else:
                return
        EditTafsir(self.parent, self.id_book)
    
    def editbk_cb(self, *a):
        self.parent.editbook.close_db()
        self.parent.notebook.set_current_page(7)
        book = self.db.file_book(self.id_book)
        self.parent.editbook.add_book(book, self.id_book, 1)
    
    def empty_book_cb(self, *a):
        model, i = self.sel_group.get_selected()
        if i:
            nm_group = model.get_value(i, 1)
            id_part = model.get_value(i, 0)
            new_bk = self.entry_group.get_text()
            if new_bk == '' :
                asm_customs.erro(self.parent, 'أدخل اسم الكتاب أولا')
                return
            db = join(asm_path.BOOK_DIR, nm_group, new_bk+u'.asm')
            if exists(db):
                asm_customs.erro(self.parent, 'يوجد كتاب بنفس الاسم في هذا القسم')
                return
            self.db.empty_book(db)
            self.db.add_book(new_bk, id_part)
            asm_customs.info(self.parent, 'تم إضافة كتاب فارغ')
        
    def build(self,*a): 
        Gtk.Box.__init__(self,spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
        hp1 = Gtk.HPaned()
        self.pack_start(hp1, True, True, 0)
        self.tree_group = Gtk.TreeView()
        self.tree_group.set_name('Tree')
        self.sel_group = self.tree_group.get_selection()
        self.tree_group.connect("cursor-changed", self.ok_group)
        cell = Gtk.CellRendererText()
        cell.set_property("ellipsize", Pango.EllipsizeMode.END)
        kal = Gtk.TreeViewColumn('الأقسام', cell, text=1)
        self.tree_group.append_column(kal)
        self.store_group = Gtk.ListStore(int, str)
        self.tree_group.set_model(self.store_group)
        self.refresh_groups()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_group)
        scroll.set_size_request(150, -1)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        hp1.pack1(scroll, True, True)

        self.store_books = Gtk.ListStore(int, str)
        self.tree_books = Gtk.TreeView()
        self.tree_books.set_name('Tree')
        self.tree_books.connect("cursor-changed", self.ok_book)
        self.sel_book = self.tree_books.get_selection()
        self.tree_books.set_grid_lines(Gtk.TreeViewGridLines.HORIZONTAL)
        cell = Gtk.CellRendererText()
        cell.set_property("ellipsize", Pango.EllipsizeMode.END)
        books = Gtk.TreeViewColumn('الكتب', cell, text=1)
        self.tree_books.append_column(books)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_books)
        scroll.set_size_request(250, -1)
        hp1.pack2(scroll, True, True)
            
        self.notebk = Gtk.Notebook()
        self.notebk.set_show_tabs(False)
        vb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        vb.set_border_width(5)
        self.entry_group = Gtk.Entry()
        self.entry_group.set_placeholder_text('أدخل اسما!')
        vb.pack_start(self.entry_group, False, False, 0)
        
        btn_new_g = Gtk.Button('قسم جديد')
        btn_new_g.connect('clicked', self.new_group)
        vb.pack_start(btn_new_g, False, False, 0)    

        btn_rn_g = Gtk.Button('تغيير اسم')
        btn_rn_g.connect('clicked', self.rename_group)
        vb.pack_start(btn_rn_g, False, False, 0)
        
        btn_rm_g = Gtk.Button('حذف قسم')
        btn_rm_g.connect('clicked', self.remove_group)
        vb.pack_start(btn_rm_g, False, False, 0)
        
        btn_up_g = Gtk.Button('حرك لأعلى')
        btn_up_g.connect('clicked', self.move_group, -1)
        vb.pack_start(btn_up_g, False, False, 0)
        
        btn_down_g = Gtk.Button('حرك لأسفل')
        btn_down_g.connect('clicked', self.move_group, 1)
        vb.pack_start(btn_down_g, False, False, 0)
        
        btn_merge_g = Gtk.Button('دمج قسم')
        btn_merge_g.connect('clicked', self.merge_group_cb)
        vb.pack_start(btn_merge_g, False, False, 0)
        
        btn_empty_book = Gtk.Button('كتاب فارغ')
        btn_empty_book.connect('clicked', self.empty_book_cb)
        vb.pack_start(btn_empty_book, False, False, 0)
        self.notebk.append_page(vb, Gtk.Label('القسم'))
        
        vb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        vb.set_border_width(5)
        self.entry_book = Gtk.Entry()
        self.entry_book.set_placeholder_text('أدخل اسما!')
        vb.pack_start(self.entry_book, False, False, 0)
        
        self.btn_rn_book = Gtk.Button('تغيير اسم')
        self.btn_rn_book.connect('clicked', self.rename_book)
        vb.pack_start(self.btn_rn_book, False, False, 0)

        self.btn_rm_book = Gtk.Button('حذف كتاب')
        self.btn_rm_book.connect('clicked', self.remove_book)
        vb.pack_start(self.btn_rm_book, False, False, 0)

        btn_fav_b = Gtk.Button('تفضيل كتاب')
        btn_fav_b.connect('clicked', self.add_to_favory)
        vb.pack_start(btn_fav_b, False, False, 0)
        
        self.btn_move_book = Gtk.Button('نقل كتاب')
        self.btn_move_book.connect('clicked', self.move_book_cb)
        vb.pack_start(self.btn_move_book, False, False, 0)
        
        self.btn_info_book = Gtk.Button('بطاقة كتاب')
        self.btn_info_book.connect('clicked', lambda *a: EditBitaka(self.parent, self.id_book))
        vb.pack_start(self.btn_info_book, False, False, 0)
        
        self.btn_edit_book = Gtk.Button('تحرير كتاب')
        self.btn_edit_book.connect('clicked', self.editbk_cb)
        vb.pack_start(self.btn_edit_book, False, False, 0)
        
        self.btn_tafsir = Gtk.Button('تحرير تفسير')
        self.btn_tafsir.connect('clicked', self.edit_tafsir_cb)
        vb.pack_start(self.btn_tafsir, False, False, 0)
        
        self.notebk.append_page(vb, Gtk.Label('الكتاب'))
        self.notebk.set_size_request(250, -1)
        self.pack_start(self.notebk, False, False, 0)
        self.set_border_width(3)
        self.show_all()
        