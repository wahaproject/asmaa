# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import Gtk, WebKit
from Asmaa.asm_contacts import Othman
import Asmaa.asm_path as asm_path
import Asmaa.asm_customs as asm_customs
from os.path import join
import pickle
import Asmaa.asm_config as asm_config
import re

title_sura = u'''
<table  id="mytitle" 
style="text-align: left; width: 95%; height: 57px; margin-left: auto; margin-right: auto;"
border="0">
<tbody>
<tr>
<td style="vertical-align: top; text-align: left;"><img
style="width: 63px; height: 49px;" alt="f" src="left1.png"></td>
<td style="vertical-align: middle; text-align: center; width: 15%;">الآيات<br>
</td>
<td style="vertical-align: top;"><img
style="width: 84px; height: 49px;" alt="ss" src="left2.png"><br>
</td>
<td
style="vertical-align: middle; text-align: center; width: 40%;">السورة<br>
</td>
<td style="vertical-align: top;"><img
style="width: 84px; height: 49px;" alt="aa" src="right2.png"><br>
</td>
<td style="vertical-align: middle; text-align: center; width: 15%;">الترتيب<br>
</td>
<td style="vertical-align: top; text-align: right;"><img
style="width: 63px; height: 49px;" alt="s" src="right1.png"><br>
</td>
</tr>
</tbody>
</table>
'''

ajzaa = {1: u'الأول', 2: u'الثاني', 3: u'الثالث', 4: u'الرابع', 5: u'الخامس', 6: u'السادس', 7: u'السابع'
         , 8: u'الثامن', 9: u'التاسع', 10: u'العاشر', 
         11: u'الحادي عشر', 12: u'الثاني عشر', 13: u'الثالث عشر', 14: u'الرابع عشر', 15: u'الخامس عشر', 16: u'السادس عشر'
         , 17: u'السابع عشر', 18: u'الثامن عشر', 19: u'التاسع عشر', 20: u'العشرون', 
         21: u'الحادي والعشرون', 22: u'الثاني والعشرون', 23: u'الثالث والعشرون', 24: u'الرابع والعشرون', 25: u'الخامس والعشرون'
         , 26: u'السادس والعشرون', 27: u'السابع والعشرون', 28: u'الثامن والعشرون', 29: u'التاسع والعشرون', 30: u'الثلاثون',  }

# class صفحة الكتب المفتوحة-----------------------------------------------------------------------

