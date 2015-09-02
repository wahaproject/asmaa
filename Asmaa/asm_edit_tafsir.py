# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import Gtk, Pango, GObject
import Asmaa.asm_config as asm_config
import Asmaa.asm_customs as asm_customs
from Asmaa.asm_contacts import bookDB, listDB, Othman

class EditTafsir(Gtk.Dialog):
    
    def quit_dlg(self, *a):
        self.destroy()
        self.db.close_db()
        del self.db
    
    def save_cb(self, *a):
        id_page = self.id_pg.get_value()
        sura = self.suras.get_active()+1
        aya = self.ayas.get_value()
        na = self.n_ayas.get_value()
        if sura == 0 or aya == 0 or na == 0: return
        self.db.edit_tafsir(id_page, sura, aya, na)
        self.change_id_pg()
        
    def no_save_cb(self, *a):
        id_page = self.id_pg.get_value()
        #self.suras.set_active(-1)
        #self.ayas.set_value(0)
        #self.n_ayas.set_value(0)
        self.db.edit_tafsir(id_page, 0, 0, 0)
        self.change_id_pg()
    
    def is_tafsir(self, all_in_page):
        try: sora, aya, na = all_in_page[6], all_in_page[7], all_in_page[8]
        except: sora = 0
        if sora > 0 and sora < 115:
            try: na = int(na)
            except: na = 1
            nasse_quran = ' '.join(self.othman.get_ayat(sora,aya,aya+na))
            self.view_nasse_bfr.insert(self.view_nasse_bfr.get_start_iter(), u" \n")
            self.view_nasse_bfr.insert_with_tags(self.view_nasse_bfr.get_start_iter(), 
                                                 nasse_quran, self.view_quran_tag)
    
    def change_id_pg(self, *a):
        page_id = self.id_pg.get_value()
        all_in_page = self.db.get_text_body(page_id)
        self.lab_id_pg.set_text(u'جزء {} ، صفحة {}'.format(all_in_page[3], all_in_page[4]))
        try:
            if all_in_page[6] != 0:
                self.suras.set_active(int(all_in_page[6])-1)
                self.ayas.set_value(int(all_in_page[7]))
                self.n_ayas.set_value(int(all_in_page[8]))
        except:
            pass
        self.view_nasse_bfr.set_text(all_in_page[2])
        self.is_tafsir(all_in_page)
        self.scroll_nasse.get_vadjustment().set_value(0.0)
    
    def select_sura(self, w):
        if self.suras.get_active() == -1: return
        ayat = asm_customs.value_active(w, 2)
        adj = self.ayas.get_adjustment()
        adj.set_upper(ayat)
        adj.set_value(1)
        adj = self.n_ayas.get_adjustment()
        adj.set_upper(ayat)
        adj.set_value(1)
    
    def __init__(self, parent, id_book):
        self.parent = parent
        self.listdb = listDB()
        book = self.listdb.file_book(id_book)
        self.db = bookDB(book, id_book)
        self.othman = Othman()
        Gtk.Dialog.__init__(self, parent=self.parent)
        self.set_icon_name("asmaa")
        self.resize(750, 450)
        self.set_modal(True)
        self.set_title(u'تعديل تفسير : {}'.format(self.db.book_name,))
        self.connect('destroy', self.quit_dlg)
        box = self.vbox
        box.set_border_width(5)
        
        # a عارض النص-----------------------------------
        self.view_nasse = asm_customs.ViewClass()
        self.view_nasse_bfr = self.view_nasse.get_buffer()
        self.view_quran_tag = self.view_nasse_bfr.create_tag("quran")
        self.view_quran_tag.set_property('foreground', self.parent.theme.color_qrn)
        self.view_quran_tag.set_property("paragraph-background", self.parent.theme.color_bg_qrn)
        self.view_quran_tag.set_property('font', self.parent.theme.font_qrn)
        self.scroll_nasse = Gtk.ScrolledWindow()
        self.scroll_nasse.set_shadow_type(Gtk.ShadowType.IN)
        self.scroll_nasse.add(self.view_nasse)
        box.pack_start(self.scroll_nasse, True, True, 0)
        box.pack_start(Gtk.HSeparator(), False, False, 3)
        
        hb = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        self.lab_id_pg = Gtk.Label('جزء 1 ، صفحة 1')
        hb.pack_start(self.lab_id_pg, False, False, 3)
        adj = Gtk.Adjustment(1, 1, len(self.db.list_pages), 1, 5.0, 0.0)
        self.id_pg = Gtk.SpinButton()
        self.id_pg.connect('changed', self.change_id_pg)
        self.id_pg.set_adjustment(adj)
        lab = Gtk.Label('معرف الصفحة')
        self.id_pg.set_wrap(True)
        self.id_pg.set_size_request(100, -1)
        hb.pack_end(self.id_pg, False, False, 0)
        hb.pack_end(lab, False, False, 0)
        box.pack_start(hb, False, False, 3)
        
        box.pack_start(Gtk.HSeparator(), False, False, 3)
        
        hb = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        sura_list = self.othman.get_suras_names()
        hb0, self.suras = asm_customs.combo(sura_list, u'السورة')
        hb.pack_start(hb0, False, False, 3)
        self.suras.set_active(-1)
        
        adj = Gtk.Adjustment(0, 0, 0, 1, 5.0, 0.0)
        self.n_ayas = Gtk.SpinButton()
        self.n_ayas.set_adjustment(adj)
        lab = Gtk.Label('عدد الآيات')
        self.n_ayas.set_wrap(True)
        self.n_ayas.set_size_request(100, -1)
        hb.pack_end(self.n_ayas, False, False, 0)
        hb.pack_end(lab, False, False, 0)
        
        adj = Gtk.Adjustment(0, 0, 0, 1, 5.0, 0.0)
        self.ayas = Gtk.SpinButton()
        self.ayas.set_adjustment(adj)
        lab = Gtk.Label('أول آية')
        self.ayas.set_wrap(True)
        self.ayas.set_size_request(100, -1)
        hb.pack_end(self.ayas, False, False, 0)
        hb.pack_end(lab, False, False, 0)
        box.pack_start(hb, False, False, 3)
        
        hbox = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
        save_btn = asm_customs.ButtonClass("غيّر")
        save_btn.set_tooltip_text('ثبت السورة والآيات للصفحة الحالية')
        save_btn.connect('clicked', self.save_cb)
        hbox.pack_start(save_btn, False, False, 0)
        no_save_btn = asm_customs.ButtonClass("أخل")
        no_save_btn.set_tooltip_text('ألغ ربط الصفحة الحالية بالآيات')
        no_save_btn.connect('clicked', self.no_save_cb)
        hbox.pack_start(no_save_btn, False, False, 0)
        clo = asm_customs.ButtonClass("إغلاق")
        clo.connect('clicked', self.quit_dlg)
        hbox.pack_end(clo, False, False, 0)
        box.pack_end(hbox, False, False, 0)
        box.pack_end(Gtk.HSeparator(), False, False, 3)
        
        self.suras.connect('changed', self.select_sura)
        self.show_all()
        
