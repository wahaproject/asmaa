# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import Gtk, Gdk
from Asmaa.asm_contacts import Othman, TarajimDB
import Asmaa.asm_stemming as asm_stemming
import Asmaa.asm_path as asm_path
import Asmaa.asm_customs as asm_customs
from os.path import join
import re, os

ACCEL_CTRL_KEY, ACCEL_CTRL_MOD = Gtk.accelerator_parse("<Ctrl>")
ACCEL_ALT_KEY, ACCEL_ALT_MOD = Gtk.accelerator_parse("<Alt>")

clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

def copy_to(widget, buff, waraka, parent):
    start_iter, end_iter = buff.get_selection_bounds()
    sel_text = buff.get_text(start_iter, end_iter, True)
    if parent.notebook.get_current_page() == 1:
        n = parent.viewerbook.get_current_page()
        ch = parent.viewerbook.get_nth_page(n)
        hamich = u'{} (ج{} - ص{})'.format(ch.nm_book, ch.all_in_page[3], ch.all_in_page[4])
    elif parent.notebook.get_current_page() == 4:
        part = parent.tafsirpage.part_now
        page = parent.tafsirpage.page_now
        nm_book = parent.tafsirpage.nm_book
        hamich = u'{} (ج{} - ص{})'.format(nm_book, part, page)
    myfile = open(join(asm_path.LIBRARY_DIR_rw, 'waraka-search', waraka), 'r')
    new_w = u'''<head>\n<title>new</title>\n</head>\n<body dir="rtl">\n\
    <div style="text-align: right;">ــــــــــــــــــــــــــــــــــــــــــــــــــــــ</div>\n\
    </body>
    '''
    text_file = myfile.read()
    if text_file == '': text_file = new_w
    if not u'ــــــــــــــــــ' in text_file: 
        text_file = re.sub('</body>', 
        '<div style="text-align: right;">ــــــــــــــــــــــــــــــــــــــــــــــــــــــ</div>\n</body>',
        text_file)
    liens_file = text_file.split('\n')
    for l in liens_file:
        if u'ــــــــــــــــــ' in l:
            index_khat = liens_file.index(l)
            n_hawamech = len(liens_file)-index_khat-2
    liens_file.insert(index_khat, 
    u'<div style="text-align: right;"><font face="KacstOne" size="6">{} </font><a href="#{}">({})</a></div>'.format(sel_text, n_hawamech, n_hawamech))
    liens_file.insert(-2,
    u'<div style="text-align: right;"><font face="KacstOne" size="3"><a name="{}">({})</a> {}</font></div>'.format(n_hawamech, n_hawamech, hamich))
    new_text = '\n'.join(liens_file)
    y = open(join(asm_path.LIBRARY_DIR_rw, 'waraka-search', waraka) , 'wb')
    y.write(new_text.encode('utf8'))
    y.close()


def copy_sel(widget, buff, parent):
    sel = buff.get_selection_bounds()
    sel_text = buff.get_text(sel[0], sel[1],True)
    clipboard.set_text(sel_text, -1)

def explain_term(widget, buff, parent):
    if buff.get_has_selection():
        sel = buff.get_selection_bounds()
        text = buff.get_text(sel[0], sel[1],True)
        text = asm_customs.first_term(text)
        if len(text) >= 3:
            all_root, all_term = asm_stemming.get_root(u''+text)
            if len(all_root) == 0:
                asm_customs.erro(parent, 'لا يوجد نتيجة'); return
            parent.winspage.dictpage.tree_dict.collapse_all()
            parent.winspage.dictpage.store_dict.clear()
            parent.winspage.dictpage.view_dict_bfr.set_text('')
            if len(all_root) != 0: 
                for text in all_root:
                    parent.winspage.dictpage.store_dict.append(None, [text])
            parent.winspage.dictpage.all_term = all_term
            i = parent.winspage.dictpage.store_dict.get_iter_first()
            p = parent.winspage.dictpage.store_dict.get_path(i)
            parent.winspage.dictpage.sel_dict.select_path(p)
            parent.notebook.set_current_page(3)
            parent.winspage.set_current_page(0)
            parent.winspage.dictpage.search_on_page(u"")
            
def tafsir_ayat(widget, buff, parent):
    if buff.get_has_selection():
        sel = buff.get_selection_bounds()
        text = buff.get_text(sel[0], sel[1],True)
        if len(text) >= 3:
            all_ayat = Othman().search('"'+text+'"')
            parent.tafsirpage.store_search.clear()
            if len(all_ayat) == 0:
                asm_customs.erro(parent, 'لا يوجد نتيجة'); return
            else: 
                for ayat in all_ayat:
                    i_sura = ayat[0]
                    i_ayat = ayat[1]
                    suras_names = Othman().get_suras_names()
                    sura = suras_names[i_sura-1]
                    parent.tafsirpage.store_search.append(None, [i_sura, i_ayat, sura[1]])
                    parent.tafsirpage.notebook.set_current_page(1)
            parent.tafsirpage.view_tafsir_bfr.set_text('')
            parent.tafsirpage.sel_search.select_path((0,))
            parent.notebook.set_current_page(4)
            parent.tafsirpage.ok_result()
            
