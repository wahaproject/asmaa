# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from os.path import join, exists, expanduser
from shutil import copyfile, copytree
import os
from shutil import copyfile, rmtree
from asm_contacts import listDB
from gi.repository import Gtk ,Gdk
import asm_path
import asm_config
import asm_customs
from asm_add import AddBooks
from asm_count import Count
from asm_edit_html import EditHTML
from asm_about import About

 
#===============================================================
class Preference(Gtk.Stack):
    
    def __init__(self, parent):
        Gtk.Stack.__init__(self)
        self.set_border_width(7)
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
        v = cbox.get_active()
        if v == 6: 
            self.btn_specific.set_no_show_all(True)
            self.btn_specific.hide()
            self.vbox_color.set_no_show_all(False)
            self.vbox_color.show_all()
        else: 
            self.btn_specific.set_no_show_all(False)
            self.btn_specific.show_all()
            self.vbox_color.set_no_show_all(True)
            self.vbox_color.hide()
        asm_config.setv('theme', v)
        self.parent.refresh()
    
    def switch_page(self, btn):
        if btn.get_active():
            if btn.get_name()== "theme":
                self.notebook.set_current_page(0)
                self.wins_btn.set_active(False)
                self.prop_btn.set_active(False)
                self.path_btn.set_active(False)
                self.modifie_btn.set_active(False)
                self.info_btn.set_active(False)
            elif btn.get_name()== "wins":
                self.notebook.set_current_page(1)
                self.path_btn.set_active(False)
                self.modifie_btn.set_active(False)
                self.theme_btn.set_active(False)
                self.prop_btn.set_active(False)
                self.info_btn.set_active(False)
            elif btn.get_name()== "path":
                self.notebook.set_current_page(2)
                self.wins_btn.set_active(False)
                self.modifie_btn.set_active(False)
                self.theme_btn.set_active(False)
                self.prop_btn.set_active(False)
                self.info_btn.set_active(False)
            elif btn.get_name()== "prop":
                self.notebook.set_current_page(3)
                self.wins_btn.set_active(False)
                self.path_btn.set_active(False)
                self.theme_btn.set_active(False)
                self.modifie_btn.set_active(False)
                self.info_btn.set_active(False)
            elif btn.get_name()== "modifie":
                self.notebook.set_current_page(4)
                self.wins_btn.set_active(False)
                self.path_btn.set_active(False)
                self.theme_btn.set_active(False)
                self.prop_btn.set_active(False)
                self.info_btn.set_active(False)
            elif btn.get_name()== "info":
                self.notebook.set_current_page(5)
                self.wins_btn.set_active(False)
                self.path_btn.set_active(False)
                self.theme_btn.set_active(False)
                self.prop_btn.set_active(False)
                self.modifie_btn.set_active(False)
    
    def ch_font(self, btn):
        nconf = btn.get_name()
        font = btn.get_font()
        asm_config.setv(nconf, font)
        self.parent.refresh()
        
    def ch_color(self, btn):
        nconf = btn.get_name()
        color = btn.get_rgba().to_string()
        asm_config.setv(nconf, color)
        self.parent.refresh()
    
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
        res = asm_customs.sure(self.parent, 'قد تحتاج هذه العملية إذا كان لديك قاعدة بيانات\nفي مسار لا تملك الصلاحيات \
للتعديل عليها فيه\nهل تريد المواصلة ؟')
        if res == -8:
            if not exists(expanduser('~/مكتبة أسماء')):
                os.mkdir(expanduser('~/مكتبة أسماء'))
            if not exists(join(expanduser('~/مكتبة أسماء'), 'books')):
                os.mkdir(join(expanduser('~/مكتبة أسماء'), 'books'))
            groups = self.db.all_parts()
            for g in groups:
                copytree(join(asm_path.LIBRARY_DIR, 'books', g[1]), join(expanduser('~/مكتبة أسماء'), 'books', g[1]))
            copytree(join(asm_path.LIBRARY_DIR, 'data'), join(expanduser('~/مكتبة أسماء'), 'data'))
            copytree(join(asm_path.LIBRARY_DIR, 'index'), join(expanduser('~/مكتبة أسماء'), 'index'))
            asm_customs.info(self.parent, 'تمت عملية النسخ بنجاح')
            res = asm_customs.sure(self.parent, 'قد تحتاج تغيير المسار إلى القاعدة الجديدة\nهل تريد فعل ذلك ؟')
            if res == -8:
                asm_config.setv('path', join(expanduser('~/مكتبة أسماء'), 'data', 'Listbooks.db'))    
                asm_customs.info(self.parent, "سوف تحتاج إلى إعادة تشغيل مكتبة أسماء")
    
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
            rmtree(join(asm_path.INDEX_DIR, 'my_index'))
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
    
    def cheeck_page(self, btn, v):
        if asm_path.can_modify(self.parent):
            if v == 1: 
                if asm_path.can_modify(self.parent):
                    self.parent.notebook.set_current_page(8)
            elif v == 2: 
                if asm_path.can_modify(self.parent):
                    SianaWin(self.parent)
            elif v == 3: 
                if asm_path.can_modify(self.parent):
                    AddBooks(self.parent)
            elif v == 4: 
                if asm_path.can_modify(self.parent):
                    WinIndexer(self.parent)
        
    def set_btns_color(self, *a):
        for a in self.vbox_color.get_children():
            self.vbox_color.remove(a)
        list_colors = [[u'قائمة الأقسام','_lists_parts'], [u'قائمة الكتب','_lists_books'], [u'القوائم الجانبية','_lists_titles'], 
                   [u'نصوص الكتاب','_nasse_books'], [u'النص القرآني', '_quran'], [u'نصوص أخرى','_nasse_others'], [u'العناوين','_anawin'],
                   [u'التحديد','_selected'], [u'المرور','_hover'], [u'البحث','_searched']]
        for a in list_colors:
            hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
            btn0 = Gtk.ColorButton.new_with_rgba(asm_customs.rgba(asm_config.getv('color{}'.format(a[1]))))
            btn0.set_name('color{}'.format(a[1]))
            btn0.connect('color-set',self.ch_color)
            self.list_btn_colors.append(btn0)
            #------------------------------------------------------
            btn1 = Gtk.ColorButton.new_with_rgba(asm_customs.rgba(asm_config.getv('background{}'.format(a[1]))))
            btn1.set_name('background{}'.format(a[1]))
            btn1.connect('color-set',self.ch_color)
            self.list_btn_colors.append(btn1)
            hbox.pack_end(btn1, False, False, 0)
            hbox.pack_end(btn0, False, False, 0)
            hbox.pack_start(Gtk.Label(a[0]), False, False, 0)
            self.vbox_color.pack_start(hbox, False, False, 0)
        self.vbox_color.show_all()
    
    def specific_cb(self, *a): 
        asm_config.setv('color_lists_parts', self.parent.theme.color_lists_parts)
        asm_config.setv('color_lists_books', self.parent.theme.color_lists_books)
        asm_config.setv('color_nasse_books', self.parent.theme.color_nasse_books)
        asm_config.setv('color_nasse_others', self.parent.theme.color_nasse_others)
        asm_config.setv('color_anawin', self.parent.theme.color_anawin)
        asm_config.setv('color_lists_titles', self.parent.theme.color_lists_titles)
        asm_config.setv('color_quran', self.parent.theme.color_quran)
        asm_config.setv('background_quran', self.parent.theme.background_quran)
        asm_config.setv('background_lists_parts', self.parent.theme.background_lists_parts)
        asm_config.setv('background_lists_books', self.parent.theme.background_lists_books)
        asm_config.setv('background_nasse_books', self.parent.theme.background_nasse_books)
        asm_config.setv('background_nasse_others', self.parent.theme.background_nasse_others)
        asm_config.setv('background_anawin', self.parent.theme.background_anawin)
        asm_config.setv('background_lists_titles', self.parent.theme.background_lists_titles)
        asm_config.setv('color_selected', self.parent.theme.color_selected)
        asm_config.setv('background_selected', self.parent.theme.background_selected)
        asm_config.setv('color_searched', self.parent.theme.color_searched)
        asm_config.setv('background_searched', self.parent.theme.background_searched)
        asm_config.setv('color_hover', self.parent.theme.color_hover)
        asm_config.setv('background_hover', self.parent.theme.background_hover)
        self.style_btn.set_active(6)
        self.vbox_color.set_no_show_all(False)
        self.vbox_color.show_all()
        self.btn_specific.set_no_show_all(True)
        self.btn_specific.hide()
        self.set_btns_color()
    
    def build(self,*a):
        self.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.set_transition_duration(300)
        self.list_btn_colors  = []
        #---------------------------
        vb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        
        btn_color = Gtk.ToolButton()
        btn_color.set_label('الألوان')
        vb.pack_start(btn_color, False, False, 0)
        btn_color.connect('clicked', lambda *a: self.set_visible_child_name('n1'))
        btn_font = Gtk.ToolButton()
        btn_font.set_label('الخطوط')
        vb.pack_start(btn_font, False, False, 0)
        btn_font.connect('clicked', lambda *a: self.set_visible_child_name('n2'))

        vb.pack_start(Gtk.Separator(), False, False, 3)
        
        btn_wins = Gtk.ToolButton()
        btn_wins.set_label('النوافذ')
        vb.pack_start(btn_wins, False, False, 0)
        btn_wins.connect('clicked', lambda *a: self.set_visible_child_name('n3'))
        
        btn_option = Gtk.ToolButton()
        btn_option.set_label('العمليات')
        vb.pack_start(btn_option, False, False, 0)
        btn_option.connect('clicked', lambda *a: self.set_visible_child_name('n4'))
        
        btn_prefe = Gtk.ToolButton()
        btn_prefe.set_label('الخيارات')
        vb.pack_start(btn_prefe, False, False, 0)
        btn_prefe.connect('clicked', lambda *a: self.set_visible_child_name('n5'))
        
        vb.pack_start(Gtk.Separator(), False, False, 3)
        
        btn_info = Gtk.ToolButton()
        btn_info.set_label('معلومات')
        vb.pack_start(btn_info, False, False, 0)
        btn_info.connect('clicked', lambda *a: self.set_visible_child_name('n6'))
        
        btn_about = Gtk.ToolButton()
        btn_about.set_label('حول المكتبة')
        btn_about.connect('clicked', lambda *a: About(self.parent))
        vb.pack_start(btn_about, False, False, 0)
        self.add_named(vb, 'n0')
        #----------------------------
        vb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        btn_back = Gtk.ToolButton()
        btn_back.set_label('الرجوع للخيارات')
        vb.pack_start(btn_back, False, False, 0)
        vb.pack_start(Gtk.Separator(), False, False, 3)
        btn_back.connect('clicked', lambda *a: self.set_visible_child_name('n0'))
        ls = ['أصفر' ,'أزرق','أحمر','أخضر','بنفسجي','معتم', 'مخصص']
        self.style_btn = Gtk.ComboBoxText()
        self.style_btn.set_name('style_btn')
        for a in ls:
            self.style_btn.append_text(a)
        self.style_btn.set_active(asm_config.getn('theme'))
        self.style_btn.connect("changed", self.specified)
        hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        
        self.btn_specific = Gtk.Button('تخصيصه')
        self.btn_specific.connect('clicked', self.specific_cb)
        hb.pack_start(self.btn_specific, False, False, 0)
        hb.pack_end(self.style_btn, False, False, 0)
        hb.pack_end(Gtk.Label('الألوان :  '), False, False, 0)
        vb.pack_start(hb, False, False, 0)
        
        self.vbox_color = Gtk.Box(spacing=10,orientation=Gtk.Orientation.VERTICAL)    
        self.vbox_color.set_border_width(10)
        if asm_config.getn('theme') == 6:
            self.btn_specific.set_no_show_all(True)
            self.btn_specific.hide()
        else:
            self.vbox_color.set_no_show_all(True)
            self.vbox_color.hide()
        self.set_btns_color()

        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.NONE)
        scroll.add(self.vbox_color)
        vb.pack_start(scroll, True, True, 0)
        self.add_named(vb, 'n1')
        #----------------------------
        vb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        vb_font = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        btn_back = Gtk.ToolButton()
        btn_back.set_label('الرجوع للخيارات')
        vb.pack_start(btn_back, False, False, 0)
        vb.pack_start(Gtk.Separator(), False, False, 3)
        btn_back.connect('clicked', lambda *a: self.set_visible_child_name('n0'))
        list_fonts = [['خط النافذة','_window'], ['قائمة الأقسام','_lists_parts'], ['قائمة الكتب','_lists_books'], ['القوائم الجانبية','_lists_titles'], ['نص الكتاب','_nasse_books'], 
                   ['نصوص أخرى','_nasse_others'], ['العناوين','_anawin'], ['القرآن الكريم','_quran']]
        for a in list_fonts:
            hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
            btn = Gtk.FontButton.new_with_font(asm_config.getv('font{}'.format(a[1])))
            btn.set_name('font'+a[1])
            btn.connect('font-set',self.ch_font)
            hbox.pack_end(btn, False, False, 0)
            hbox.pack_start(Gtk.Label(a[0]), False, False, 0)
            vb_font.pack_start(hbox, False, False, 0)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.NONE)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.add(vb_font)
        vb.pack_start(scroll, True, True, 0)
        self.add_named(vb, 'n2')
        #----------------------------
        vb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        btn_back = Gtk.ToolButton()
        btn_back.set_label('الرجوع للخيارات')
        vb.pack_start(btn_back, False, False, 0)
        vb.pack_start(Gtk.Separator(), False, False, 3)
        btn_back.connect('clicked', lambda *a: self.set_visible_child_name('n0'))
        
        btn_win_organize = Gtk.ToolButton()
        btn_win_organize.set_label('تعديل المكتبة')
        btn_win_organize.connect('clicked', self.cheeck_page, 1)
        vb.pack_start(btn_win_organize, False, False, 0)
        
        btn_win_siana = Gtk.ToolButton()
        btn_win_siana.set_label('نافذة الصيانة')
        btn_win_siana.connect('clicked', self.cheeck_page, 2)
        vb.pack_start(btn_win_siana, False, False, 0)
        
        btn_win_add = Gtk.ToolButton()
        btn_win_add.set_label('نافذة الاستيراد')
        btn_win_add.connect('clicked', self.cheeck_page, 3)
        vb.pack_start(btn_win_add, False, False, 0)
        
        btn_win_export = Gtk.ToolButton()
        btn_win_export.set_label('نافذة التصدير')
        btn_win_export.set_sensitive(False)
        #btn_win_export.connect('clicked', lambda *a: AddBooks(self.parent))
        vb.pack_start(btn_win_export, False, False, 0)
        
        btn_win_index = Gtk.ToolButton()
        btn_win_index.set_label('نافذة الفهرسة')
        btn_win_index.set_sensitive(False)
        vb.pack_start(btn_win_index, False, False, 0)
        self.add_named(vb, 'n3')
        #----------------------------
        vb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        btn_back = Gtk.ToolButton()
        btn_back.set_label('الرجوع للخيارات')
        vb.pack_start(btn_back, False, False, 0)
        vb.pack_start(Gtk.Separator(), False, False, 3)
        btn_back.connect('clicked', lambda *a: self.set_visible_child_name('n0'))

        self.add_db = Gtk.ToolButton()
        self.add_db.set_label('إنشاء مكتبة مفرّغة')
        self.add_db.connect('clicked', self.new_db)
        vb.pack_start(self.add_db, False, False, 0)
        
        self.b_dest = Gtk.ToolButton()
        self.b_dest.set_label('تغيير مسار المكتبة')
        self.b_dest.connect('clicked', self.change_path_db)  
        self.b_path = Gtk.ToolButton()
        self.b_path.set_label('عرض المسار الحاليّ')
        self.b_path.connect('clicked', lambda *a: asm_customs.info(self.parent, asm_config.getv('path')))  
        vb.pack_start(self.b_dest, False, False, 0)
        vb.pack_start(self.b_path, False, False, 0)
        
        self.copy_to_home = Gtk.ToolButton()
        self.copy_to_home.set_label('نسخ المكتبة  إلى المنزل')
        self.copy_to_home.set_tooltip_text('هذا الخيار إذا كانت كتب المكتبة في دليل :\nلا يمكن الكتابة فيه')
        self.copy_to_home.connect('clicked', self.copy_to_home_cb)
        vb.pack_start(self.copy_to_home, False, False, 0)      
        self.add_named(vb, 'n4')
        #----------------------------
        vb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        btn_back = Gtk.ToolButton()
        btn_back.set_label('الرجوع للخيارات')
        vb.pack_start(btn_back, False, False, 0)
        vb.pack_start(Gtk.Separator(), False, False, 3)
        btn_back.connect('clicked', lambda *a: self.set_visible_child_name('n0'))
        
        self.saved_session = Gtk.CheckButton('حفظ الجلسة عند الإغلاق')
        vb.pack_start(self.saved_session, False, False, 0)
        if asm_config.getn('saved_session') == 1: self.saved_session.set_active(True)
        else: self.saved_session.set_active(False)
        self.saved_session.connect("toggled", self.saved_session_cb)
        
        self.active_mouse_browse = Gtk.CheckButton('التصفح بعجلة الفأرة')
        vb.pack_start(self.active_mouse_browse, False, False, 0)
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
        vb.pack_start(hb, False, False, 0)
        
        ls = [u'0.1', u'0.2', u'0.5', u'1', u'1.5', u'2', u'3']
        time_browse = Gtk.ComboBoxText()
        for a in ls:
            time_browse.append_text(a)
        time_browse.connect("changed", self.time_browse_cb)
        time_browse.set_active(asm_config.getn('time_browse'))
        hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(Gtk.Label('زمن التصفح بالثواني'), False, False, 0)
        hb.pack_end(time_browse, False, False, 0)
        vb.pack_start(hb, False, False, 0)
        
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
        vb.pack_start(hb, False, False, 0)
        
        self.numbers = Gtk.CheckButton('استعمال أرقام المغاربة')
        vb.pack_start(self.numbers, False, False, 0)
        if asm_config.getn('nmbrs') == 1: self.numbers.set_active(True)
        else: self.numbers.set_active(False)
        self.numbers.connect("toggled", self.numbers_cb)

        self.add_named(vb, 'n5')
        #----------------------------
        vb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        btn_back = Gtk.ToolButton()
        btn_back.set_label('الرجوع للخيارات')
        vb.pack_start(btn_back, False, False, 0)
        vb.pack_start(Gtk.Separator(), False, False, 3)
        btn_back.connect('clicked', lambda *a: self.set_visible_child_name('n0'))

        self.n_books_parts = Gtk.ToolButton()
        self.n_books_parts.set_label('عدد الكتب')
        self.n_books_parts.connect('clicked', self.count_cb)
        vb.pack_start(self.n_books_parts, False, False, 0)
        self.rapid_count = Gtk.ToolButton()
        self.rapid_count.set_label('إحصاء سريع')
        self.rapid_count.connect('clicked', self.count_fast)
        self.detail_count = Gtk.ToolButton()
        self.detail_count.set_label('إحصاء مفصل')
        self.detail_count.connect('clicked', self.count_detail)
        vb.pack_start(self.rapid_count, False, False, 0)
        vb.pack_start(self.detail_count, False, False, 0)
        
        web_page = Gtk.LinkButton.new_with_label("http://sourceforge.net/projects/asmaalibrary/files/",
                                                'صفحة البرنامج على الشّبكة')
        vb.pack_start(web_page, False, False, 0)
        
        db_void = Gtk.LinkButton.new_with_label("http://sourceforge.net/projects/asmaalibrary/files/AsmaaLibrary.tar.gz/download",
                                                'تنزيل قاعدة بيانات للتجربة')
        
        vb.pack_start(db_void, False, False, 0)
        self.add_named(vb, 'n6')

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
        