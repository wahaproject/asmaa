# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from os.path import join, exists
import os
from shutil import copyfile, rmtree
from Asmaa.asm_contacts import listDB
from gi.repository import Gtk ,Gdk
import Asmaa.asm_path as asm_path
import Asmaa.asm_config as asm_config
import Asmaa.asm_customs as asm_customs
from Asmaa.asm_add import AddBooks
from Asmaa.asm_count import Count
from Asmaa.asm_edit_html import EditHTML
from Asmaa.asm_about import About


# class نافذة التفضيلات----------------------------------------------------------       
        
class Preference(Gtk.Dialog):
    
    def __init__(self, parent):
        self.parent = parent
        self.db = listDB()
        self.mycount = Count()
        self.build()        
    
    def refresh(self, *a):
        n = self.parent.viewerbook.get_n_pages()
        for a in range(n):
            ch = self.parent.viewerbook.get_nth_page(a)
            ch.change_font()
        v = self.parent.notebook.get_n_pages()
        for c in range(v):
            if c in [4, 5]:
                ch = self.parent.notebook.get_nth_page(c)
                ch.change_font()
            elif c ==3:
                n = self.parent.winspage.get_n_pages()
                for a in range(n):
                    ch = self.parent.winspage.get_nth_page(a)
                    ch.change_font()
    
    def specified(self, cbox):
        if cbox.get_active() == 0:
            self.frame.set_sensitive(False)
            asm_config.setv('theme', 0)
            #asm_customs.info(self.parent, "سوف تحتاج إلى إعادة تشغيل المكتبة")
        elif cbox.get_active() == 1:
            self.frame.set_sensitive(False)
            asm_config.setv('theme', 1)
        elif cbox.get_active() == 2:
            self.frame.set_sensitive(False)
            asm_config.setv('theme', 2)
        else:
            self.frame.set_sensitive(True)
            asm_config.setv('theme', 3)
        self.parent.theme.refresh()
        self.refresh()
    
    def switch_page(self, btn):
        if btn.get_active():
            if btn.get_name()== u"theme":
                self.notebook.set_current_page(0)
                self.wins_btn.set_active(False)
                self.prop_btn.set_active(False)
                self.path_btn.set_active(False)
                self.modifie_btn.set_active(False)
                self.info_btn.set_active(False)
            elif btn.get_name()== u"wins":
                self.notebook.set_current_page(1)
                self.path_btn.set_active(False)
                self.modifie_btn.set_active(False)
                self.theme_btn.set_active(False)
                self.prop_btn.set_active(False)
                self.info_btn.set_active(False)
            elif btn.get_name()== u"path":
                self.notebook.set_current_page(2)
                self.wins_btn.set_active(False)
                self.modifie_btn.set_active(False)
                self.theme_btn.set_active(False)
                self.prop_btn.set_active(False)
                self.info_btn.set_active(False)
            elif btn.get_name()== u"prop":
                self.notebook.set_current_page(3)
                self.wins_btn.set_active(False)
                self.path_btn.set_active(False)
                self.theme_btn.set_active(False)
                self.modifie_btn.set_active(False)
                self.info_btn.set_active(False)
            elif btn.get_name()== u"modifie":
                self.notebook.set_current_page(4)
                self.wins_btn.set_active(False)
                self.path_btn.set_active(False)
                self.theme_btn.set_active(False)
                self.prop_btn.set_active(False)
                self.info_btn.set_active(False)
            elif btn.get_name()== u"info":
                self.notebook.set_current_page(5)
                self.wins_btn.set_active(False)
                self.path_btn.set_active(False)
                self.theme_btn.set_active(False)
                self.prop_btn.set_active(False)
                self.modifie_btn.set_active(False)
    
    def ch_font(self, btn):
        nconf = btn.get_name()
        dialog = Gtk.FontChooserDialog("اختر خطا", self.parent)
        dialog.set_font(asm_config.getv(nconf))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            font = dialog.get_font()
            asm_config.setv(nconf, font)
        dialog.destroy()
        self.parent.theme.refresh()
        
    def ch_color(self, btn):
        nconf = btn.get_name()
        dialog = Gtk.ColorChooserDialog("اختر لونا", self.parent)
        dialog.set_rgba(asm_customs.rgba(asm_config.getv(nconf)))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            color = dialog.get_rgba().to_string()
            asm_config.setv(nconf, color)
        dialog.destroy()
        self.parent.theme.refresh()
    
    def change_vls(self, btn, nm):
        v = btn.get_active()
        asm_config.setv(nm, v)
    
    def change_path_db(self, *a):
        open_dlg = Gtk.FileChooserDialog(u'تغيير مسار قاعدة البيانات',
                                         self.parent, Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                         Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        
        Filter = Gtk.FileFilter()
        Filter.set_name(u"قاعدة البيانات")
        Filter.add_pattern("Listbooks.db")
        open_dlg.add_filter(Filter)
        
        res = open_dlg.run()
        if res == Gtk.ResponseType.OK:
            asm_config.setv('path', open_dlg.get_filenames()[0])          
            asm_customs.info(self.parent, u'يرجى إعادة تشغيل المكتبة ليتغير المسار فعليا!')
        open_dlg.destroy()
    
    def new_db(self,*a): 
        save_dlg = Gtk.FileChooserDialog(u'مسار قاعدة البيانات الجديدة', self.parent,
                                    Gtk.FileChooserAction.SELECT_FOLDER,
                                    (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        res = save_dlg.run()
        if res == Gtk.ResponseType.OK:
            new_dir = join(save_dlg.get_filename(), u'مكتبة أسماء')
            if os.path.exists(join(new_dir, u'data', u'Listbooks.db')):
                asm_customs.erro(self.parent, u'يوجد مكتبة في هذا الدليل بالفعل')
            else: 
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)
                if not os.path.exists(join(new_dir, u'data')):
                    os.mkdir(join(new_dir, u'data'))
                if not os.path.exists(join(new_dir, u'books')):
                    os.mkdir(join(new_dir, u'books'))
                if not os.path.exists(join(new_dir, u'index')):
                    os.mkdir(join(new_dir, u'index'))
                self.db.new_db(join(new_dir, 'data', 'Listbooks.db'))
                asm_customs.info(self.parent, u'تم إضافة مكتبة مفرغة جديدة')
        save_dlg.destroy()
    
    def saved_session_cb(self, *a):
        if self.saved_session.get_active():
            asm_config.setv('saved_session', 1)
        else:
            asm_config.setv('saved_session', 0)
            
    def numbers_cb(self, *a):
        if self.numbers.get_active():
            asm_config.setv('nmbrs', 1)
        else:
            asm_config.setv('nmbrs', 0)
    
    def style_browse_cb(self, btn):
        v = btn.get_active()
        asm_config.setv('style_browse', v)
        self.parent.viewerbook.convert_browse()
        
    def time_browse_cb(self, btn):
        v = btn.get_active()
        asm_config.setv('time_browse', v)
        self.parent.viewerbook.convert_browse()
        
    def auto_browse_cb(self, btn):
        v = btn.get_active_text()
        asm_config.setv('auto_browse', int(v))
        self.parent.viewerbook.convert_browse()
              
    def active_mouse_browse_cb(self, *a):
        if self.active_mouse_browse.get_active():
            asm_config.setv('mouse_browse', 1)
        else:
            asm_config.setv('mouse_browse', 0)
        self.parent.viewerbook.convert_browse()
    
    def copy_to_home_cb(self, *a):
        groups = self.db.all_parts()
        for g in groups:
            if not exists(join(asm_path.BOOK_DIR_rw, g[1])):
                os.mkdir(join(asm_path.BOOK_DIR_rw, g[1]))
            books = self.db.books_part(g[0])
            for b in books:
                book_old = self.db.file_book(b[0])
                self.db.mode_write(b[0])
                book_new = self.db.file_book(b[0])
                if not exists(book_new):
                    copyfile(book_old, book_new)
        asm_customs.info(self.parent, 'تمت عملية النسخ بنجاح')
        self.copy_to_home.set_sensitive(False)
    
    def count_cb(self, *a):
        n_group = len(self.db.all_parts())
        n_book = self.db.n_books()
        asm_customs.info(self.parent, 'عدد الأقسام : {}\nعدد الكتب : {}'.format(n_group,n_book))
    
    def count_fast(self, *a):
        self.file_html = self.mycount.fast()
        self.open_file()
        
    def count_detail(self, *a):
        self.file_html = self.mycount.detail()
        self.open_file()
        
    def rv_index_cb(self, *a):
        check = self.db.remove_index()
        if check == None:
            rmtree(join(asm_path.INDEX_DIR_rw, 'my_index'))
        asm_customs.info(self.parent, 'تم مسح الفهرس .')
    
    def open_file(self, *a):
        dlg = Gtk.Dialog(parent=self.parent)
        box = dlg.vbox
        dlg.set_icon_name("asmaa")
        dlg.set_default_size(1000, 700)
        dlg.set_title('إحصاء الكتب')
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        self.view_html = EditHTML()
        self.view_html.open_html(self.file_html)
        close_btn = Gtk.Button("إغلاق")
        close_btn.connect('clicked',lambda *a: dlg.destroy())
        self.view_html.hb_tb.pack_end(close_btn, False, False, 0)
        box.pack_start(self.view_html, True, True, 0)
        dlg.show_all()
    
    def build(self,*a):
        Gtk.Dialog.__init__(self, parent=self.parent)
        self.set_default_size(500, 400)
        vbox1 = self.vbox
        vbox = Gtk.Box(spacing=0,orientation=Gtk.Orientation.HORIZONTAL)
        hb_bar = Gtk.HeaderBar()
        hb_bar.set_show_close_button(True)
        self.set_titlebar(hb_bar)
        hb_bar.set_custom_title(vbox)
        Gtk.StyleContext.add_class(vbox.get_style_context(), "linked")
        vbox.set_border_width(3)
        self.notebook = Gtk.Notebook()
        self.notebook.set_show_tabs(False)
        
        box = Gtk.Box(spacing=5, orientation=Gtk.Orientation.VERTICAL)
        box1 = Gtk.Box(spacing=4, orientation=Gtk.Orientation.VERTICAL)
        box1.set_border_width(5)
        self.frame = Gtk.Frame()
        box.set_border_width(5)
        ls = [u'بدون', u'مقترح', u'متباين', u'مخصص']
        style_btn = Gtk.ComboBoxText()
        for a in ls:
            style_btn.append_text(a)
        style_btn.connect("changed", self.specified)
        style_btn.set_active(asm_config.getn('theme'))
        hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(Gtk.Label('النمط'), False, False, 0)
        hb.pack_end(style_btn, False, False, 0)
        box.pack_start(hb, False, False, 0)
        box.pack_start(self.frame, True, True, 0)
       
        list_w1 = [[u'قائمة الأقسام','_prts'], [u'قائمة الكتب','_bks'], [u'القوائم الجانبية','_idx'], [u'نصوص الكتاب','_nass'], 
                   [u'النص القرآني', '_qrn'], [u'نصوص أخرى','_oth'], [u'العناوين','_tit']]
        list_w2 = [[u'لون خلفية العرض','_bg'], [u'خلفية النص القرآني', '_bg_qrn'], [u'لون خلفية القوائم','_bgs', 
                   [u'لون خط التحديد','_sel'], [u'لون خلفية التحديد','_bg_sel'], [u'لون تحديد البحث','_fnd']]]
        
        for a in list_w1:
            hbox = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
            btn1 = Gtk.ToolButton(stock_id = Gtk.STOCK_SELECT_FONT)
            btn1.set_name('font'+a[1])
            btn1.connect('clicked',self.ch_font)
            btn2 = Gtk.ToolButton(stock_id = Gtk.STOCK_SELECT_COLOR)
            btn2.set_name('color'+a[1])
            btn2.connect('clicked',self.ch_color)
            hbox.pack_start(Gtk.Label(a[0]), False, False, 0)
            hbox.pack_end(btn2, False, False, 0)
            hbox.pack_end(btn1, False, False, 0)
            box1.pack_start(hbox, False, False, 0)
            
        for a in list_w2:
            hbox = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
            btn = Gtk.ToolButton(stock_id = Gtk.STOCK_SELECT_COLOR)
            btn.set_name('color'+a[1])
            btn.connect('clicked',self.ch_color)
            hbox.pack_start(Gtk.Label(a[0]), False, False, 0)
            hbox.pack_end(btn, False, False, 0)
            box1.pack_start(hbox, False, False, 0)
            
        ref = Gtk.Button("تحديث الواجهة")
        ref.connect('clicked', lambda *a: self.parent.theme.refresh())
        ref.connect('clicked', self.refresh)
        box.pack_end(ref, False, False, 0)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(box1)
        self.frame.add(scroll)
        self.notebook.append_page(box, Gtk.Label('خط ولون'))
        
        box = Gtk.VBox(False, 6)
        box.set_border_width(6) 
        btn_win_organize = Gtk.Button('تعديل المكتبة')
        btn_win_organize.connect('clicked', lambda *a: self.parent.notebook.set_current_page(8))
        box.pack_start(btn_win_organize, False, False, 0)
        
        btn_win_siana = Gtk.Button('نافذة الصيانة')
        btn_win_siana.connect('clicked', lambda *a: SianaWin(self.parent))
        box.pack_start(btn_win_siana, False, False, 0)
        
        btn_win_add = Gtk.Button('نافذة الاستيراد')
        btn_win_add.connect('clicked', lambda *a: AddBooks(self.parent))
        box.pack_start(btn_win_add, False, False, 0)
        
        btn_win_export = Gtk.Button('نافذة التصدير')
        btn_win_export.set_sensitive(False)
        #btn_win_export.connect('clicked', lambda *a: AddBooks(self.parent))
        box.pack_start(btn_win_export, False, False, 0)
        
        btn_win_index = Gtk.Button('نافذة الفهرسة')
        #btn_win_index.set_sensitive(False)
        try:
            from Asmaa.asm_indexer import WinIndexer
            btn_win_index.connect('clicked', lambda *a: WinIndexer(self.parent))
        except: pass
        box.pack_start(btn_win_index, False, False, 0)
        self.notebook.append_page(box, Gtk.Label('النوافذ'))

        box = Gtk.VBox(False, 6)
        box.set_border_width(6) 
        self.add_db = Gtk.Button('إنشاء مكتبة مفرّغة')
        self.add_db.connect('clicked', self.new_db)
        box.pack_start(self.add_db, False, False, 0)
        
        self.b_dest = Gtk.Button('تغيير مسار المكتبة')
        self.b_dest.connect('clicked', self.change_path_db)  
        self.b_path = Gtk.Button('عرض المسار الحاليّ')
        self.b_path.connect('clicked', lambda *a: asm_customs.info(self.parent, asm_config.getv('path')))  
        box.pack_start(self.b_dest, False, False, 0)
        box.pack_start(self.b_path, False, False, 0)
        
        self.copy_to_home = Gtk.Button('نسخ المكتبة  إلى المنزل')
        self.copy_to_home.set_tooltip_text('هذا الخيار إذا كانت كتب المكتبة في الدليل :\n"/usr/share/asmaa/"')
        if self.db.check_books_library() == False:
            self.copy_to_home.set_sensitive(False) 
        self.copy_to_home.connect('clicked', self.copy_to_home_cb)
        box.pack_start(self.copy_to_home, False, False, 0)      
        self.notebook.append_page(box, Gtk.Label('المسار'))
        
        box = Gtk.VBox(False, 6)
        box.set_border_width(5)
        
        self.saved_session = Gtk.CheckButton('حفظ الجلسة عند الإغلاق')
        box.pack_start(self.saved_session, False, False, 0)
        if asm_config.getn('saved_session') == 1: self.saved_session.set_active(True)
        else: self.saved_session.set_active(False)
        self.saved_session.connect("toggled", self.saved_session_cb)
        
        self.active_mouse_browse = Gtk.CheckButton('التصفح بعجلة الفأرة')
        box.pack_start(self.active_mouse_browse, False, False, 0)
        if asm_config.getn('mouse_browse') == 1: self.active_mouse_browse.set_active(True)
        else: self.active_mouse_browse.set_active(  False)
        self.active_mouse_browse.connect("toggled", self.active_mouse_browse_cb)
        
        ls = [u'بدون', u'اختفاء وظهور', u'زحلقة أفقية', u'زحلقة عمودية']
        style_browse = Gtk.ComboBoxText()
        for a in ls:
            style_browse.append_text(a)
        style_browse.connect("changed", self.style_browse_cb)
        style_browse.set_active(asm_config.getn('style_browse'))
        hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(Gtk.Label('نمط التصفح'), False, False, 0)
        hb.pack_end(style_browse, False, False, 0)
        box.pack_start(hb, False, False, 0)
        
        ls = [u'0.1', u'0.2', u'0.5', u'1', u'1.5', u'2', u'3']
        time_browse = Gtk.ComboBoxText()
        for a in ls:
            time_browse.append_text(a)
        time_browse.connect("changed", self.time_browse_cb)
        time_browse.set_active(asm_config.getn('time_browse'))
        hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(Gtk.Label('زمن التصفح بالثواني'), False, False, 0)
        hb.pack_end(time_browse, False, False, 0)
        box.pack_start(hb, False, False, 0)
        
        ls = [u'1', u'2', u'3', u'4', u'5', u'10']
        auto_browse = Gtk.ComboBoxText()
        for a in ls:
            auto_browse.append_text(a)
        auto_browse.connect("changed", self.auto_browse_cb)
        idx = ls.index(str(asm_config.getv('auto_browse')), )
        auto_browse.set_active(idx)
        hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(Gtk.Label('سرعة الاستعراض الآلي'), False, False, 0)
        hb.pack_end(auto_browse, False, False, 0)
        box.pack_start(hb, False, False, 0)
        
        self.numbers = Gtk.CheckButton('استعمال أرقام المغاربة')
        box.pack_start(self.numbers, False, False, 0)
        if asm_config.getn('nmbrs') == 1: self.numbers.set_active(True)
        else: self.numbers.set_active(False)
        self.numbers.connect("toggled", self.numbers_cb)
        self.notebook.append_page(box, Gtk.Label('خيارات'))
                
        box = Gtk.VBox(False, 6)
        box.set_border_width(6)
        self.rv_index = Gtk.Button('حذف الفهارس')
        self.rv_index.connect('clicked', self.rv_index_cb)
        box.pack_start(self.rv_index, False, False, 0)
        self.notebook.append_page(box, Gtk.Label('العمليات'))
        
        box = Gtk.VBox(False, 6)
        box.set_border_width(6)
        self.n_books_parts = Gtk.Button('عدد الكتب')
        self.n_books_parts.connect('clicked', self.count_cb)
        box.pack_start(self.n_books_parts, False, False, 0)
        self.rapid_count = Gtk.Button('إحصاء سريع')
        self.rapid_count.connect('clicked', self.count_fast)
        self.detail_count = Gtk.Button('إحصاء مفصل')
        self.detail_count.connect('clicked', self.count_detail)
        box.pack_start(self.rapid_count, False, False, 0)
        box.pack_start(self.detail_count, False, False, 0)
        
        btn_about = Gtk.Button('حول المكتبة')
        btn_about.connect('clicked', lambda *a: About(self.parent))
        box.pack_start(btn_about, False, False, 0)
        
        btn_help = Gtk.Button('صفحة المساعدة')
        btn_help.connect('clicked', lambda *a: self.parent.notebook.set_current_page(5))
        box.pack_start(btn_help, False, False, 0)
        
        web_page = Gtk.LinkButton.new_with_label("http://sourceforge.net/projects/asmaalibrary/files/",
                                                'صفحة البرنامج على الشّبكة')
        box.pack_start(web_page, False, False, 0)
        
        db_void = Gtk.LinkButton.new_with_label("http://sourceforge.net/projects/asmaalibrary/files/AsmaaLibrary.tar.gz/download",
                                                'تنزيل قاعدة بيانات للتجربة')
        
        box.pack_start(db_void, False, False, 0)
        self.notebook.append_page(box, Gtk.Label('المعلومات'))
        
        vbox1.pack_start(self.notebook, True, True, 0)
        
        self.theme_btn = Gtk.ToggleButton()
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_SELECT_COLOR, Gtk.IconSize.LARGE_TOOLBAR)
        self.theme_btn.set_image(img)
        self.theme_btn.set_name('theme')
        self.theme_btn.set_active(True)
        self.theme_btn.connect("clicked", self.switch_page)
        vbox.pack_start(self.theme_btn, False, False, 0)
        
        self.wins_btn = Gtk.ToggleButton()
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_HOME, Gtk.IconSize.LARGE_TOOLBAR)
        self.wins_btn.set_image(img)
        self.wins_btn.set_name('wins')
        self.wins_btn.connect("clicked", self.switch_page)
        vbox.pack_start(self.wins_btn, False, False, 0)
        
        self.path_btn = Gtk.ToggleButton()
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_OPEN, Gtk.IconSize.LARGE_TOOLBAR)
        self.path_btn.set_image(img)
        self.path_btn.set_name('path')
        self.path_btn.connect("clicked", self.switch_page)
        vbox.pack_start(self.path_btn, False, False, 0)
        
        self.prop_btn = Gtk.ToggleButton()
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_PROPERTIES, Gtk.IconSize.LARGE_TOOLBAR)
        self.prop_btn.set_image(img)
        self.prop_btn.set_name('prop')
        self.prop_btn.connect("clicked", self.switch_page)
        vbox.pack_start(self.prop_btn, False, False, 0)
        
        self.modifie_btn = Gtk.ToggleButton()
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_PREFERENCES, Gtk.IconSize.LARGE_TOOLBAR)
        self.modifie_btn.set_image(img)
        self.modifie_btn.set_name('modifie')
        self.modifie_btn.connect("clicked", self.switch_page)
        vbox.pack_start(self.modifie_btn, False, False, 0)
        
        self.info_btn = Gtk.ToggleButton()
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_INFO, Gtk.IconSize.LARGE_TOOLBAR)
        self.info_btn.set_image(img)
        self.info_btn.set_name('info')
        self.info_btn.connect("clicked", self.switch_page)
        vbox.pack_start(self.info_btn, False, False, 0)
        
        self.show_all()

