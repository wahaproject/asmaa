# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from os.path import join
from gi.repository import Gtk, Gdk
import Asmaa.asm_customs as asm_customs
import Asmaa.asm_path as asm_path
import Asmaa.asm_config as asm_config
from Asmaa.asm_preference import Preference
from Asmaa.asm_theme import MyTheme
from Asmaa.asm_viewer import ViewerBooks, OpenBook
from Asmaa.asm_listbook import ListBooks
from Asmaa.asm_otherwins import OtherWins
from Asmaa.asm_tafsir import Tafsir
from Asmaa.asm_marks import SavedMarks
from Asmaa.asm_result import SavedResult
from Asmaa.asm_search import Searcher
from Asmaa.asm_waraka import Warakat
from Asmaa.asm_moshaf import ViewerMoshaf
from Asmaa.asm_tablabel import TabLabel
from Asmaa.asm_edit_book import EditBook
from Asmaa.asm_edit_bitaka import EditBitaka
from Asmaa.asm_contacts import listDB
from Asmaa.asm_organize import Organize


Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL)
ACCEL_CTRL_KEY, ACCEL_CTRL_MOD = Gtk.accelerator_parse("<Ctrl>")
ACCEL_SHFT_KEY, ACCEL_SHFT_MOD = Gtk.accelerator_parse("<Shift>")
ACCEL_ALT_KEY, ACCEL_ALT_MOD = Gtk.accelerator_parse("<Alt>")


#a--------------------------------------------------
try: greet = Gtk.Window(Gtk.WindowType.POPUP)
except: 
    greet = Gtk.Window()
    greet.set_title("مرحبا !")
greet.set_border_width(15)
greet.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
greet.set_size_request(400,300)
vb = Gtk.VBox(False, 10)
img_greet = Gtk.Image()
img_greet.set_from_file(join(asm_path.ICON_DIR,"greet.png"))
vb.pack_start(img_greet, False, False, 0)
vb.pack_start(Gtk.Label('الإصدار {}\nجارٍ تحميل برنامج مكتبة أسماء....'.format(asm_customs.version, ))
              , False, False, 0)
greet.add(vb)
greet.show_all()
while (Gtk.events_pending()): Gtk.main_iteration()
     
# class الرئيس--------------------------------------------------------
        
