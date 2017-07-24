# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import Gtk
import asm_customs
from asm_contacts import listDB

class EditBitaka(Gtk.Dialog):
    
    def quit_dlg(self, *a):
        #del self.db
        self.destroy()
    
    def save_cb(self, *a):
        txt_bitaka = self.view_bitaka_bfr.get_text(self.view_bitaka_bfr.get_start_iter(),
                            self.view_bitaka_bfr.get_end_iter(), False)
        txt_info = self.view_info_bfr.get_text(self.view_info_bfr.get_start_iter(),
                            self.view_info_bfr.get_end_iter(), False)
        name = self.ent_name.get_text()
        short_name = self.ent_name_sh.get_text()
        if self.has_shorts.get_active(): is_short = 1
        else: is_short = 0
        self.db.save_info(self.book, name, short_name, txt_bitaka, txt_info, is_short)
        asm_customs.info(self.parent, 'تم حفظ المعلومات الجديدة')
    
    def __init__(self, parent, id_book):
        self.parent = parent
        self.db = listDB()
        self.book = self.db.file_book(id_book)
        Gtk.Dialog.__init__(self, parent=self.parent)
        self.set_icon_name("asmaa")
        self.connect('destroy', self.quit_dlg)
        area = self.get_content_area()
        area.set_spacing(5)
        self.set_border_width(5)
        
        hb_bar = Gtk.HeaderBar()
        hb_bar.set_show_close_button(True)
        self.set_titlebar(hb_bar)
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        hb_bar.set_custom_title(stack_switcher)

        self.set_default_size(600, 450)
        box = Gtk.Box(spacing=6,orientation=Gtk.Orientation.VERTICAL)

        box1 = Gtk.Box(spacing=6,orientation=Gtk.Orientation.VERTICAL)
        box2 = Gtk.Box(spacing=6,orientation=Gtk.Orientation.VERTICAL)
        
        hbox = Gtk.HBox(False, 3)
        self.n_n = Gtk.Label('اسم الكتاب')
        hbox.pack_start(self.n_n, False, False, 0) 
        self.ent_name = Gtk.Entry()
        self.ent_name.set_text(self.db.info_book(self.book)[0])
        hbox.pack_start(self.ent_name, True, True, 0)
        box1.pack_start(hbox, False, False, 0)
        
        hbox = Gtk.HBox(False, 3)
        self.n_ns = Gtk.Label('اسم مختصر')
        hbox.pack_start(self.n_ns, False, False, 0) 
        self.ent_name_sh = Gtk.Entry()
        self.ent_name_sh.set_text(self.db.info_book(self.book)[1])
        hbox.pack_start(self.ent_name_sh, True, True, 0)
        box1.pack_start(hbox, False, False, 0)
        
        box1.pack_start(Gtk.HSeparator(), False, False, 0)
        
        self.view_bitaka = Gtk.TextView()
        self.view_bitaka.set_wrap_mode(Gtk.WrapMode.WORD)
        self.view_bitaka.set_right_margin(5)
        self.view_bitaka.set_left_margin(5)
        self.view_bitaka_bfr = self.view_bitaka.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_bitaka)
        self.bitaka_book = self.db.info_book(self.book)[3]
        self.view_bitaka_bfr.set_text(self.bitaka_book)
        hbox = Gtk.HBox(False, 3)
        hbox.pack_start(Gtk.Label('بطاقة الكتاب'), False, False, 0)
        sample_btn = Gtk.ToggleButton("عينة")
        def sample_cb(w):
            if sample_btn.get_active():
                self.bitaka_book = self.view_bitaka_bfr.get_text(self.view_bitaka_bfr.get_start_iter(),
                            self.view_bitaka_bfr.get_end_iter(), False)
                self.view_bitaka_bfr.set_text('اسم الكتاب :\nالمؤلف :\nالناشر :\nالطبعة :\n\
التحقيق :\nعدد الأجزاء :\nمصدر الكتاب :\nترقيم الكتاب :')
            else:
                self.view_bitaka_bfr.set_text(self.bitaka_book)
        sample_btn.connect('toggled', sample_cb)
        hbox.pack_end(sample_btn, False, False, 0)
        box1.pack_start(hbox, False, False, 0)
        box1.pack_start(scroll, True, True, 0)
        
        self.view_info = Gtk.TextView()
        self.view_info.set_wrap_mode(Gtk.WrapMode.WORD)
        self.view_info.set_right_margin(5)
        self.view_info.set_left_margin(5)
        self.view_info_bfr = self.view_info.get_buffer()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_info)
        self.info_book = self.db.info_book(self.book)[4]
        self.view_info_bfr.set_text(self.info_book)
        hbox = Gtk.HBox(False, 3)
        hbox.pack_start(Gtk.Label('نبذة عن الكتاب'), False, False, 0)
        sample_btn1 = Gtk.ToggleButton("عينة")
        def sample_cb1(w):
            if sample_btn1.get_active():
                self.info_book = self.view_info_bfr.get_text(self.view_info_bfr.get_start_iter(),
                            self.view_info_bfr.get_end_iter(), False)
                self.view_info_bfr.set_text('موضوع الكتاب\nسبب التأليف\nمكانة الكتاب العلمية\nكلام العلماء في تقريضه')
            else:
                self.view_info_bfr.set_text(self.info_book)
        sample_btn1.connect('toggled', sample_cb1)
        hbox.pack_end(sample_btn1, False, False, 0)
        box1.pack_start(hbox, False, False, 0)
        box1.pack_start(scroll, True, True, 0)
        stack.add_titled(box1, 'n1', "بطاقة ونبذة")
        
        hbox = Gtk.HBox(False, 3)
        self.has_shorts = Gtk.CheckButton('هل به اختصارات قياسية')
        self.has_shorts.set_tooltip_text("'A'='صلى الله عليه وسلم', 'B'='رضي الله عن', 'C'='رحمه الله',\n'D'='عز وجل', 'E'='عليه الصلاة و السلام', 'Y'=':'")
        hbox.pack_start(self.has_shorts, False, False, 0) 
        if self.db.info_book(self.book)[7] == 1: self.has_shorts.set_active(True)
        box2.pack_start(hbox, False, False, 0)
        stack.add_titled(box2, 'n1', "معلومات أخرى")

        save_btn = Gtk.Button("حفظ")
        save_btn.connect('clicked', self.save_cb)
        hb_bar.pack_start(save_btn)
        
        box.pack_start(stack, True, True, 0)
        
        area.pack_start(box, True, True, 0)
        self.show_all()