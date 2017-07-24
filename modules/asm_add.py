# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

import os, re
from shutil import copyfile
import asm_path
import asm_customs
from gi.repository import Gtk, GObject, Pango
from os.path import join, exists
from asm_contacts import listDB
from asm_import_bok import DB_from_MDB, load_list_books_from_shamela, DB_from_BOK, DB_from_doc
import sqlite3
import zipfile
import xml.etree.ElementTree

# class إضافة كتاب--------------------------------------------------------------

class AddBooks(Gtk.Dialog):
    
    def change_font(self, *a):
        ls = [self.tree_add, self.tree_add_doc]
        for a in ls:
            szfont, fmfont = asm_customs.split_font(self.parent.theme.font_lists_books)
            data = '''
            * {
            font-family: "'''+fmfont+'''";
            font-size: '''+szfont+'''px;
            }
            #Tree:selected {
            color: '''+asm_customs.rgb(self.parent.theme.color_selected)+''';
            background-color: '''+asm_customs.rgb(self.parent.theme.background_selected)+''';
            }
            #Tree:hover {
            color: '''+asm_customs.rgb(self.parent.theme.color_hover)+''';
            background-color: '''+asm_customs.rgb(self.parent.theme.background_hover)+''';
            }
            #Tree {
            color: '''+asm_customs.rgb(self.parent.theme.color_lists_books)+''';
            background-color: '''+asm_customs.rgb(self.parent.theme.background_lists_books)+''';
            }'''
            css_provider = Gtk.CssProvider()
            context = a.get_style_context()
            css_provider.load_from_data(data.encode('utf8'))
            context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    
    def add_bok(self, *args):
        self.progress.set_fraction(0.0)
        self.progress.set_text('')
        add_dlg = Gtk.FileChooserDialog("اختر ملفات الشاملة", self.parent, 
                                      buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT))
        cl_button = add_dlg.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        def cll(widget,*a):
            for i in add_dlg.get_filenames():
                self.store_add.append([i, os.path.basename(i)])
        cl_button.connect('clicked',cll)
        ff = Gtk.FileFilter()
        ff.set_name('جميع الملفات المدعومة')
        ff.add_pattern('*.[Bb][Oo][Kk]')
        ff.add_pattern('*.[Aa][Ss][Mm]')
        add_dlg.add_filter(ff)
        ff = Gtk.FileFilter()
        ff.set_name('ملفات الشاملة (bok)')
        ff.add_pattern('*.[Bb][Oo][Kk]')
        add_dlg.add_filter(ff)
        ff = Gtk.FileFilter()
        ff.set_name('ملفات أسماء (asm)')
        ff.add_pattern('*.[Aa][Ss][Mm]')
        add_dlg.add_filter(ff)
        add_dlg.set_select_multiple(True)
        add_dlg.run()
        add_dlg.destroy()
        
    def add_doc(self, *args):
        self.progress.set_fraction(0.0)
        self.progress.set_text('')
        add_dlg = Gtk.FileChooserDialog("اختر ملفات الشاملة", self.parent, 
                                      buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT))
        cl_button = add_dlg.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        def cll(widget,*a):
            for i in add_dlg.get_filenames():
                self.store_add_doc.append([i, os.path.basename(i)])
        cl_button.connect('clicked',cll)
        ff = Gtk.FileFilter()
        ff.set_name('الملفات المدعومة')
        ff.add_pattern('*.[Dd][Oo][Cc][Xx]')
        ff.add_pattern('*.[Hh][Tt][Mm][Ll]')
        ff.add_pattern('*.[Hh][Tt][Mm]')
        ff.add_pattern('*.[Tt][Xx][Tt]')
        ff.add_pattern('*.[Oo][Dd][Tt]')
        ff.add_pattern('*.[Rr][Tt][Ff]')
        ff.add_pattern('*.[Dd][Oo][Cc]')
        add_dlg.add_filter(ff)
        ff = Gtk.FileFilter()
        ff.set_name('جميع الملفات')
        ff.add_pattern('*')
        add_dlg.add_filter(ff)
        add_dlg.set_select_multiple(True)
        add_dlg.run()
        add_dlg.destroy()

    def start_convert(self, *a):
        if self.stack.get_visible_child_name() == 'n3':
            if len(self.store_books) == 0:
                asm_customs.erro(self, 'يجب إظهار قائمة الكتب أولا!')
                return
            self.btn_convert.set_sensitive(False)
            self.btn_stop.set_sensitive(True)
            self.stop_n = 0
            self.no_book = 1
            self.no_add = u''
            self.btn_convert.set_sensitive(False)
            self.store_books.foreach(self.import_shamela, True)
            if self.no_add != u'': asm_customs.erro(self, u'الكتب التي لم يتم إضافتها {}'.format(self.no_add,))
            self.lab_status.set_text(' لقد انتهت عملية التحويل ')
            self.btn_convert.set_sensitive(True)
        elif self.stack.get_visible_child_name() == 'n1':
            id_group = asm_customs.value_active(self.groups)
            if id_group == None:
                if len(self.db.all_parts()) > 0: asm_customs.info(self, "اختر القسم المراد ضم الكتب إليه")
                else: asm_customs.info(self, "اذهب إلى صفحة تنظيم المكتبة وأضف قسما لاستيراد الملفات إليه")
            else: 
                self.btn_convert.set_sensitive(False)
                self.btn_stop.set_sensitive(True)
                self.stop_n = 0
                self.import_book()
        elif self.stack.get_visible_child_name() == 'n2':
            id_group = asm_customs.value_active(self.groups_doc)
            if id_group == None:
                if len(self.db.all_parts()) > 0: asm_customs.info(self, "اختر القسم المراد ضم الكتب إليه")
                else: asm_customs.info(self, "اذهب إلى صفحة تنظيم المكتبة وأضف قسما لاستيراد الملفات إليه")
            else: 
                self.btn_convert.set_sensitive(False)
                self.btn_stop.set_sensitive(True)
                self.stop_n = 0
                self.import_docs()
    
    def get_text_from_file(self, myfile, name_file):
        # HTML----------------------------
        if re.search(re.compile(u'\.[Hh][Tt][Mm][Ll]?$'), name_file) != None:
            try:
                file = open(myfile)
                text = file.read()
                text = re.sub('\n', ' ', text)
                text = re.sub('<script.*?>.*?</script>', '', text)
                text = re.sub('<style.*?>.*?</style>', '', text)
                text = re.sub('<(.|\n)*?>', '\n', text)
                text = re.sub('\n\s+\n', '\n', text)
                text = re.sub('&.*?;', ' ', text)
                return text
            except: self.no_add += u'\n'+name_file
        # DOCX----------------------------
        elif re.search(re.compile(u'\.[Dd][Oo][Cc][Xx]$'), name_file) != None:
            try:
                myFile = zipfile.ZipFile(myfile)
                share = xml.etree.ElementTree.fromstring(myFile.read('word/document.xml'))
                text_nodes = []
                for elt in share.iter():
                    if elt.text != None:
                        text_nodes.append(elt.text.strip())
                text = u"\n".join(text_nodes)
                return re.sub(u'\n\s+\n', u'\n', text)
            except: self.no_add += u'\n'+name_file
        # ODT----------------------------
        elif re.search(re.compile(u'\.[Oo][Dd][Tt]$'), name_file) != None:
            try:
                myFile = zipfile.ZipFile(myfile)
                share = xml.etree.ElementTree.fromstring(myFile.read('content.xml'))
                text_nodes = []
                for elt in share.iter():
                    if elt.text != None:
                        text_nodes.append(elt.text.strip())
                text = u"\n".join(text_nodes)
                return re.sub(u'\n\s+\n', u'\n', text)
            except: self.no_add += u'\n'+name_file
        # TXT----------------------------
        elif re.search(re.compile(u'\.[Tt][Xx][Tt]$'), name_file) != None:
            try: 
                file = open(myfile)
                text =file.read()
                return re.sub(u'\n\s+\n', u'\n', text)
            except: self.no_add += '\n'+name_file
        # DOC & RTF----------------------
        elif re.search(re.compile(u'\.[Dd][Oo][Cc]$'), name_file) != None or \
        re.search(re.compile(u'\.[Rr][Tt][Ff]$'), name_file) != None:
            try: 
                (fi, fo, fe) = os.popen(u'catdoc -w "{}"'.format(myfile, ))
                fi.close()
                retval = fo.read()
                erroroutput = fe.read()
                fo.close()
                fe.close()
                if not erroroutput:
                    text = retval
                    return re.sub(u'\n\s+\n', u'\n', text)
                else:
                    raise OSError("Executing the command caused an error: %s" % erroroutput)
            except OSError: self.no_add += u'\n'+name_file+u'  -يرجى التحقق من تثبيت حزمة "catdoc"'
            except: self.no_add += u'\n'+name_file
        #OTHER----------------------------
        else:
            try: 
                text = open(myfile).read()
                return re.sub(u'\n\s+\n', u'\n', text)
            except: pass
    
    def split_text_to_pages(self, text):
        text = text.strip()
        pages = []
        if self.letters.get_active():
            n = self.n_letters.get_value()
            n_page = len(text)/int(n)
            list_term = text.split(' ')
            if n_page > 0: 
                n_term_page = len(list_term)/(n_page)
                baki = len(list_term)%(n_page)
                for a in range(n_page):
                    pages.append(u' '.join(list_term[a*n_term_page:(a+1)*n_term_page]))
                if baki > 0: pages.append(u' '.join(list_term[(n_page+1)*n_term_page:]))
            else:
                pages = [text]
        elif self.fasil.get_active():
            nass = self.separative.get_text()
            pages = text.split(nass)
        else:
            pages = [text]
        return pages           
    
    def make_book(self, nm_book, id_group, nm_group, list_page, list_title):
        DB_from_doc(nm_book, id_group, nm_group, list_page, list_title)
    
    def import_docs(self, *a):
        self.no_add = u''
        if len(self.store_add_doc) == 0: return
        id_group = asm_customs.value_active(self.groups_doc)
        nm_group = asm_customs.value_active(self.groups_doc, 1)
        self.progress.set_fraction(0.0)
        self.btn_clear_doc.set_sensitive(False)
        self.btn_convert.set_sensitive(False)
        self.btn_remove_doc.set_sensitive(False)
        self.btn_add_doc.set_sensitive(False)
        if not self.is_book_radio.get_active():
            new_book = self.name_book_entry.get_text()
            if new_book == u'': 
                asm_customs.info(self, "ضع اسما للكتاب المراد استيراده")
                return
            list_page = []
            list_title = []
            id_page = 1
        n_docs = len(self.store_add_doc)
        f = 0
        self.no_add = u''
        while len(self.store_add_doc) > 0:
            f += 1
            self.progress.set_fraction(float(f)/float(n_docs))
            while (Gtk.events_pending()): Gtk.main_iteration()
            if self.is_book_radio.get_active():
                new_book = re.sub(u'\....?.?$', u'', self.store_add_doc[0][1])
                text_book = self.get_text_from_file(self.store_add_doc[0][0], 
                                                    self.store_add_doc[0][1])
                if text_book != None and len(text_book) != 0:
                    pages = self.split_text_to_pages(text_book)
                    list_page = []
                    for a in range(len(pages)):
                        list_page.append([a+1, pages[a], 1, a+1])
                    list_title = [[1, new_book, 1, 0]]
                    self.make_book(new_book, id_group, nm_group, list_page, list_title)
            elif self.is_part_radio.get_active():
                text_book = self.get_text_from_file(self.store_add_doc[0][0], 
                                                    self.store_add_doc[0][1])
                if text_book != None and len(text_book) != 0:
                    pages = self.split_text_to_pages(text_book)
                    for a in range(len(pages)):
                        list_page.append([id_page, pages[a], f, a+1])
                        id_page += 1
                    list_title.append([id_page-len(pages), u'الجزء {}'.format(f), 1, 0])
            else:
                text_book = self.get_text_from_file(self.store_add_doc[0][0], 
                                                    self.store_add_doc[0][1])
                if text_book != None and len(text_book) != 0:
                    list_page.append([f, text_book, 1, f])
            i = self.store_add_doc.get_iter_first()
            self.store_add_doc.remove(i)
        if not self.is_book_radio.get_active():
            if list_title == []: list_title = [[1, new_book, 1, 0]]
            if self.no_add != u'': 
                msg = asm_customs.sure(self, u'''
                عدد الملفات التي لم يتمكن من إضافتها هو {}
                هل تريد الاستمرار في تكوين الكتاب ؟
                '''.format(len(self.no_add.split('\n')),))
                if msg == Gtk.ResponseType.YES:
                    self.make_book(new_book, id_group, nm_group, list_page, list_title)
        self.progress.set_text('انتهى !!')
        self.progress.set_fraction(1.0)
        self.btn_clear_doc.set_sensitive(True)
        self.btn_convert.set_sensitive(True)
        self.btn_remove_doc.set_sensitive(True)
        self.btn_add_doc.set_sensitive(True)
        if self.no_add != u'': asm_customs.erro(self, u'الملفات التي لم يتم إضافتها {}'.format(self.no_add,))
    
    def import_shamela(self, model, path, i, fixed):
        # model = 0=bool, 1='BkId', 2='Bk', 3='cat', 4='Betaka', 5='Inf', 6='Auth', 7='TafseerNam', 8='IslamShort', 9='Archive'
        bool0 = model.get_value(i,0)
        if self.stop_n == 1: return True
        if bool0 == fixed: 
            nm_book = model.get_value(i, 2)
            id_book = model.get_value(i, 1)
            archive = model.get_value(i, 9)#######
            i0 = model.iter_parent(i)
            if i0 != None: 
                info_list = model.get(i, 1, 2, 4, 5, 6, 7, 8)
                nm_group = model.get_value(i0, 2)
                id_group = model.get_value(i0, 1)
                dr = str(id_book)[-1]
                if archive == 0:
                    book  = join(self.path_shamila, 'Books', dr, str(id_book)+'.mdb')
                else:
                    book  = join(self.path_shamila, 'Books', 'Archive', str(archive)+'.mdb')
                try:
                    while (Gtk.events_pending()): Gtk.main_iteration()
                    self.no_book += 1
                    self.progress.set_fraction(float(self.no_book)/float(self.no_all_book))
                    DB_from_MDB(book, nm_group, info_list, self.comments, self.shorts, archive)
                    model.set_value(i, 0, False)
                    self.lab_status.set_text('({} \ {})  يجري تحويل كتاب {} '.format(self.no_book, self.no_all_book, nm_book))
                except OSError: asm_customs.erro(self, "حزمة mdbtools \nيرجى تثبيتها لأجل استيراد الكتب غير مثبتة"); raise
                except: self.no_add += '\n- '+info_list[1]; print ('not add {}'.format(str(info_list[0])+'.mdb',))
            return False
    
    def import_book(self, *a):
        if len(self.store_add) == 0: return
        id_group = asm_customs.value_active(self.groups)
        nm_group = asm_customs.value_active(self.groups, 1)
        self.progress.set_fraction(0.0)
        self.btn_clear.set_sensitive(False)
        self.btn_convert.set_sensitive(False)
        self.btn_remove.set_sensitive(False)
        self.btn_add.set_sensitive(False)
        n_books = len(self.store_add)
        f = 0
        self.no_add = u''
        while len(self.store_add) > 0:
            if self.stop_n == 1: break
            while (Gtk.events_pending()): Gtk.main_iteration()
            book = self.store_add[0][0]
            nm_file = self.store_add[0][1]
            if nm_file[-4:] == u'.asm':
                try: 
                    con = sqlite3.connect(book)
                    cur = con.cursor()
                    cur.execute("SELECT * FROM main")
                    info = cur.fetchone()
                    is_tafsir = info[8]
                    nm_book = info[0]
                    new_book = join(asm_path.BOOK_DIR, nm_group, nm_file) 
                    copyfile(book, new_book)
                    self.db.add_book(nm_book, id_group, is_tafsir)
                except: self.no_add += u'\n- '+nm_file[:-4]; print ('not add {}'.format(book,))
            else:
                nm_book = nm_file[:-4]
                #try:
                DB_from_BOK(book, nm_group, id_group)
                self.progress.set_fraction(float(f)/float(n_books))