class AsmaaApp(Gtk.Window):    
    
    # a البحث في النافذة الحالية----------------------------------
    
    def search_on_page(self, *a):
        text = self.entry_search.get_text() 
        if len(text) == 1 or text == u"ال": return
        n = self.notebook.get_current_page()
        ch = self.notebook.get_nth_page(n)
        ch.search_on_page(text)
    
    def search_on_active(self, *a):
        text = self.entry_search.get_text() 
        n = self.notebook.get_current_page()
        ch = self.notebook.get_nth_page(n)
        ch.search_on_active(text)
            
    # a تغيير طريقة عرض قائمة الكتب--------------------------
    
    def change_view(self, *a):
        if self.list_books.nb.get_current_page() in [0, 1]:
            self.list_books.nb.set_current_page(2)
            asm_config.setv('view_books', 1)
            self.show_icons.set_label("عرض بالأيقونات")
        elif self.list_books.nb.get_current_page() in [2, 3]:
            self.list_books.nb.set_current_page(0)
            asm_config.setv('view_books', 0)
            self.show_icons.set_label("عرض بالقائمة")
        self.go_parts.hide()
    
    # a إظهار وإخفاء اللوح الجانبي--------------------------
    
    def show_side(self, *a):
        if asm_config.getn('show_side') == 0:
            self.list_books.vbox_side.hide()
            asm_config.setv('show_side', 1)
        else:
            self.list_books.vbox_side.show_all()
            asm_config.setv('show_side', 0)
    
    # a حفظ موضع من كتاب----------------------------------
    
    def site_in_book(self, *a):
        list_marks = eval(asm_config.getv('marks'))
        if self.notebook.get_current_page() == 1:
            n = self.viewerbook.get_current_page()
            ch =self.viewerbook.get_nth_page(n)
            list_marks.append([ch.all_in_page[1], ch.nm_book, ch.id_book])
            marks = repr(list_marks)
            asm_config.setv('marks', marks)
            asm_customs.info(self, u'تم تعليم هذا الموضع')
    
    # a  إضافة الكتاب المفتوح إلى المفضلة--------------------
    
    def add_to_favory(self, *a):
        if self.notebook.get_current_page() == 1:
            n = self.viewerbook.get_current_page()
            ch = self.viewerbook.get_nth_page(n)
            check = ch.db_list.to_favorite(ch.id_book)
            if check == None: asm_customs.info(self, u'تم إضافة كتاب "{}" للمفضلة'.format(ch.nm_book,))
            self.list_books.load_fav()
    
    # a عند التبديل بين نوافذ المكتبة-------------------------------
    
    def back_to_previous_page(self, *a):
        if len(self.opened) == 1: return
        del self.opened[-1]
        if self.opened[-1] == 7: 
            del self.opened[-1]
        self.notebook.set_current_page(self.opened[-1])
    
    def switch_page(self, widget, page, n):
        if n in self.opened: 
            self.opened.remove(n)
        self.opened.append(n)
        self.btn_action_edit.hide()
        self.btn_action_book.hide()
        self.btn_action_list.hide()
        if n == 0:
            self.btn_action_list.show_all()
            self.entry_search.set_placeholder_text('بحث عن كتاب')
            if self.list_books.nb.get_current_page() in [1, 3]:
                self.go_parts.show_all()
            else:
                self.go_parts.hide()
        elif n == 8:
            self.entry_search.set_placeholder_text('بحث عن كتاب')
        elif n == 1:
            self.btn_action_book.show_all()
            self.entry_search.set_placeholder_text('بحث في النّصّ')
        elif n == 7:
            self.btn_action_edit.show_all()
            self.entry_search.set_placeholder_text('بحث في النّصّ')
        elif n == 3:
            ss = [u"بحث عن كلمة",u"بحث عن راوٍ",u"بحث عن مؤلف"]
            text = ss[self.winspage.get_current_page()]
            self.entry_search.set_placeholder_text(text)
        elif n == 2:
            self.entry_search.set_placeholder_text('بحث في القرآن')
        else:
            self.entry_search.set_placeholder_text('بحث في النّصّ')
        if n in [1,2,4,5,7]: self.btnbox_pages.show_all()
        else: self.btnbox_pages.hide()
        if n!= 0: self.go_parts.hide()
        else: self.btnbox_pages.hide()
