# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

from os.path import join
from gi.repository import Gtk, Pango
import Asmaa.asm_path as asm_path


# class عنوان الصفحة-------------------------------------------------------------------    
    
class TabLabel(Gtk.Box):
    close_img=None
    
    def __init__(self, child, nm):
        self.nm = nm
        self.child=child
        if not self.close_img:
            self.close_img=Gtk.Image()
            self.close_img.set_from_file(join(asm_path.ICON_DIR, 'tab.png'))
        Gtk.Box.__init__(self,orientation=Gtk.Orientation.HORIZONTAL)
        self.close=Gtk.Button()
        self.close.set_tooltip_text('اغلق هذه الصفحة')
        self.close.add(self.close_img)
        self.close.set_focus_on_click(False)
        self.close.connect('clicked',self.close_tab)
        self.close.set_relief(Gtk.ReliefStyle(2))
        self.lab = Gtk.Label(self.nm)
        self.lab.set_width_chars(15)
        self.lab.set_ellipsize(Pango.EllipsizeMode.END)
        self.pack_start(self.lab, True, True,0)
        self.pack_start(self.close, False, False,0)
        self.set_tooltip_text(self.nm)
        self.show_all()

    def close_tab(self, *a):
        n = self.get_parent()
        i = n.page_num(self.child)
        if i < 0: return
        w = n.get_nth_page(i)
        try: w.db_list.set_last(w.all_in_page[1], w.id_book)
        except: pass
        n.remove_page(i)
        try: w.db.close_db()
        except: pass
        w.destroy()