# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from os.path import join, exists, isdir
import os
from gi.repository import Gtk
import asm_path
import asm_customs
from asm_edit_html import EditHTML

new_w = '''<head>
<title>new</title>
</head>
<body dir="rtl">
<div style="text-align: right;">ــــــــــــــــــــــــــــــــــــــــــــــــــــــ</div>
</body>
'''

# class نافذة أوراق البحث----------------------------------------------------------       
        
class Warakat(Gtk.HPaned):
    
    def remove_one(self, *a):
        model, i = self.tree_waraka.get_selection().get_selected()
        if i:
            msg = asm_customs.sure(self.parent, "هل تريد مسح الورقة المحددة")
            if msg == Gtk.ResponseType.YES:
                waraka = model.get_value(i,0)
                os.remove(join(asm_path.LIBRARY_DIR, u'waraka-search', waraka))
                model.remove(i)
                self.edit_html.set_sensitive(False)
                
    def remove_all(self, *a):
        msg = asm_customs.sure(self.parent, "هل تريد مسح جميع أوراق البحث")
        if msg == Gtk.ResponseType.YES:
            list_n = os.listdir(join(asm_path.LIBRARY_DIR, u'waraka-search'))
            for v in list_n:
                os.remove(join(asm_path.LIBRARY_DIR, u'waraka-search', v))
            self.store_waraka.clear()
            self.edit_html.set_sensitive(False)
            self.edit_html.clear_page()
    
    def show_waraka(self, *a):
        model, i = self.sel_waraka.get_selected()
        if i:
            waraka = model.get_value(i,0)
            myfile = join(asm_path.LIBRARY_DIR, u'waraka-search', waraka)
            self.edit_html.open_html(myfile)
            self.myfile = myfile
            self.edit_html.set_sensitive(True)
    
    def load_warakat(self, *a):
        self.store_waraka.clear()
        list_n = os.listdir(join(asm_path.LIBRARY_DIR, u'waraka-search'))
        for v in list_n:
            if isdir(join(asm_path.LIBRARY_DIR, u'waraka-search', v)): continue
            self.store_waraka.append([v])
    
    def search_on_active(self, text):
        self.edit_html.search_on_active(text)
    
    def search_on_page(self, text):
        self.edit_html.search_on_page(text)
    
#    def near_page(self, v):
#        self.iv.near_waraka(v) 
    
    def new_waraka(self, *a):
        if asm_path.can_modify(self.parent):
            new_waraka = self.ent_new.get_text()
            if new_waraka == u'': return
            myfile = join(asm_path.LIBRARY_DIR, u'waraka-search', new_waraka)
            if not exists(myfile):
                try:
                    f = open(myfile,'w+')
                    f.write(new_w)
                    f.close()
                except: raise
            else:
                asm_customs.erro(self.parent, "يوجد ورقة بنفس الاسم يرجى تغيير الاسم.")
                return
            self.store_waraka.append([new_waraka])
            self.ent_new.set_text('')
    
    def __init__(self, parent):
        self.parent = parent
        self.myfile = None
        self.edit_html = EditHTML()
        self.edit_html.set_sensitive(False)
        Gtk.HPaned.__init__(self)
        self.set_border_width(5)
        self.set_position(150)
        vbox = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        
        hbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        self.ent_new = Gtk.Entry()
        self.ent_new.set_placeholder_text('ورقة بحث جديدة')
        hbox.pack_end(self.ent_new, False, False, 0)
        new_btn = Gtk.ToolButton(stock_id=Gtk.STOCK_NEW)
        new_btn.connect('clicked', self.new_waraka)
        new_btn.set_tooltip_text('أضف ورقة بحث جديدة')
        hbox.pack_end(new_btn, False, False, 0)
        vbox.pack_start(hbox, False, False, 0)
        
        self.tree_waraka = Gtk.TreeView()
        self.tree_waraka.set_name('Tree')
        self.tree_waraka.set_size_request(150, -1)
        self.sel_waraka = self.tree_waraka.get_selection()
        cell = Gtk.CellRendererText()
        kal = Gtk.TreeViewColumn('أوراق البحث', cell, text=0)
        self.tree_waraka.append_column(kal)
        self.store_waraka = Gtk.ListStore(str)
        self.load_warakat()
        self.tree_waraka.set_model(self.store_waraka)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_waraka)
        self.tree_waraka.connect("cursor-changed", self.show_waraka)
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scroll, True, True, 0)
        
        remove = asm_customs.ButtonClass("حذف")
        remove.connect('clicked', self.remove_one)
        hbox = Gtk.Box(spacing=5,orientation=Gtk.Orientation.HORIZONTAL)
        hbox.pack_start(remove, True, True, 0)
        remove_all = asm_customs.ButtonClass("مسح")
        remove_all.connect('clicked', self.remove_all)
        hbox.pack_start(remove_all, True, True, 0)
        vbox.pack_start(hbox, False, False, 0)

        self.pack1(vbox, False, False)
        self.pack2(self.edit_html, True, False)
        self.show_all()