#        self.pref_btn.set_active(False)
    
            
    # a التصفح--------------------------------------------
   
    def back_to_old(self, *a):
        n = self.notebook.get_current_page()
        ch = self.notebook.get_nth_page(n)
        ch.back_to_old()
        
    def advance_to_new(self, *a):
        n = self.notebook.get_current_page()
        ch = self.notebook.get_nth_page(n)
        ch.advance_to_new()

    def first_page(self, *a):
        n = self.notebook.get_current_page()
        ch = self.notebook.get_nth_page(n)
        ch.first_page()
    
    def previous_page(self, *a):
        n = self.notebook.get_current_page()
        ch = self.notebook.get_nth_page(n)
        ch.previous_page()
    
    def next_page(self, *a):
        n = self.notebook.get_current_page()
        ch = self.notebook.get_nth_page(n)
        ch.next_page()
    
    def last_page(self, *a):
        n = self.notebook.get_current_page()
        ch = self.notebook.get_nth_page(n)
        ch.last_page()
    
    def opened_book(self, *a):
        if self.viewerbook.get_n_pages() == 0:
            return
        else:
            self.notebook.set_current_page(1)
    
    def full_screen(self, *a):
        if self.full == 1:
            self.unfullscreen()
            self.full = 0
        else:
            self.fullscreen()
            self.full = 1
        
    def delete_event_cb(self, *a):
        asm_config.setv('quran_pos', self.moshafpage.page_id)
        session = []
        session.append(self.viewerbook.session)
        session.append(self.opened)
        saved = repr(session)
        asm_config.setv('start_session', saved)
        n = self.viewerbook.get_n_pages()
        for a in range(n):
            ch = self.viewerbook.get_nth_page(a)
            try: ch.db_list.set_last(ch.all_in_page[1], ch.id_book)
            except: pass
        Gtk.main_quit()
        
    def start_session(self, *a):
        session = eval(asm_config.getv('start_session'))
        if asm_config.getn('saved_session') == 0: return
        if session[1][-1] == 1: 
            if self.viewerbook.get_n_pages() == 0: self.notebook.set_current_page(session[1][-2])
            else: self.notebook.set_current_page(session[1][-1])
        elif session[1][-1] in [0, 2, 3, 4, 5, 6, 8]:
            self.notebook.set_current_page(session[1][-1])
        else:
            self.notebook.set_current_page(session[1][-2])
        if session[0] == []: return
        for id_book in session[0][0]:
            book = self.db.file_book(id_book)
            sr = OpenBook(self, book, id_book)
            self.viewerbook.append_page(sr,TabLabel(sr, self.db.tit_book(id_book)[1]))
            sr.set_index()
            sr.scroll_search.hide()
        self.viewerbook.set_current_page(session[0][1])
    
    
    def set_tashkil(self, *a):
        if asm_config.getn('tashkil') == 0: 
            asm_config.setv('tashkil', 1)
            self.del_tashkil.set_label("حذف التّشكيل")
        else: 
            asm_config.setv('tashkil', 0)
            self.del_tashkil.set_label("إعادة التّشكيل")
        self.viewerbook.set_tashkil()
            
        
    def __init__(self,*a):
        self.full = 0
        self.opened = [0]
        self.db = listDB()
        self.entry_search = Gtk.SearchEntry()
        Gtk.Window.__init__(self)
        self.axl = Gtk.AccelGroup()
        self.add_accel_group(self.axl)
        self.theme = MyTheme()
        self.search_win = Searcher(self)
        self.list_books = ListBooks(self)
        self.viewerbook = ViewerBooks(self)
        self.tafsirpage = Tafsir(self)
        self.warakapage = Warakat(self)
        self.editbook = EditBook(self)
        self.help_book = OpenBook(self, asm_path.DALIL_DB, -1)
        self.winspage = OtherWins(self)
        self.help_book.set_border_width(3)
        self.help_book.comment_btn.set_sensitive(False)
        self.help_book.set_index()
        self.moshafpage = ViewerMoshaf(self)
        self.organize = Organize(self)
        #-------------------------------
        self.build()