class ViewerMoshaf(Gtk.HPaned):
    
    def __init__(self, parent):
        self.parent = parent
        self.db = Othman()
        self.opened_new = []
        self.opened_old = []
        self.build()
    
    def show_bitaka(self, *a):
        return [u'',u'',u'',u'''
كلام رب العالمين على الحقيقة بألفاظه ومعانيه 
محفوظ في الصدور ، مقروء بالألسنة مكتوب في المصاحف
تكلم به الله تعالى فسمعه جبريل منه 
وتكلم به جبريل فسمعه النبي - صلى الله عليه وسلم - منه ، 
وتكلم به النبي - صلى الله عليه وسلم - فسمعته منه أمته وحفظته عنه ، 
فالكلام كلام الباري والصوت صوت القارئ . 
قال الله تعالى : فأجره حتى يسمع كلام الله  الآية 
        ''', u'''''']
    
    def first_page(self, *a):
        self.show_page(1)
    
    def previous_page(self, *a):
        if self.page_id == 1:
            return
        self.show_page(self.page_id-1)
    
    def next_page(self, *a):
        if self.page_id == 604:
            return
        self.show_page(self.page_id+1)
    
    def last_page(self, *a):
        self.show_page(604)
    
    def back_to_old(self, *a):
        if len(self.opened_old) == 1: return
        n = self.opened_old.pop()
        self.show_page(self.opened_old[-1])
        self.opened_new.append(n)
        
    def advance_to_new(self, *a):
        if len(self.opened_new) == 0: return
        n = self.opened_new.pop()
        self.show_page(n)
        if n != self.opened_old[-1]: self.opened_old.append(n)
    
    def ok_index(self, *a):
        model, i = self.sel_index.get_selected()
        if i:
            page= model.get_value(i,0)
            self.show_page(page)
            
    def show_page(self, page=1):
        new_list = []
        sura = u''
        ls_text = self.db.text_in_page(page)
        ls_text.reverse()
        for a in range(len(ls_text)):
            if a%2 == 0:
                txt = u'<div id = "nasse">'+' '.join(ls_text[a])+'</div>'
                new_list.append(txt)
            else:
                sura = ls_text[a][1]
                if page != 1 and page != 187: 
                    new_list.append(u'<div id = "basmala">بِــــسۡمِ ٱللهِ ٱلرَّحۡمَـٰنِ ٱلرَّحِيمِ</div>')
                tit = title_sura.replace(u'الترتيب', u'الترتيب{}'.format(ls_text[a][0]),).\
                replace(u'السورة', u'سورة '+ls_text[a][1]).replace(u'الآيات', u'الآيات{}'.format(ls_text[a][3]))
                new_list.append(tit)
        new_list.reverse()
        if [] in new_list: new_list.remove([])
        if sura == u'': sura = self.db.info_page(page)[0]
        new_text = ' '.join(new_list)
        html = open(join(asm_path.MOSHAF_DIR, 'page_quran.html'), 'r')
        html = html.read()
        html = html.replace('{nasse}', new_text)
        html = html.replace('{sura}', u'سورة '+sura)
        html = html.replace('{joze}', u'الجزء '+ajzaa[self.db.info_page(page)[1]])
        html = html.replace('{page}', str(page))
        if len(self.my_aya.keys()) != 0:
            if page in self.my_aya.keys():
                for a in self.my_aya[page]:
                    aya_txt = self.db.get_aya(a)
                    html = re.sub(aya_txt, u'<span style="background-color: rgb(255, 245, 177);">{}</span>'.format(aya_txt,), html)
        self.view_quran.load_html_string(html, u'file://{}/'.format(asm_path.MOSHAF_DIR,))
        self.page_id = page
        if len(self.opened_old) == 0: self.opened_old.append(page)
        elif page != self.opened_old[-1]: self.opened_old.append(page)
    
    def load_sura(self, *a):
        for a in self.list_sura:
            while (Gtk.events_pending()): Gtk.main_iteration()
            s = self.store_index.append(None, a[0])
            for b in a[1:]:
                self.store_index.append(s, b)
    
    def load_tahzib(self, *a):
        iters = [None]
        last_iter = None
        last_level = 0
        for i in self.list_ahzab:
            level = i[2]
            if level > last_level: iters.append(last_iter)
            elif level < last_level:
                for j in range(last_level-level): iters.pop()
            try :
                last_iter = self.store_index.append(iters[-1], [i[0], i[1]])
            except :
                pass
            last_level = level
    
    def load_page(self, *a):
        for page in range(1, 605):
            self.store_index.append(None, [page, u'الصفحة {}'.format(page,)])
    
    def load_index(self, btn):
        self.tree_index.handler_block(self.changed_index)
        v = btn.get_active()
        self.store_index.clear()
        if v == 0:
            self.load_sura()
        elif v == 1:
            self.load_tahzib()
        elif v == 2:
            self.load_page()
        self.my_aya = {}
        self.show_page(self.page_id)
        self.tree_index.handler_unblock(self.changed_index)
   
    def tafsir_ayat(self, *a):
        all_ayat = self.db.ayat_in_page(self.page_id)
        self.parent.tafsirpage.store_search.clear()
        if len(all_ayat[0]) == 0:
            asm_customs.erro(self.parent, 'لا يوجد نتيجة'); return
        else: 
            for ayat in all_ayat:
                i_sura = ayat[0]
                i_ayat = ayat[1]
                suras_names = Othman().get_suras_names()
                sura = suras_names[i_sura-1]
                self.parent.tafsirpage.store_search.append(None, [i_sura, i_ayat, sura[1]])
                self.parent.tafsirpage.notebook.set_current_page(1)
        self.parent.tafsirpage.view_tafsir_bfr.set_text('')
        self.parent.tafsirpage.sel_search.select_path((0,))
        self.parent.notebook.set_current_page(4)
        self.parent.tafsirpage.ok_result()
   
    def populate_page_popup_cb(self, view, menu):
        for a in menu.get_children():
            a.destroy()
        f1 = Gtk.MenuItem('تفسير الآيات')
        f1.connect('activate', self.tafsir_ayat) 
        menu.append(f1)
        c1 = Gtk.SeparatorMenuItem()
        menu.append(c1)
        c1.show()
        i = Gtk.MenuItem('تكبير النص')
        i.connect('activate', lambda m,v,*a,**k: v.zoom_in(), view)
        menu.append(i)
        i = Gtk.MenuItem('تصغير النص')
        i.connect('activate', lambda m,v,**k: v.zoom_out(), view)
        menu.append(i)
        i = Gtk.MenuItem('الحجم العادي')
        i.connect('activate', lambda m,v,*a,**k: v.get_zoom_level() == 1.0 or v.set_zoom_level(1.0), view)
        menu.append(i)
        menu.show_all()
        return False
    
    def search_on_page(self, text):
        return
     
    def search_on_active(self, text):
        if len(text) >= 3:
            all_ayat = Othman().search(text)
            self.store_index.clear()
            if len(all_ayat) == 0:
                asm_customs.erro(self.parent, 'لا يوجد نتيجة'); return
            else: 
                for ayat in all_ayat:
                    sura = ayat[0]
                    aya = ayat[1]
                    suras_names = Othman().get_suras_names()
                    suranm = suras_names[sura-1]
                    id_page = self.db.aya_page(aya, sura)
                    if id_page != self.id_page_last:
                        self.my_aya[id_page] = [ayat[5]]
                        self.id_page_last = id_page
                        self.store_index.append(None, [id_page, suranm[1]])
                    else:
                        self.my_aya[id_page].append(ayat[5])                
        
    def build(self, *a):
        self.id_page_last = 0
        try:
            self.list_sura = pickle.load(open(join(asm_path.MOSHAF_DIR, 'list_sura.pkl'), "rb"))
            self.list_ahzab =  pickle.load(open(join(asm_path.MOSHAF_DIR, 'list_ahzab.pkl'), "rb"))
        except:
            self.list_sura = []
            self.list_ahzab =  []
        self.my_aya = {}
        self.page_id = asm_config.getn('quran_pos')
        Gtk.HPaned.__init__(self)
        self.set_border_width(3)
        self.set_position(150)
        # a الفهرس-----------------------------------
        vbox = Gtk.VBox(False, 3)
        index_by = Gtk.ComboBoxText()
        index_by.append_text(u'السور')
        index_by.append_text(u'الأجزاء')
        index_by.append_text(u'الصفحات')
        index_by.set_active(0)
        vbox.pack_start(index_by, False, False, 0)
        self.tree_index = asm_customs.TreeIndex()
        self.tree_index.set_headers_visible(False)
        cell = Gtk.CellRendererText()
        cell.set_property("wrap-width", 150)
        kal = Gtk.TreeViewColumn('الفهرس', cell, text=1)
        self.tree_index.append_column(kal)
        self.store_index = Gtk.TreeStore(int, str)
        self.tree_index.set_model(self.store_index)
        self.sel_index = self.tree_index.get_selection()
        self.changed_index = self.tree_index.connect("cursor-changed", self.ok_index)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_index)
        scroll.get_hadjustment().set_value(0.0) 
        vbox.pack_start(scroll, True, True, 0)
        self.pack1(vbox, True, True)
        
        self.view_quran = WebKit.WebView()
        self.view_quran.connect("populate-popup", self.populate_page_popup_cb)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.view_quran)
        self.view_quran.set_full_content_zoom(True)
        self.pack2(scroll, True, True)
        index_by.connect('changed', self.load_index)
        self.load_index(index_by)