def tarjama_rawi(widget, buff, parent):
    if buff.get_has_selection():
        sel = buff.get_selection_bounds()
        text = buff.get_text(sel[0], sel[1],True)
        if len(text) >= 3:
            all_rewat = TarajimDB().tardjma('"'+text+'"')
            parent.winspage.tarjamapage.store_tarjama.clear()
            if len(all_rewat) == 0:
                asm_customs.erro(parent, 'لا يوجد نتيجة'); return
            else: 
                for id_rawi in all_rewat:
                    name = id_rawi[1].split(u'،')[0]
                    parent.winspage.tarjamapage.store_tarjama.append(None, [id_rawi[0], name])
            parent.winspage.tarjamapage.tree_tarjama.collapse_all()
            parent.winspage.tarjamapage.view_tarjama_bfr.set_text('')
            parent.winspage.tarjamapage.tree_tarjama.expand_all()
            parent.winspage.tarjamapage.sel_tarjama.select_path((0,))
            parent.notebook.set_current_page(3)
            parent.winspage.set_current_page(1)
            
def tarjama_author(widget, buff, parent):
    if buff.get_has_selection():
        sel = buff.get_selection_bounds()
        text = buff.get_text(sel[0], sel[1],True)
        if len(text) >= 3:
            parent.winspage.authorpage.search_on_page(text)
            parent.winspage.authorpage.view_author_bfr.set_text('')
            parent.winspage.authorpage.tree_author.expand_all()
            parent.winspage.authorpage.sel_author.select_path((0,))
            parent.notebook.set_current_page(3)
            parent.winspage.set_current_page(2)

def populate_popup(view, menu, parent):
    for a in menu.get_children():
        a.destroy()
    buff = view.get_buffer()
    f1 = Gtk.MenuItem('شرح المفردة في القاموس')
    f1.add_accelerator("activate", parent.axl, Gdk.KEY_D, ACCEL_CTRL_MOD, 
                       Gtk.AccelFlags.VISIBLE)
    menu.append(f1)
    f1.set_sensitive(False)
    f1.show()
    f2 = Gtk.MenuItem('بحث عن آية في التفسير')
    menu.append(f2)
    f2.set_sensitive(False)
    f2.show()
    f3 = Gtk.MenuItem('ترجمة راو في التهذيب')
    menu.append(f3)
    f3.set_sensitive(False)
    f3.show()
    f8 = Gtk.MenuItem('ترجمة مؤلّف')
    menu.append(f8)
    f8.set_sensitive(False)
    f8.show()
    c1 = Gtk.SeparatorMenuItem()
    menu.append(c1)
    c1.show()
    f4 = Gtk.MenuItem('نسخ')
    menu.append(f4)
    f4.set_sensitive(False)
    f4.show()
    c2 = Gtk.SeparatorMenuItem()
    menu.append(c2)
    c2.show()
    f5 = Gtk.MenuItem('نسخ إلى ورقة البحث : ')
    menu.append(f5)
    f5.set_sensitive(False)
    f5.show()
    imenu = Gtk.Menu()
    f5.set_submenu(imenu)
    list_n = os.listdir(join(asm_path.LIBRARY_DIR_rw, 'waraka-search'))
    if len(list_n) > 0: 
        for v in list_n:
            fm = Gtk.MenuItem(v)
            fm.connect("activate", copy_to, buff, v, parent)
            imenu.append(fm)
            fm.show()
    else:
        fm = Gtk.MenuItem('لا يوجد ورقة بحث')
        fm.set_sensitive(False)
        imenu.append(fm)
        fm.show()
    c3 = Gtk.SeparatorMenuItem()
    menu.append(c3)
    c3.show()
    f6 = Gtk.MenuItem('الصفحة السابقة')
    f6.add_accelerator("activate", parent.axl, Gdk.KEY_Right, ACCEL_ALT_MOD, 
                       Gtk.AccelFlags.VISIBLE)
    menu.append(f6)
    f6.show()
    f7 = Gtk.MenuItem('الصفحة التالية')
    f7.add_accelerator("activate", parent.axl, Gdk.KEY_Left, ACCEL_ALT_MOD, 
                       Gtk.AccelFlags.VISIBLE)
    menu.append(f7)
    f7.show()
    if buff.get_has_selection():
        f1.set_sensitive(True)
        f2.set_sensitive(True)
        f3.set_sensitive(True)
        f4.set_sensitive(True)
        f5.set_sensitive(True)
        f8.set_sensitive(True)
    f1.connect("activate", explain_term, buff, parent)
    f2.connect("activate", tafsir_ayat, buff, parent)
    f3.connect("activate", tarjama_rawi, buff, parent)
    f4.connect("activate", copy_sel, buff, parent)
    f6.connect("activate", parent.previous_page, buff, parent)
    f7.connect("activate", parent.next_page, buff, parent)
    f8.connect("activate", tarjama_author, buff, parent)