class SianaWin (Gtk.Dialog):
    
    def star_siana(self, btn):
        btn.set_sensitive(False)
        self.db.repair(self.store_repair, self.progress_repair)
        btn.set_sensitive(True)
    
    def __init__(self, parent):
        self.parent = parent
        self.db = listDB()
        Gtk.Dialog.__init__(self, parent=self.parent)
        
        hb_bar = Gtk.HeaderBar()
        hb_bar.set_show_close_button(True)
        hb_bar.set_title('صيانة وإصلاح المكتبة')
        self.set_titlebar(hb_bar)
        
        Box = self.vbox
        Box.set_spacing(5)
        self.set_border_width(3)
        self.set_size_request(420, 350)
        self.progress_repair = Gtk.ProgressBar()
        self.store_repair = Gtk.ListStore(str)
        self.tree_repair = Gtk.TreeView()
        sah1 = Gtk.TreeViewColumn('نتائج الفحص',Gtk.CellRendererText(),text = 0)
        self.tree_repair.append_column(sah1)
        self.tree_repair.set_model(self.store_repair)
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.tree_repair)
        Box.pack_start(scroll, True, True, 0)
        Box.pack_start(self.progress_repair, False, False, 0)
        siana = Gtk.Button("صيانة")
        siana.connect('clicked', self.star_siana)
        hb_bar.pack_start(siana)
        self.show_all()
        