class ListTafasir(Gtk.Dialog):
    
    def __init__(self, parent):
        self.parent = parent
        self.db = listDB()
        self.build()

    def load_tafasir(self, *a):
        list_tafsir = eval(asm_config.getv('list_tafsir'))
        all_tafsir = self.parent.db.all_tafsir()
        if list_tafsir[2] == 0:
            for a in all_tafsir:
                self.store_tafsir_added.append(a)
                list_tafsir[1].append(a[0])
        else:
            for a in list_tafsir[1]:
                self.store_tafsir_added.append(self.parent.db.tit_book(a))
            for t in all_tafsir:
                if t[0] not in list_tafsir[1]:
                    self.store_tafsir_no_added.append(t)
        self.col_btn.set_active(list_tafsir[0])
        list_tafsir[2] = 1
        list_tafsir = repr(list_tafsir)
        asm_config.setv('list_tafsir', list_tafsir)

    def save_list(self, *a):
        list_tafsir = eval(asm_config.getv('list_tafsir'))
        list_tafsir[2] = 1
        list_tafsir[1] = []
        list_tafsir[0] = self.col_btn.get_active()
        for a in self.store_tafsir_added:
            list_tafsir[1].append(a[0])
        list_tafsir = repr(list_tafsir)
        asm_config.setv('list_tafsir', list_tafsir)
        self.parent.tafsirpage.refresh_list()
        self.destroy()
    
    def to_add_cb(self, *a):
        model, i = self.sel_tafsir_no_added.get_selected()
        if i:
            id_tafsir = model.get_value(i, 0)
            model.remove(i)
            self.store_tafsir_added.append(self.parent.db.tit_book(id_tafsir))
    
    def no_add_cb(self, *a):
        model, i = self.sel_tafsir_added.get_selected()
        if i:
            id_tafsir = model.get_value(i, 0)
            model.remove(i)
            self.store_tafsir_no_added.append(self.parent.db.tit_book(id_tafsir))
            
    def out_tafsir(self, *a):
        model, i = self.sel_tafsir_no_added.get_selected()
        if i:
            nm = model.get_value(i, 1)
            msg = asm_customs.sure(self.parent, 'هل تريد إزالة {} من القائمة؟'.format(nm, ))
            if msg == Gtk.ResponseType.YES:
                id_tafsir = model.get_value(i, 0)
                tafsir = self.db.file_book(id_tafsir)
                self.db.out_tafsir(tafsir, id_tafsir)
                model.remove(i)
        else:
            asm_customs.info(self.parent, "يجب تعليم التفسير في قائمة التفاسير المهملة\n ليتم إزالته منها")
    
    def build(self, *a):
        Gtk.Dialog.__init__(self, parent=self.parent)
        self.set_border_width(3)
        self.set_icon_name("asmaa")
        self.set_size_request(620, 450)
        self.connect('delete-event', lambda *a: self.destroy())
        vbox = self.vbox
        
        hb_bar = Gtk.HeaderBar()
        hb_bar.set_title("تعديل قائمة التفاسير")
        hb_bar.set_show_close_button(True)
        self.set_titlebar(hb_bar)
        
        hbox = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
        vbox1 = Gtk.Box(spacing=5,orientation=Gtk.Orientation.VERTICAL)
        self.store_tafsir_added = Gtk.ListStore(GObject.TYPE_INT, GObject.TYPE_STRING)
        self.tree_tafsir_added = Gtk.TreeView()
        self.tree_tafsir_added.set_model(self.store_tafsir_added)
        self.sel_tafsir_added = self.tree_tafsir_added.get_selection()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_tafsir_added)
        scroll.set_size_request(200, -1)
        celltext = Gtk.CellRendererText()
        celltext.set_property("ellipsize", Pango.EllipsizeMode.END)
        columntext = Gtk.TreeViewColumn("التفاسير المعتمدة", celltext, text = 1 )
        columntext.set_expand(True)
        self.tree_tafsir_added.append_column(columntext)
        vbox1.pack_start(scroll, True, True, 3)
        hbox.pack_start(vbox1, True, True, 0)
        
        vbox1 = Gtk.Box(spacing=5,orientation=Gtk.Orientation.VERTICAL)
        icon_theme = Gtk.IconTheme.get_default ()
        no_add = Gtk.Button()
        img = Gtk.Image()
        has = icon_theme.has_icon("gtk-go-forward-rtl")
        if  has: 
            img.set_from_icon_name('gtk-go-forward-rtl', Gtk.IconSize.BUTTON)
        else:
            img.set_from_stock(Gtk.STOCK_GO_BACK, Gtk.IconSize.BUTTON)
        no_add.set_image(img)
        no_add.set_tooltip_text('ألغ')
        no_add.connect('clicked', self.no_add_cb)
        vbox1.pack_start(no_add, True, False, 0)
        #--------------------------------------
        to_add = Gtk.Button()
        img = Gtk.Image()
        has = icon_theme.has_icon("gtk-go-back-rtl")
        if  has: 
            img.set_from_icon_name('gtk-go-back-rtl', Gtk.IconSize.BUTTON)
        else:
            img.set_from_stock(Gtk.STOCK_GO_FORWARD, Gtk.IconSize.BUTTON)
        to_add.set_image(img)
        to_add.set_tooltip_text('أضف')
        to_add.connect('clicked', self.to_add_cb)
        vbox1.pack_start(to_add, True, False, 0)
        hbox.pack_start(vbox1, False, False, 0)
        #--------------------------------------
        
        vbox1 = Gtk.Box(spacing=5,orientation=Gtk.Orientation.VERTICAL)
        self.store_tafsir_no_added = Gtk.ListStore(GObject.TYPE_INT, GObject.TYPE_STRING)
        self.tree_tafsir_no_added = Gtk.TreeView()
        self.tree_tafsir_no_added.set_model(self.store_tafsir_no_added)
        self.sel_tafsir_no_added = self.tree_tafsir_no_added.get_selection()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_tafsir_no_added)
        scroll.set_size_request(200, -1)
        celltext = Gtk.CellRendererText()
        celltext.set_property("ellipsize", Pango.EllipsizeMode.END)
        columntext = Gtk.TreeViewColumn("التفاسير المهملة", celltext, text = 1 )
        columntext.set_expand(True)
        self.tree_tafsir_no_added.append_column(columntext)
        vbox1.pack_start(scroll, True, True, 3)
        hbox.pack_start(vbox1, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)
        
        ls = ['1', '2', '3', '4', '5']
        self.col_btn = Gtk.ComboBoxText()
        for a in ls:
            self.col_btn.append_text(a)
        hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hb.pack_start(Gtk.Label('عدد الأعمدة في قائمة التفاسير'), False, False, 0)
        hb.pack_start(self.col_btn, False, False, 0)
        
        btn_re = Gtk.Button("إزالة من التفاسير")
        btn_re.connect("clicked", self.out_tafsir)
        hb.pack_end(btn_re, False, False, 0)
        vbox.pack_start(hb, False, False, 5)
        
        self.btn_save = asm_customs.ButtonClass('حفظ')
        self.btn_save.connect('clicked', self.save_list)
        hb_bar.pack_start(self.btn_save)
        self.load_tafasir()
        self.show_all()