#                except OSError: asm_customs.erro(self, "حزمة mdbtools \nيرجى تثبيتها لأجل استيراد الكتب غير مثبتة"); raise
#                except: self.no_add += u'\n- '+nm_book; print ('not add {}'.format(book,))
            i = self.store_add.get_iter_first()
            self.store_add.remove(i)
            f +=1
        self.progress.set_text('انتهى !!')
        self.progress.set_fraction(1.0)
        self.btn_clear.set_sensitive(True)
        self.btn_convert.set_sensitive(True)
        self.btn_remove.set_sensitive(True)
        self.btn_add.set_sensitive(True)
        if self.no_add != u'': asm_customs.erro(self, u'الكتب التي لم يتم إضافتها {}'.format(self.no_add,)) 
    
    def select_path(self, *a): 
        save_dlg = Gtk.FileChooserDialog(u'تحديد مجلد', self.parent,
                                    Gtk.FileChooserAction.SELECT_FOLDER,
                                    (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        res = save_dlg.run()
        if res == Gtk.ResponseType.OK:
            new_dir = save_dlg.get_filename()
            self.entry_shamila.set_text(new_dir)
        save_dlg.destroy()
    
    def show_books(self, *a):
        self.comments = {}
        self.shorts = {}
        self.path_shamila = self.entry_shamila.get_text()
        if self.path_shamila == u'': 
            asm_customs.erro(self, "لم تحدد موقع المكتبة الشاملة")
            return
        else:
            if not exists(join(self.path_shamila, u'Files')) or not exists(join(self.path_shamila, u'Books')):
                asm_customs.erro(self, "موقع الشاملة المحدد غير صحيح")
                return
            elif not exists(join(self.path_shamila, u'Files', u'main.mdb')) or \
            not exists(join(self.path_shamila, u'Files', u'special.mdb')):
                asm_customs.erro(self, "بعض الملفات الضرورية غير موجودة في هذا الدليل")
                return
        self.btn_convert.set_sensitive(False)
        load_list_books = load_list_books_from_shamela(join(self.path_shamila, u'Files', u'main.mdb'),
                                     join(self.path_shamila, u'Files', u'special.mdb'), 
                                     self.store_books, self.comments, self.shorts)
        self.no_all_book = load_list_books.no_all_book
        self.all_books.set_active(True)
        self.btn_convert.set_sensitive(True)
    
    def remove_iter(self, *a):
        if self.stack.get_visible_child_name() == 'n1':
            (model, i) = self.sel_add.get_selected()
        else:
            (model, i) = self.sel_add_doc.get_selected()
        if i :
            model.remove(i)
    
    def stop_operation(self, *a):
        self.stop_n = 1
        self.btn_convert.set_sensitive(True)
        self.btn_stop.set_sensitive(False)
    
    def select_inselect(self, model, path, i, bool1):
        bool0 = model.get_value(i,0)
        if bool0 != bool1: 
            model.set_value(i,0, bool1)
            return False
    
    def select_all(self, *a):
        if self.all_books.get_active():
            try: self.store_books.foreach(self.select_inselect, True)
            except: pass
        else:
            try: self.store_books.foreach(self.select_inselect, False)
            except: pass
            
    def fixed_toggled(self, cell, path, model):
        itr = model.get_iter((path),)
        fixed = model.get_value(itr, 0)
        if model.iter_has_child(itr):
            n_iters = self.store_books.iter_n_children(itr)
            d = 0
            while d in range(n_iters):
                iter1 = model.get_iter((int(path),d),)
                fixed1 = model.get_value(iter1, 0)
                fixed1 = not fixed
                model.set(iter1, 0, fixed1)
                d += 1
        fixed = not fixed
        model.set(itr, 0, fixed)

    def specified(self, *a):
        if self.is_book_radio.get_active():
            self.name_book_entry.set_sensitive(False)
            self.fasil.set_sensitive(True)
            self.letters.set_sensitive(True)
        elif self.is_part_radio.get_active():
            self.name_book_entry.set_sensitive(True)
            self.fasil.set_sensitive(True)
            self.letters.set_sensitive(True)
        else:
            self.name_book_entry.set_sensitive(True)
            self.fasil.set_sensitive(False)
            self.letters.set_sensitive(False)
            
    def __init__(self, parent):
        self.no_all_book = 1
        self.parent = parent
        self.db_bok = None
        self.stop_n = 0
        self.db = listDB()
        vbox = Gtk.Box(spacing=5,orientation=Gtk.Orientation.VERTICAL)
        box = Gtk.Box(spacing=5,orientation=Gtk.Orientation.VERTICAL)
        Gtk.Dialog.__init__(self, parent=self.parent)
        self.resize(550, 450)
        area = self.get_content_area()
        area.set_spacing(3)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        hb_bar = Gtk.HeaderBar()
        hb_bar.set_show_close_button(True)
        self.set_titlebar(hb_bar)
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(1000)
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)
        hb_bar.set_custom_title(stack_switcher)
         
        
        # a استيراد ملفات bok & asm----------------------------
        hb = Gtk.HBox(False, 3)
        self.btn_add = Gtk.Button("جديد")
        self.btn_add.connect('clicked', self.add_bok)
        hb.pack_start(self.btn_add, False, False, 0)
        hb.pack_start(Gtk.Label('«bok, asm»'), True, True, 0)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(hbox.get_style_context(), "linked")
        hb.pack_end(hbox, False, False, 0)
        self.btn_remove = Gtk.Button("حذف")
        self.btn_remove.connect('clicked', self.remove_iter)
        hbox.pack_start(self.btn_remove, False, False, 0)
        self.btn_clear = Gtk.Button("مسح")
        self.btn_clear.connect('clicked', lambda *a: self.store_add.clear())
        hbox.pack_start(self.btn_clear, False, False, 0)
        box.pack_start(hb, False, False, 0)
        self.store_add = Gtk.ListStore(str, str)
        self.tree_add = Gtk.TreeView()
        self.tree_add.set_name('Tree')
        self.sel_add = self.tree_add.get_selection()
        column = Gtk.TreeViewColumn('الكتب',Gtk.CellRendererText(),text = 1)
        self.tree_add.append_column(column)
        self.tree_add.set_model(self.store_add)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_add)
        box.pack_start(scroll, True, True, 0)
        ls = []
        for a in self.db.all_parts():
            ls.append([a[0], a[1]])
        hbox, self.groups = asm_customs.combo(ls, 'ضع هذه الكتب في قسم :')
        box.pack_start(hbox, False, False, 0)
        box.set_border_width(5)
        self.stack.add_titled(box, 'n1','ملفات كتب')
        
        # a استيراد الملفات النصية----------------------------
        box = Gtk.Box(spacing=5,orientation=Gtk.Orientation.VERTICAL)
        box.set_border_width(5)
        hb = Gtk.HBox(False, 3)
        self.btn_add_doc = Gtk.Button("جديد")
        self.btn_add_doc.connect('clicked', self.add_doc)
        hb.pack_start(self.btn_add_doc, False, False, 0)
        hb.pack_start(Gtk.Label('«odt, docx, doc, rtf, txt, html»'), True, True, 0)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(hbox.get_style_context(), "linked")
        hb.pack_end(hbox, False, False, 0)
        self.btn_remove_doc = Gtk.Button("حذف")
        self.btn_remove_doc.connect('clicked', self.remove_iter)
        hbox.pack_start(self.btn_remove_doc, False, False, 0)
        self.btn_clear_doc = Gtk.Button("مسح")
        self.btn_clear_doc.connect('clicked', lambda *a: self.store_add_doc.clear())
        hbox.pack_start(self.btn_clear_doc, False, False, 0)
        box.pack_start(hb, False, False, 0)
        self.store_add_doc = Gtk.ListStore(str, str)
        self.tree_add_doc = Gtk.TreeView()
        self.tree_add_doc.set_name('Tree')
        self.sel_add_doc = self.tree_add_doc.get_selection()
        column = Gtk.TreeViewColumn('الملفات',Gtk.CellRendererText(),text = 1)
        self.tree_add_doc.append_column(column)
        self.tree_add_doc.set_model(self.store_add_doc)
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_add_doc)
        box.pack_start(scroll, True, True, 0)
        
        hbox = Gtk.Box(spacing=10,orientation=Gtk.Orientation.HORIZONTAL)
        self.is_book_radio = Gtk.RadioButton.new_with_label_from_widget(None, 'كتاب')
        self.is_part_radio = Gtk.RadioButton.new_with_label_from_widget(self.is_book_radio, 'جزء')
        self.is_page_radio = Gtk.RadioButton.new_with_label_from_widget(self.is_part_radio, 'صفحة')
        self.is_book_radio.connect('toggled',self.specified,'0')
        self.is_part_radio.connect('toggled',self.specified,'1')
        self.is_page_radio.connect('toggled',self.specified,'2')
        hbox.pack_start(Gtk.Label('كل ملف يمثل : '), False, False, 0)
        hbox.pack_start(self.is_book_radio, False, False, 0)
        hbox.pack_start(self.is_part_radio, False, False, 0)
        hbox.pack_start(self.is_page_radio, False, False, 0)
        hbox.set_border_width(5)
        box.pack_start(hbox, False, False, 0)
        
        hb = Gtk.HBox(False, 7)
        hb.pack_start(Gtk.Label('اسم الكتاب : '), False, False, 0)
        self.name_book_entry = Gtk.Entry()
        self.name_book_entry.set_sensitive(False)
        hb.pack_start(self.name_book_entry, True, True, 0)
        box.pack_start(hb, False, False, 0)
        
        hb = Gtk.HBox(False, 7)
        self.letters = Gtk.CheckButton('عدد الأحرف في الصفحة')
        hb.pack_start(self.letters, False, False, 0)
        adj = Gtk.Adjustment(3000, 10, 100000, 1, 5.0, 0.0)
        self.n_letters = Gtk.SpinButton()
        self.n_letters.set_adjustment(adj)
        self.n_letters.set_wrap(True)
        self.n_letters.set_sensitive(False)
        hb.pack_start(self.n_letters, False, False, 0)
        box.pack_start(hb, False, False, 0)
        
        hb = Gtk.HBox(False, 7)
        self.fasil = Gtk.CheckButton('رمز فاصل بين الصفحات')
        hb.pack_start(self.fasil, False, False, 0)
        self.separative = Gtk.Entry()
        self.separative.set_placeholder_text("الفاصل يتم حذفه من الكتاب")
        self.separative.set_sensitive(False)
        hb.pack_start(self.separative, True, True, 0)
        box.pack_start(hb, False, False, 0)
        def letters_cb(widget, *a):
            if self.letters.get_active():
                self.n_letters.set_sensitive(True)
                self.fasil.set_active(False)
            else:
                self.n_letters.set_sensitive(False)
        self.letters.connect('toggled', letters_cb)
        def fasil_cb(widget, *a):
            if self.fasil.get_active():
                self.separative.set_sensitive(True)
                self.letters.set_active(False)
            else:
                self.separative.set_sensitive(False)
        self.fasil.connect('toggled', fasil_cb)
        
        box.pack_start(Gtk.HSeparator(), False, False, 0)
        
        hbox, self.groups_doc = asm_customs.combo(ls, 'ضع هذه الكتب في قسم :')
        box.pack_start(hbox, False, False, 0)
        self.stack.add_titled(box, 'n2','ملفات نصية')
        
        # a استيراد الشاملة----------------------------
        box = Gtk.Box(spacing=3,orientation=Gtk.Orientation.VERTICAL)
        box.set_border_width(5)
        
        hbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        self.entry_shamila = Gtk.Entry()
        b_shamila = Gtk.Button('...')
        b_shamila.connect('clicked', self.select_path)  
        hbox.pack_start(Gtk.Label('مجلد الشاملة'), False, False, 0)
        hbox.pack_start(self.entry_shamila, True, True, 0)
        hbox.pack_start(b_shamila, False, False, 0)
        box.pack_start(hbox, False, False, 0)
        
        hbox = Gtk.Box(spacing=6,orientation=Gtk.Orientation.HORIZONTAL)
        b_show = Gtk.Button('أظهر قائمة الكتب')
        b_show.connect('clicked', self.show_books)  
        hbox.pack_start(b_show, False, False, 0)
        box.pack_start(hbox, False, False, 0)
        
        #self.store_books = Gtk.TreeStore(GObject.TYPE_BOOLEAN, GObject.TYPE_STRING, GObject.TYPE_INT)
        self.store_books = Gtk.TreeStore(GObject.TYPE_BOOLEAN, GObject.TYPE_INT, GObject.TYPE_STRING, GObject.TYPE_INT, 
                                         GObject.TYPE_STRING, GObject.TYPE_STRING, GObject.TYPE_STRING, 
                                         GObject.TYPE_STRING, GObject.TYPE_INT, GObject.TYPE_INT)########
        self.tree_books = Gtk.TreeView()
        self.tree_books.set_model(self.store_books)
        self.sel_books = self.tree_books.get_selection()
        scroll = Gtk.ScrolledWindow()
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        scroll.add(self.tree_books)
        scroll.set_size_request(200, -1)
        celltext = Gtk.CellRendererText()
        celltext.set_property("ellipsize", Pango.EllipsizeMode.END)
        celltoggle = Gtk.CellRendererToggle()
        celltoggle.set_property('activatable', True)
        columntoggle = Gtk.TreeViewColumn("اختر", celltoggle)
        columntext = Gtk.TreeViewColumn("الكتب", celltext, text = 2 )
        columntext.set_expand(True)
        columntoggle.add_attribute( celltoggle, "active", 0)
        celltoggle.connect('toggled', self.fixed_toggled, self.store_books)
        self.tree_books.append_column(columntoggle)
        self.tree_books.append_column(columntext)
        box.pack_start(scroll, True, True, 0)
        
        hbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        self.all_books = Gtk.CheckButton('الكل')
        self.all_books.connect('toggled', self.select_all) 
        hbox.pack_start(self.all_books, False, False, 0)
        self.lab_status = Gtk.Label('')
        self.lab_status.set_ellipsize(Pango.EllipsizeMode.END)
        hbox.pack_end(self.lab_status, False, False, 0)
        box.pack_end(hbox, False, False, 0)
        
        self.stack.add_titled(box, 'n3','قرص الشاملة')
        
        hbox = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_border_width(5)
        self.btn_close = asm_customs.ButtonClass("إغلاق")
        self.btn_close.connect('clicked', lambda *a: self.destroy())
        hbox.pack_end(self.btn_close, False, False, 0)
        hb = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(hb.get_style_context(), "linked")
        hbox.pack_start(hb, False, False, 0)
        self.btn_convert = Gtk.Button("تحويل")
        self.btn_convert.connect('clicked', self.start_convert)
        hb.pack_start(self.btn_convert, False, False, 0)
        self.btn_stop = Gtk.Button("إيقاف")
        self.btn_stop.connect('clicked', self.stop_operation)
        self.btn_stop.set_sensitive(False)
        hb.pack_start(self.btn_stop, False, False, 0)
        vbox.pack_start(self.stack, True, True, 0)
        self.progress = Gtk.ProgressBar()
        vbox.pack_start(self.progress, False, False, 0)
        vbox.pack_start(hbox, False, False, 0)
        area.pack_start(vbox, True, True, 0)
        self.change_font()
        self.show_all()
        