# a البناء-------------------------------------------------------------------- 
    
    def build(self,*a):
        #self.set_title("مكتبة أسماء")
        self.set_icon_name('asmaa')
        self.maximize()
        #self.set_opacity(1.0)
        #self.set_default_size(800, 600)
        self.connect("delete_event", self.delete_event_cb)
        self.connect("destroy", self.delete_event_cb)
        self.box = Gtk.Box(spacing=5, orientation=Gtk.Orientation.VERTICAL)
        
        hb_bar = Gtk.HeaderBar()
        hb_bar.set_show_close_button(True)
        self.set_titlebar(hb_bar)

        menu_wins = Gtk.Menu()      
        win_quran = Gtk.ImageMenuItem("القرآن الكريم")
        win_quran.add_accelerator("activate", self.axl, Gdk.KEY_F1, 0, Gtk.AccelFlags.VISIBLE)
        img = Gtk.Image()
        img.set_from_file(join(asm_path.ICON_DIR, 'Quran-16.png'))
        win_quran.set_image(img)
        win_quran.connect('activate', lambda *a: self.notebook.set_current_page(2))
        win_tafsir = Gtk.ImageMenuItem("التفاسير")
        win_tafsir.add_accelerator("activate", self.axl, Gdk.KEY_F2, 0, Gtk.AccelFlags.VISIBLE)
        img = Gtk.Image()
        img.set_from_file(join(asm_path.ICON_DIR, 'Tafsir-16.png'))
        win_tafsir.set_image(img)
        win_tafsir.connect('activate', lambda *a: self.notebook.set_current_page(4))
        win_list = Gtk.ImageMenuItem("قائمة الكتب")
        win_list.add_accelerator("activate", self.axl, Gdk.KEY_F3, 0, Gtk.AccelFlags.VISIBLE)
        img = Gtk.Image()
        img.set_from_file(join(asm_path.ICON_DIR, 'Books-16.png'))
        win_list.set_image(img)
        win_list.connect('activate', lambda *a: self.notebook.set_current_page(0))
        win_opened = Gtk.ImageMenuItem("الكتب المفتوحة")
        win_opened.add_accelerator("activate", self.axl, Gdk.KEY_F4, 0, Gtk.AccelFlags.VISIBLE)
        img = Gtk.Image()
        img.set_from_file(join(asm_path.ICON_DIR, 'Book-Open-16.png'))
        win_opened.set_image(img)
        win_opened.connect('activate', self.opened_book)
        win_waraka = Gtk.ImageMenuItem("أوراق البحث")
        win_waraka.add_accelerator("activate", self.axl, Gdk.KEY_F5, 0, Gtk.AccelFlags.VISIBLE)
        img = Gtk.Image()
        img.set_from_file(join(asm_path.ICON_DIR, 'Papers-16.png'))
        win_waraka.set_image(img)
        win_waraka.connect('activate', lambda *a: self.notebook.set_current_page(6))
        win_special = Gtk.ImageMenuItem("نوافذ خاصة")
        win_special.add_accelerator("activate", self.axl, Gdk.KEY_F6, 0, Gtk.AccelFlags.VISIBLE)
        img = Gtk.Image()
        img.set_from_file(join(asm_path.ICON_DIR, 'Wins-16.png'))
        win_special.set_image(img)
        win_special.connect('activate', lambda *a: self.notebook.set_current_page(3))
        win_help = Gtk.ImageMenuItem("صفحة المساعدة")
        win_help.add_accelerator("activate", self.axl, Gdk.KEY_F7, 0, Gtk.AccelFlags.VISIBLE)
        img = Gtk.Image()
        img.set_from_file(join(asm_path.ICON_DIR, 'Help-16.png'))
        win_help.set_image(img)
        win_help.connect('activate', lambda *a: self.notebook.set_current_page(5))
        full_screen = Gtk.ImageMenuItem("ملء الشاشة")
        full_screen.add_accelerator("activate", self.axl, Gdk.KEY_F11, 0, Gtk.AccelFlags.VISIBLE)
        full_screen.connect('activate', self.full_screen)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_FULLSCREEN, Gtk.IconSize.MENU)
        full_screen.set_image(img)
        exit1 = Gtk.ImageMenuItem("خروج")
        exit1.add_accelerator("activate", self.axl, Gdk.KEY_Q, ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE)
        img = Gtk.Image()
        img.set_from_file(join(asm_path.ICON_DIR, 'exit-16.png'))
        exit1.set_image(img)
        exit1.connect('activate', Gtk.main_quit)
        menu_wins.append(win_quran)
        menu_wins.append(win_tafsir)
        menu_wins.append(win_list)
        menu_wins.append(win_opened)
        menu_wins.append(win_waraka)
        menu_wins.append(win_special)
        menu_wins.append(win_help)
        menu_wins.append(Gtk.SeparatorMenuItem())
        menu_wins.append(full_screen) 
        menu_wins.append(exit1)
        btn_menu = Gtk.MenuButton();
        btn_menu.set_popup (menu_wins);
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_HOME, Gtk.IconSize.BUTTON)
        btn_menu.set_image(img)
        menu_wins.show_all();
        
        hb_bar.pack_start(btn_menu)

        
        btnbox_action = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(btnbox_action.get_style_context(), "linked")
        
        find_btn = Gtk.Button()
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_FIND, Gtk.IconSize.BUTTON)
        find_btn.set_image(img)
        find_btn.set_tooltip_text('نافذة البحث')
        find_btn.connect('clicked', lambda *a: self.search_win.show_all())
        btnbox_action.pack_start(find_btn, False, False, 0)
        
        menu_saveds = Gtk.Menu()   
        win_marks = Gtk.ImageMenuItem("نافذة العلامات المرجعيّة")
        win_marks.connect('activate', lambda *a: SavedMarks(self))
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_PASTE, Gtk.IconSize.MENU)
        win_marks.set_image(img)
        menu_saveds.append(win_marks)     
        win_results = Gtk.ImageMenuItem("نافذة البحوث المحفوظة")
        win_results.connect('activate', lambda *a: SavedResult(self))
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_GO_UP, Gtk.IconSize.MENU)
        win_results.set_image(img)
        menu_saveds.append(win_results)
        btn_saveds = Gtk.MenuButton();
        btn_saveds.set_popup (menu_saveds);
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_SAVE, Gtk.IconSize.BUTTON)
        btn_saveds.set_image(img)
        menu_saveds.show_all();
        btnbox_action.pack_start(btn_saveds, False, False, 0)
        
        # a أحداث صفحة الكتاب المفتوح--------------------------------------
        
        menu_action_book = Gtk.Menu()      
        go_old = Gtk.ImageMenuItem("الذهاب إلى التصفح الأقدم")
        go_old.connect('activate', self.back_to_old)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_GO_DOWN, Gtk.IconSize.MENU)
        go_old.set_image(img)
        menu_action_book.append(go_old)     
        go_new = Gtk.ImageMenuItem("الذهاب إلى التصفح الأحدث")
        go_new.connect('activate', self.advance_to_new)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_GO_UP, Gtk.IconSize.MENU)
        go_new.set_image(img)
        menu_action_book.append(go_new)
        menu_action_book.append(Gtk.SeparatorMenuItem())
        add_fav = Gtk.ImageMenuItem("أضف الكتاب إلى المفضّلة")
        add_fav.connect('activate', self.add_to_favory)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_SAVE, Gtk.IconSize.MENU)
        add_fav.set_image(img)
        menu_action_book.append(add_fav)     
        sav_mark = Gtk.ImageMenuItem("حفظ موضع الصّفحة الحاليّة")
        sav_mark.connect('activate', self.site_in_book)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_PASTE, Gtk.IconSize.MENU)
        sav_mark.set_image(img)
        menu_action_book.append(sav_mark)     
        menu_action_book.append(Gtk.SeparatorMenuItem())
        self.del_tashkil = Gtk.ImageMenuItem("حذف التّشكيل")
        if asm_config.getn('tashkil') == 0:  self.del_tashkil.set_label("إعادة التّشكيل")
        self.del_tashkil.connect('activate', self.set_tashkil)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_FILE, Gtk.IconSize.MENU)
        self.del_tashkil.set_image(img)
        menu_action_book.append(self.del_tashkil)
        
        menu_action_book.append(Gtk.SeparatorMenuItem())
        win_prefs = Gtk.ImageMenuItem("التفضيلات")
        win_prefs.connect("activate", lambda *a: Preference(self))
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_PREFERENCES, Gtk.IconSize.MENU)
        win_prefs.set_image(img)
        menu_action_book.append(win_prefs)
        self.btn_action_book = Gtk.MenuButton();
        self.btn_action_book.set_popup (menu_action_book);
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_EXECUTE, Gtk.IconSize.BUTTON)
        self.btn_action_book.set_image(img)
        menu_action_book.show_all();
        btnbox_action.pack_start(self.btn_action_book, False, False, 0)
        
        # a أحداث صفحة قائمة الكتب--------------------------------------
        
        menu_action_list = Gtk.Menu()          
        self.show_icons = Gtk.ImageMenuItem.new_with_label("عرض بالأيقونات")
        self.show_icons.add_accelerator("activate", self.axl, Gdk.KEY_S, ACCEL_CTRL_MOD, 
                       Gtk.AccelFlags.VISIBLE)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_FILE, Gtk.IconSize.MENU)
        self.show_icons.set_image(img)
        menu_action_list.append(self.show_icons)
        if asm_config.getn('view_books') == 0: self.show_icons.set_label("عرض بالقائمة")
        else: self.show_icons.set_label("عرض بالأيقونات")
        self.show_icons.connect('activate', self.change_view)
        menu_action_list.append(Gtk.SeparatorMenuItem())
        side_panel = Gtk.ImageMenuItem("إخفاء/عرض اللوح الجانبي")
        side_panel.connect('activate', self.show_side)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_CLEAR, Gtk.IconSize.MENU)
        side_panel.set_image(img)
        menu_action_list.append(side_panel)  
        menu_action_list.append(Gtk.SeparatorMenuItem())
        organize = Gtk.ImageMenuItem("تنظيم المكتبة")
        organize.connect('activate', lambda *a: self.notebook.set_current_page(8))
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_EDIT, Gtk.IconSize.MENU)
        organize.set_image(img)
        menu_action_list.append(organize)     
        
        menu_action_list.append(Gtk.SeparatorMenuItem())
        win_prefs = Gtk.ImageMenuItem("التفضيلات")
        win_prefs.connect("activate", lambda *a: Preference(self))
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_PREFERENCES, Gtk.IconSize.MENU)
        win_prefs.set_image(img)
        menu_action_list.append(win_prefs)
        self.btn_action_list = Gtk.MenuButton();
        self.btn_action_list.set_popup (menu_action_list);
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_EXECUTE, Gtk.IconSize.BUTTON)
        self.btn_action_list.set_image(img)
        menu_action_list.show_all();
        btnbox_action.pack_start(self.btn_action_list, False, False, 0)
        
        # a أحداث صفحة تحرير الكتاب--------------------------------------
        
        menu_action_edit = Gtk.Menu()          
        find_replace = Gtk.ImageMenuItem("إيجاد واستبدال")
        find_replace.connect('activate', self.editbook.replace_all)
        find_replace.add_accelerator("activate", self.axl, Gdk.KEY_F, ACCEL_CTRL_MOD, 
                       Gtk.AccelFlags.VISIBLE)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_FIND_AND_REPLACE, Gtk.IconSize.MENU)
        find_replace.set_image(img)
        menu_action_edit.append(find_replace)
        back_old_text = Gtk.ImageMenuItem("أرجع النص الأصلي")
        back_old_text.add_accelerator("activate", self.axl, Gdk.KEY_Z, ACCEL_CTRL_MOD, 
                       Gtk.AccelFlags.VISIBLE)
        back_old_text.connect('activate', self.editbook.undo_cb)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_UNDO, Gtk.IconSize.MENU)
        back_old_text.set_image(img)
        menu_action_edit.append(back_old_text)  
        menu_action_edit.append(Gtk.SeparatorMenuItem())
        change_info = Gtk.ImageMenuItem.new_with_label("تغيير معلومات الكتاب")
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_INFO, Gtk.IconSize.MENU)
        change_info.set_image(img)
        menu_action_edit.append(change_info)
        change_info.connect('activate', lambda *a: EditBitaka(self, self.editbook.id_book))
        menu_action_edit.append(Gtk.SeparatorMenuItem())
        save_changed = Gtk.ImageMenuItem("حفظ التغييرات في الكتاب")
        save_changed.add_accelerator("activate", self.axl, Gdk.KEY_S, ACCEL_CTRL_MOD, 
                       Gtk.AccelFlags.VISIBLE)
        save_changed.connect('activate', self.editbook.save_book)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_SAVE, Gtk.IconSize.MENU)
        save_changed.set_image(img)
        menu_action_edit.append(save_changed)  
        show_normal = Gtk.ImageMenuItem("عرض الكتاب في الوضع العاديّ")
        show_normal.connect('activate', self.editbook.show_book)
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_FILE, Gtk.IconSize.MENU)
        show_normal.set_image(img)
        menu_action_edit.append(show_normal)  
         
        self.btn_action_edit = Gtk.MenuButton();
        self.btn_action_edit.set_popup (menu_action_edit);
        img = Gtk.Image()
        img.set_from_stock(Gtk.STOCK_EXECUTE, Gtk.IconSize.BUTTON)
        self.btn_action_edit.set_image(img)
        menu_action_edit.show_all();
        btnbox_action.pack_start(self.btn_action_edit, False, False, 0)
        hb_bar.pack_start(btnbox_action)
        
        #------------------------------------
        self.go_parts = Gtk.Button()
        self.go_parts.set_size_request(64, -1)
        self.go_parts.set_tooltip_text("الرجوع إلى الأقسام الرّئيسة")
        self.go_parts.connect('clicked', lambda *a: self.list_books.back_cb())
        img = Gtk.Image()
        icon_theme = Gtk.IconTheme.get_default ()
        has = icon_theme.has_icon("gtk-go-back-rtl")
        if  has: 
            img.set_from_icon_name('gtk-go-back-rtl', Gtk.IconSize.BUTTON)
        else:
            img.set_from_stock(Gtk.STOCK_GO_FORWARD, Gtk.IconSize.BUTTON)
        self.go_parts.set_image(img)
        hb_bar.pack_start(self.go_parts)
        
        # a أزرار التصفح---------------------------------------
            
        self.btnbox_pages = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.btnbox_pages.get_style_context(), "linked")
        #-----------------------------
        first_page = Gtk.Button()
        img = Gtk.Image()
        has = icon_theme.has_icon("gtk-goto-first-rtl")
        if  has: 
            img.set_from_icon_name('gtk-goto-first-rtl', Gtk.IconSize.BUTTON)
        else:
            img.set_from_stock(Gtk.STOCK_GOTO_LAST, Gtk.IconSize.BUTTON)
        first_page.set_image(img)
        first_page.set_tooltip_text('الصفحة الأولى')
        first_page.connect('clicked', self.first_page)
        first_page.add_accelerator("clicked",self.axl, Gdk.KEY_Up, ACCEL_ALT_MOD, Gtk.AccelFlags.VISIBLE)
        self.btnbox_pages.pack_start(first_page, False, False, 0)
        #--------------------------------------
        prev_page = Gtk.Button()
        img = Gtk.Image()
        has = icon_theme.has_icon("gtk-go-back-rtl")
        if  has: 
            img.set_from_icon_name('gtk-go-back-rtl', Gtk.IconSize.BUTTON)
        else:
            img.set_from_stock(Gtk.STOCK_GO_FORWARD, Gtk.IconSize.BUTTON)
        prev_page.set_image(img)
        prev_page.set_tooltip_text('الصفحة السابقة')
        prev_page.connect('clicked', self.previous_page)
        prev_page.add_accelerator("clicked",self.axl, Gdk.KEY_Right, ACCEL_ALT_MOD, Gtk.AccelFlags.VISIBLE)
        self.btnbox_pages.pack_start(prev_page, False, False, 0)
        #--------------------------------------
        next_page = Gtk.Button()
        img = Gtk.Image()
        has = icon_theme.has_icon("gtk-go-forward-rtl")
        if  has: 
            img.set_from_icon_name('gtk-go-forward-rtl', Gtk.IconSize.BUTTON)
        else:
            img.set_from_stock(Gtk.STOCK_GO_BACK, Gtk.IconSize.BUTTON)
        next_page.set_image(img)
        next_page.set_tooltip_text('الصفحة التالية')
        next_page.connect('clicked', self.next_page)
        next_page.add_accelerator("clicked",self.axl, Gdk.KEY_Left, ACCEL_ALT_MOD, Gtk.AccelFlags.VISIBLE)
        self.btnbox_pages.pack_start(next_page, False, False, 0)
        #--------------------------------------
        last_page = Gtk.Button()
        img = Gtk.Image()
        has = icon_theme.has_icon("gtk-goto-last-rtl")
        if  has: 
            img.set_from_icon_name('gtk-goto-last-rtl', Gtk.IconSize.BUTTON)
        else:
            img.set_from_stock(Gtk.STOCK_GOTO_FIRST, Gtk.IconSize.BUTTON)
        last_page.set_image(img)
        last_page.set_tooltip_text('الصفحة الأخيرة')
        last_page.connect('clicked', self.last_page)
        last_page.add_accelerator("clicked",self.axl, Gdk.KEY_Down, ACCEL_ALT_MOD, Gtk.AccelFlags.VISIBLE)
        self.btnbox_pages.pack_start(last_page, False, False, 0)
        hb_bar.set_custom_title(self.btnbox_pages)
        
        self.entry_search.set_placeholder_text('بحث عن كتاب')
        self.entry_search.connect('changed', self.search_on_page)
        self.entry_search.connect('activate', self.search_on_active)
        
        hb_bar.pack_end(self.entry_search)
        
        # a--------------------------------
        self.notebook = Gtk.Notebook()
        self.notebook.set_show_tabs(False)
        self.notebook.append_page(self.list_books, Gtk.Label('0'))
        self.notebook.append_page(self.viewerbook, Gtk.Label('1'))
        self.notebook.append_page(self.moshafpage, Gtk.Label('2'))
        self.notebook.append_page(self.winspage, Gtk.Label('3'))
        self.notebook.append_page(self.tafsirpage, Gtk.Label('4'))
        self.notebook.append_page(self.help_book, Gtk.Label('5'))
        self.notebook.append_page(self.warakapage, Gtk.Label('6'))
        self.notebook.append_page(self.editbook, Gtk.Label('7'))
        self.notebook.append_page(self.organize, Gtk.Label('8'))
        self.notebook.connect("switch-page", self.switch_page)
        self.notebook.set_scrollable(True)
        self.notebook.set_show_tabs(False)

        self.box.pack_start(self.notebook, True, True, 0)

    
        self.axl.connect(Gdk.KEY_F11, 0, Gtk.AccelFlags.VISIBLE, self.full_screen)
        self.axl.connect(Gdk.KEY_F9, 0, Gtk.AccelFlags.VISIBLE, self.viewerbook.hide_index)
        self.axl.connect(Gdk.KEY_BackSpace, ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE, self.back_to_previous_page)
        
        self.axl.connect(Gdk.KEY_F1, 0, Gtk.AccelFlags.VISIBLE, lambda *a: self.notebook.set_current_page(2))
        self.axl.connect(Gdk.KEY_F2, 0, Gtk.AccelFlags.VISIBLE, lambda *a: self.notebook.set_current_page(4))
        self.axl.connect(Gdk.KEY_F3, 0, Gtk.AccelFlags.VISIBLE, lambda *a: self.notebook.set_current_page(0))
        self.axl.connect(Gdk.KEY_F4, 0, Gtk.AccelFlags.VISIBLE, self.opened_book)
        self.axl.connect(Gdk.KEY_F5, 0, Gtk.AccelFlags.VISIBLE, lambda *a: self.notebook.set_current_page(6))
        self.axl.connect(Gdk.KEY_F6, 0, Gtk.AccelFlags.VISIBLE, lambda *a: self.notebook.set_current_page(3))
        self.axl.connect(Gdk.KEY_F7, 0, Gtk.AccelFlags.VISIBLE, lambda *a: self.notebook.set_current_page(5))
        self.axl.connect(Gdk.KEY_Q, ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE, self.delete_event_cb)
        self.axl.connect(Gdk.KEY_S, ACCEL_CTRL_MOD, Gtk.AccelFlags.VISIBLE, self.change_view)
        self.axl.connect(Gdk.KEY_Up, ACCEL_ALT_MOD, Gtk.AccelFlags.VISIBLE, self.first_page)
        self.axl.connect(Gdk.KEY_Down, ACCEL_ALT_MOD, Gtk.AccelFlags.VISIBLE, self.last_page)
        self.axl.connect(Gdk.KEY_Left, ACCEL_ALT_MOD, Gtk.AccelFlags.VISIBLE, self.next_page)
        self.axl.connect(Gdk.KEY_Right, ACCEL_ALT_MOD, Gtk.AccelFlags.VISIBLE, self.previous_page)

        self.add(self.box)
        
        self.show_all()
        if asm_config.getn('search') == 0:
            self.search_win.stack.set_visible_child_name("n1")
        else:
            self.search_win.stack.set_visible_child_name("n2")
        self.btnbox_pages.hide()
        self.btn_action_book.hide()
        self.btn_action_edit.hide()
        self.go_parts.hide()
        self.help_book.scroll_search.hide()
        self.help_book.hp.set_position(120)
        if asm_config.getn('show_side') == 1:
            self.list_books.vbox_side.hide()
        else:
            self.list_books.vbox_side.show_all() 
        greet.destroy()
        try: self.start_session()
        except: pass
#----------------------------------------------------

Asm = AsmaaApp()
def main(): 
    Gtk.main()

if __name__ == "__main__":
    main()
