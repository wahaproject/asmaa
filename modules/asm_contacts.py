# -*- coding: utf-8 -*-

##############################################################################
#a#######  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

import sqlite3
from gi.repository import Gtk
import asm_path
import asm_config
import asm_araby
import asm_customs
from os.path import join, exists, getsize, basename
from os import unlink, listdir, mkdir


# class قاعدة بيانات قائمة الكتب----------------------------------

class listDB(object):
    
    def info_book(self, book):
        con = sqlite3.connect(book)
        cur = con.cursor()
        cur.execute("SELECT * FROM main")
        return cur.fetchone()
    
    def save_info(self, book, name, short_name, txt_bitaka, txt_info, is_short):
        con = sqlite3.connect(book)
        cur = con.cursor()
        cur.execute('UPDATE main SET bk=?, shortname=?, betaka=?, inf=?, islamshort=?', (name, short_name, txt_bitaka, txt_info, is_short))
        con.commit()
    
    def rename_book_in_main(self, book, name):
        con = sqlite3.connect(book)
        cur = con.cursor()
        cur.execute('UPDATE main SET bk=?', (name,))
        con.commit()
        
    def make_tafsir(self, book, id_book):
        con = sqlite3.connect(book)
        cur = con.cursor()
        cur.execute('UPDATE main SET is_tafseer=1')
        self.add_tafsir(id_book)
        con.commit()
        
    def out_tafsir(self, book, id_book):
        con = sqlite3.connect(book)
        cur = con.cursor()
        cur.execute('UPDATE main SET is_tafseer=0')
        con.commit()
        self.cur.execute('UPDATE books SET tafsir=0 WHERE id_book=?', (id_book, ))
        self.con.commit()
    
    def __init__(self, *a):
        self.con = sqlite3.connect(asm_path.LISTBOOK_FILE)
        self.con.create_function('fuzzy', 1, asm_araby.fuzzy_plus)
        self.cur = self.con.cursor()
     
    # a صيانة قاعدة البيانات-------------------------------------
    
    def repair(self, store, progress):
        store.clear()
        progress.set_text('جاري الفحص')
        #a الكتب الموجودة في قاعدة البيانات-------------------------
        self.cur.execute('SELECT id_book, tit FROM books')
        books = self.cur.fetchall()
        n_books = len(books)
        list1 = [] 
        a  = 0
        while a < (n_books):
            if a%500 == 499: 
                while (Gtk.events_pending()): Gtk.main_iteration()
            nm_book = books[a][1]
            id_book = books[a][0]
            nm_group = self.group_book(id_book)
            if nm_group == '': 
                self.remove_book(id_book)
                store.append([nm_book+u" :  اسم فقط لا ينتمي لقسم (تم حذفه)"])
                continue
            list1.append(nm_book)
            book = self.file_book(id_book)
            if not exists(book) or getsize(book) == 0:
                self.remove_book(id_book)
                try: unlink(book)
                except: pass
                store.append([nm_book+u" :  يوجد الاسم فقط (تم حذفه)"])
            j = (float(a)/float(n_books+1))/2.0
            progress.set_fraction(j)
            a += 1
        #a الأقسام الموجودة في قاعدة البيانات-------------------------
        groups = self.all_parts()
        for g in groups:
            if not exists(join(asm_path.BOOK_DIR, g[1])):
                mkdir(join(asm_path.BOOK_DIR, g[1]))
                store.append([g[1]+u" : قسم فارغ موجود في قاعدة البيانات (تم إضافته إلى الدليل)"])
        #a الكتب والأقسام الموجودة في دليل المكتبة--------------------
        path = asm_path.BOOK_DIR
        list_g = listdir(path)
        b = 0
        for a in list_g:
            self.cur.execute("SELECT * FROM groups WHERE tit=?", (a,))
            group = self.cur.fetchone()
            if group == None or len(group) == 0:
                self.add_part(a)
                store.append([a+u" : قسم موجود في الدليل فقط (تم إضافته إلى قاعدة البيانات)"])
            ls_b = listdir(join(path, a))
            for a1 in ls_b:
                if b%500 == 499: 
                    while (Gtk.events_pending()): Gtk.main_iteration()
                if a1[-4:] == '.asm' and getsize(join(path, a, a1)) > 0:
                    a2 = a1.replace('.asm', '')
                    self.cur.execute("SELECT * FROM books WHERE tit=?", (a2,))
                    book = self.cur.fetchone()
                    if book == [] or book == None :
                        id_group = self.group_id(a)
                        try:
                            is_tafsir = self.info_book(join(path, a, a1))[8]
                            self.add_book(a2, id_group, is_tafsir)
                            store.append([a1+u" : كتاب موجود في الدليل فقط تم إضافته إلى قسم "+a])
                        except:
                            unlink(join(path, a, a1))
                            store.append([a1+u" : كتاب تالف (تم حذفه)"])
                else:
                    try:
                        unlink(join(path, a, a1))
                        store.append([a1+u" : كتاب فارغ (تم حذفه)"])
                    except: pass
                b += 1
                j1 = ((float(b)/float(n_books))/2.0) + j
                progress.set_fraction(j1)
        #a الكتب والأقسام الموجودة في دليل المكتبة المقروءة--------------------        
        path = asm_path.BOOK_DIR
        if asm_path.HOME_DIR in asm_path.BOOK_DIR and asm_path.LIBRARY_DIR_r != u'':
            list_g = listdir(path)
            b = 0
            for a in list_g:
                self.cur.execute("SELECT * FROM groups WHERE tit=?", (a,))
                group = self.cur.fetchone()
                if group == None or len(group) == 0:
                    self.add_part(a)
                    store.append([a+u" : قسم موجود في الدليل فقط (تم إضافته إلى قاعدة البيانات)"])
                ls_b = listdir(join(path, a))
                for a1 in ls_b:
                    if b%500 == 499: 
                        while (Gtk.events_pending()): Gtk.main_iteration()
                    if a1[-4:] == '.asm' and getsize(join(path, a, a1)) > 0:
                        a2 = a1.replace('.asm', '')
                        self.cur.execute("SELECT * FROM books WHERE tit=?", (a2,))
                        book = self.cur.fetchone()
                        if book == [] or book == None :
                            id_group = self.group_id(a)
                            try:
                                is_tafsir = self.info_book(join(path, a, a1))[8]
                                self.add_book(a2, id_group, is_tafsir, -1)
                                store.append([a1+u" : كتاب موجود في الدليل فقط تم إضافته إلى قسم "+a])
                            except: pass   
                    b += 1
        if len(store) == 0:
                store.append([u"جميع البيانات سليمة"])
        store.append([u"انتهى."])
        progress.set_fraction(0.0)
      
    # a قاعدة بيانات جديدة---------------------------------------
    
    def new_db(self, path):
        con = sqlite3.connect(path)
        cur = con.cursor()
        cur.execute('CREATE TABLE groups (id_group integer primary key, tit varchar(255), sub INTEGER, cat INTEGER)') 
        cur.execute('CREATE TABLE books (id_book integer primary key, tit varchar(255), \
        parent INTEGER, fav  INTEGER DEFAULT 0, last  INTEGER DEFAULT 1, cat  INTEGER DEFAULT 0,\
        tafsir  INTEGER DEFAULT 0, indx INTEGER DEFAULT 0)')
      
    # a الأقسام الرئيسة---------------------------------------
    
    def all_parts(self, *a):
        self.cur.execute('SELECT id_group, tit FROM groups ORDER BY cat')
        parts = self.cur.fetchall()
        return parts
    
    # a التفاسير---------------------------------------
    
    def all_tafsir(self, *a):
        self.cur.execute('SELECT id_book, tit FROM books WHERE tafsir=1')
        tafsir = self.cur.fetchall()
        return tafsir
    
    def add_tafsir(self, id_book):
        self.cur.execute('UPDATE books SET tafsir=1 WHERE id_book=?', (id_book, ))
        check = self.con.commit()
        return check
    
    # a كتب قسم محدد---------------------------------------
    
    def books_part(self, id_part):
        self.cur.execute('SELECT id_book, tit FROM books WHERE parent=? ORDER BY tit', (id_part, ))
        books = self.cur.fetchall()
        return books
    
    # a اسم كتاب محدد---------------------------------------
    
    def tit_book(self, id_book):
        self.cur.execute('SELECT id_book, tit FROM books WHERE id_book=?', (id_book, ))
        book = self.cur.fetchone()
        return book
    
    # a مجموعة كتاب محدد---------------------------------
   
    def group_book(self, id_book):
        self.cur.execute('SELECT parent FROM books WHERE id_book=?', (id_book, ))
        parent = self.cur.fetchone()
        self.cur.execute('SELECT tit FROM groups WHERE id_group=?', (parent[0], ))
        part = self.cur.fetchone()
        if part == None: return ''
        return part[0]
    
    # a معرف مجموعة محددة---------------------------------
   
    def group_id(self, nm_group):
        self.cur.execute('SELECT id_group FROM groups WHERE tit=?', (nm_group, ))
        part = self.cur.fetchone()
        return part[0]
    
    # a إضافة كتاب إلى المفضلة------------------------------
    
    def to_favorite(self, id_book):
        self.cur.execute('UPDATE books SET fav=1 WHERE id_book=?', (id_book, ))
        check = self.con.commit()
        if len(self.cur.execute('SELECT id_book FROM books WHERE id_book=?', (id_book, )).fetchall()) == 0: return 'u'
        return check
    
    # a إخراج كتاب من المفضلة------------------------------
    
    def out_favorite(self, id_book):
        self.cur.execute('UPDATE books SET fav = 0 WHERE id_book=?', (id_book, ))
        check = self.con.commit()
        return check
   
    # a كتب المفضلة---------------------------------------
    
    def favorite_books(self):
        self.cur.execute('SELECT id_book, tit FROM books WHERE fav=1')
        books = self.cur.fetchall()
        return books
    
    # a عدد الكتب---------------------------------------
    
    def n_books(self):
        self.cur.execute('SELECT id_book FROM books')
        books = self.cur.fetchall()
        return len(books)
    
    # a كتاب فارغ-----------------------------------------
    
    def empty_book(self, db):
        nm_book = basename(db).replace('.asm', '')
        con = sqlite3.connect(db, isolation_level=None)
        cur = con.cursor() 
        for tb in asm_customs.schema.keys():
            cur.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(tb, asm_customs.schema[tb]))
        cur.execute('INSERT INTO main VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (nm_book, '', 0, '', '', 0, 0, 0, 0, 0, 0.1))
        cur.execute('INSERT INTO pages VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (1, '', 1, 1, 0, 0, 0, 0))
        cur.execute('INSERT INTO titles VALUES (?, ?, ?, ?)', (1, nm_book, 0, 0))
        con.commit()
    
    # a إضافة قسم--------------------------------------
    
    def add_part(self, nm_part):
        self.cur.execute('SELECT id_group, tit FROM groups WHERE tit=?', (nm_part,))
        is_group = self.cur.fetchall()
        if len(is_group) > 0: return is_group[0][0]
        self.cur.execute('SELECT id_group FROM groups ORDER BY id_group')
        groups = self.cur.fetchall()
        if len(groups) == 0: id_group = 1
        else: id_group = groups[-1][0]+1
        self.cur.execute('INSERT INTO groups VALUES (?, ?, ?, ?)', 
                         (id_group, nm_part, 0, len(groups)))
        check = self.con.commit()
        if check == None:
            return id_group
    
    # a إضافة كتاب--------------------------------------
    
    def add_book(self, nm_book, id_part, is_tafsir=0, cat=0):
        self.cur.execute('SELECT tit, parent FROM books WHERE tit=? AND parent=?', (nm_book, id_part))
        is_book = self.cur.fetchall()
        if len(is_book) > 0: return True
        self.cur.execute('SELECT id_book FROM books ORDER BY id_book')
        books = self.cur.fetchall()
        if len(books) == 0: id_book = 1
        else: id_book = books[-1][0]+1
        self.cur.execute('INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                         (id_book, nm_book, id_part, 0, 0, cat, is_tafsir, 0))
        check = self.con.commit()
        return check
    
    # a إعادة تسمية قسم------------------------------
    
    def rename_part(self, nm_new, nm_old):
        self.cur.execute('UPDATE groups SET tit=? WHERE tit=?', (nm_new, nm_old))
        check = self.con.commit()
        return check
    
    # a حذف قسم------------------------------------------
    
    def remove_group(self, id_group):
        self.cur.execute('DELETE FROM groups WHERE id_group=?', (id_group,))
        check1 = self.con.commit()
        if check1 == None:
            self.cur.execute('DELETE FROM books WHERE parent=?', (id_group,))
            check = self.con.commit()
        return check

    # a حذف الفهرس------------------------------------------
    
    def remove_index(self, *a):
        self.cur.execute('UPDATE books SET indx=0 WHERE indx=1')
        check = self.con.commit()
        return check
    
    # a حذف كتاب------------------------------------------
    
    def remove_book(self, id_book):
        self.cur.execute('DELETE FROM books WHERE id_book=?', (id_book,))
        check = self.con.commit()
        return check

    # a ترتيب الاقسام----------------------------------------
    
    def organiz_groups(self, ls):
        self.cur.execute('BEGIN;')
        for a in ls:
            self.cur.execute('UPDATE groups SET cat=? WHERE tit=?', (a[0], a[1]))
        check = self.con.commit()
        return check
    
    # a دمج قسمين----------------------------------------
    
    def merge_group(self, id_old, id_new):
        self.cur.execute('DELETE FROM groups WHERE id_group=?', (id_old,))
        check1 = self.con.commit()
        if check1 == None:
            self.cur.execute('UPDATE books SET parent=? WHERE parent=?', (id_new, id_old))
            check = self.con.commit()
        return check
    
    # a إعادة تسمية كتاب----------------------------------------
    
    def rename_book(self, nm_new, nm_old):
        self.cur.execute('UPDATE books SET tit=? WHERE tit=?', (nm_new, nm_old))
        check = self.con.commit()
        return check
    
    # a تغيير قسم كتاب----------------------------------------
    
    def change_group(self, id_book, id_group):
        self.cur.execute('UPDATE books SET parent=? WHERE id_book=?', (id_group, id_book))
        check = self.con.commit()
        return check
    
    # a هل الكتاب مفهرس؟------------------------------------
    def is_indexed(self, id_book):
        self.cur.execute('SELECT id_book FROM books WHERE indx=1 AND id_book=? LIMIT 1', (id_book, ))
        books = self.cur.fetchone()
        if books == None or len(books) == 0: return False
        else: return True
        
    # a تعيين كتاب مفهرس------------------------------------
    def add_indexed(self, id_book):
        self.cur.execute('UPDATE books SET indx=1 WHERE id_book=?', (id_book, ))
        check = self.con.commit()
        return check
        
    # a إلغاء فهرسة كتاب------------------------------------
    def null_indexed(self, id_book):
        self.cur.execute('UPDATE books SET indx=0 WHERE id_book=?', (id_book, ))
        check = self.con.commit()
        return check
    
    # a بحث في قائمة الكتب-----------------------------------
    
    def search_books(self, text):
        self.cur.execute('SELECT id_book, tit FROM books WHERE fuzzy(tit) LIKE ? LIMIT 100', ('%'+asm_araby.fuzzy(text)+'%', ))
        books = self.cur.fetchall()
        return books

    # a حفظ أخر صفحة في التصفح------------------------------
    
    def set_last(self, id_page, id_book):
        self.cur.execute('UPDATE books SET last=? WHERE id_book=?', (id_page, id_book))
        check = self.con.commit()
        return check
    
    # a استرجاع أخر صفحة في التصفح------------------------------
    
    def get_last(self, id_book):
        self.cur.execute('SELECT last FROM books WHERE id_book=?', (id_book, ))
        id_page = self.cur.fetchone()
        return id_page
    
    # a موقع الكتب-------------------------------------------
    
    def book_dir(self, id_book):
        self.cur.execute('SELECT cat FROM books WHERE id_book=?', (id_book, ))
        cat = self.cur.fetchone()
        if cat[0] == -1: return asm_path.BOOK_DIR
        else: return asm_path.BOOK_DIR
    
    # a استخراج كتاب لوضع الكتابة-----------------------------
    
    def mode_write(self, id_book):
        self.cur.execute('UPDATE books SET cat=0 WHERE id_book=?', (id_book, ))
        self.con.commit()
    
    # a إعادة ملف كتاب----------------------------------------
    
    def file_book(self, id_book):
        book_dir = self.book_dir(id_book)
        return join(book_dir, self.group_book(id_book),
                     self.tit_book(id_book)[1]+u'.asm')

# class قاعدة بيانات كتاب محدد----------------------------------

class bookDB(object):
    
    altered = [(u'EX', u''), (u'{', u'﴿'), (u'}', u'﴾'), (u'0', u'٠'), (u'1', u'١'), 
                (u'2', u'٢'), (u'3', u'٣'), (u'4', u'٤'), (u'5', u'٥‌'), (u'6', u'٦'), 
                (u'7', u'٧'), (u'8', u'٨'), (u'9', u'٩'), (u'+', u'')]
    
    altered0 = [(u'EX', u''), (u'{', u'﴿'), (u'}', u'﴾'), ( u'٠',u'0'), ( u'١',u'1'), 
                (u'٢', u'2'), (u'٣' ,u'3'), (u'٤' ,u'4'), (u'٥‌' ,u'5'), (u'٦' ,u'6'), 
                (u'٧' ,u'7'), (u'٨' ,u'8'), (u'٩' ,u'9'), (u'+', u'')]
    
    shorts0 = [(u'A', u'صلى الله عليه وسلم'), (u'B', u'رضي الله عن'), (u'C', u'رحمه الله'), 
             (u'D', u'عز وجل'), (u'E', u'عليه الصلاة و السلام'), (u'Y', u':')]
    
    def __init__(self, book, id_book):
        self.book = book
        self.id_book = id_book
        self.con = sqlite3.connect(self.book)
        self.con.create_function('fuzzy', 1, asm_araby.fuzzy_plus)
        self.con.create_function('expand_shorts', 1, self.expand_shorts)
        self.cur = self.con.cursor()
        
        self.is_tafseer = 0
        self.is_sharh = 0
        self.shorts = 0
        self.cur.execute("SELECT bk, is_tafseer, is_sharh, islamshort, version FROM main LIMIT 1")
        r = self.cur.fetchone()
        self.book_name = r[0]
        self.n_version = r[4]
        self.is_tafseer, self.is_sharh, self.shorts = r[1], r[2], r[3]
        self.shorts_init()
        self.cur.execute("SELECT rowid FROM pages ORDER BY part AND page")
        self.list_pages = self.cur.fetchall()
        self.len_index = len(self.cur.execute("SELECT rowid FROM pages").fetchall())
        
    def change_version(self, ver):
        self.cur.execute('UPDATE main SET version=?', (ver, ))
        self.con.commit()
    
    def shorts_init(self):
        self.shorts1 = []
        self.shorts2 = []
        if self.shorts & 1: self.shorts1 = self.shorts0
        else: self.shorts1 = []
        if self.shorts<2: self.shorts2 = []; return
        self.cur.execute('SELECT ramz, nass FROM shorts')
        ramz = self.cur.fetchall()
        for a in ramz:
            self.shorts2.append((a[0], a[1]))
            
    def expand_shorts(self, txt):
        if asm_config.getn('nmbrs') == 0: 
            for i, j in self.altered: txt = txt.replace(i, j)
        else: 
            for i, j in self.altered0: txt = txt.replace(i, j)
        for i, j in self.shorts1: txt = txt.replace(i, j)
        for i, j in self.shorts2: txt = txt.replace(i, j)
        return txt
    
    # a فهرس كتاب محدد---------------------------------------
    
    def index_book(self, *a):
        self.cur.execute("SELECT rowid, id, tit, lvl FROM titles ORDER BY id")
        toc_list = self.cur.fetchall()
        en = enumerate(toc_list)
        rv = reversed(list(en))
        h = {}
        for i, j in rv: h[j[1]] = j # i is used to keep the order only
        self.toc_ids = h.keys() 
#        self.toc_ids.sort()
        self.toc_uniq = h.values()
#        self.toc_uniq.sort()
        return toc_list
    
    # a عناوين صفحة ممعينة---------------------------------------
    
    def titles_page(self, page_id):
        self.cur.execute("SELECT tit FROM titles WHERE id=?", (page_id, ))
        t_list = self.cur.fetchall()
        t = []
        for i in t_list:
            t.append(i[0])
        return t
    
    # a نص صفحة معينة----------------------------------------
    
    def get_text_body(self, page_id):
        self.cur.execute("SELECT rowid, id, expand_shorts(nass) as text, part, page, \
        hno, sora, aya, na FROM pages WHERE id=? LIMIT 1" , (page_id, ))
        return self.cur.fetchone()

    # a التصفح--------------------------------------------

    def first_page(self):
        self.cur.execute("SELECT id FROM pages WHERE rowid=?", (1, ))
        return self.cur.fetchone()[0]
    
    def previous_page(self, current_id):
        if current_id == 1: return 1
        self.cur.execute("SELECT id FROM pages WHERE rowid=?", (current_id-1, ))
        return self.cur.fetchone()[0]
    
    def next_page(self, current_id):
        if current_id == len(self.list_pages): return len(self.list_pages)
        self.cur.execute("SELECT id FROM pages WHERE rowid=?", (current_id+1, ))
        return self.cur.fetchone()[0]
    
    def last_page(self):
        self.cur.execute("SELECT id FROM pages WHERE rowid=?", (len(self.list_pages), ))
        return self.cur.fetchone()[0]
    
    # a بطاقة الكتاب----------------------------------------------
    
    def info_book(self):
        self.cur.execute("SELECT * FROM main")
        return self.cur.fetchone()
    
    def go_to_page(self, n_part, n_page):
        self.cur.execute("SELECT id FROM pages WHERE part=? AND page=?" , (n_part, n_page))
        return self.cur.fetchone()
    
    def go_to_nearer_page(self, n_part, n_page, n):
        self.cur.execute("SELECT id FROM pages WHERE part=? AND page=?" , (n_part, n_page-n))
        return self.cur.fetchone()
    
    def page_ayat(self, sora, aya):
        self.cur.execute("""SELECT id FROM pages WHERE sora=? AND aya<=?""", (sora, aya))
        page = self.cur.fetchall()
        try: return page[-1][0]
        except: return 1
    
    def edit_tafsir(self, id_page, sura, aya, na):
        self.cur.execute('UPDATE pages SET sora=?, aya=?, na=? WHERE id=?', (sura, aya, na, id_page))
        self.con.commit()
    
    def get_title(self, id_page):
        self.cur.execute('SELECT tit FROM titles WHERE id<=?', (id_page,)) 
        try: tit = self.cur.fetchall()[-1][0]
        except: tit = '......'
        return tit
        
    def search(self, text, store, condition, phrase):
        len_book = len(self.list_pages)
        parts = int(len_book/200)
        remainder = len_book-(200*parts)
        s = 0
        v = 0    
        while v in range(parts+1):
            while (Gtk.events_pending()): Gtk.main_iteration()
            p1 = v*200
            p2 = (v+1)*200
            if v < parts:
                cond = 'id BETWEEN {} and {}'.format(p1, p2)
            elif v == parts:
                cond = 'id BETWEEN {} and {}'.format(p1, remainder)
            elif v > parts:
                pass  
            self.cur.execute("""SELECT id, part, page FROM pages WHERE {} AND {}""".format(cond, condition), phrase)
            i_pgs = self.cur.fetchall()
            for i in i_pgs:
                j = i[0]
                tit = self.get_title(j)
                try: pg = int(i[2])
                except: pg = 1
                try: pr = int(i[1])
                except: pr = 1
                store.append([j, s, self.book_name, tit, pr, pg, self.book, self.id_book])
                s += 1
            v += 1
    
    def all_page(self, *a):
        self.cur.execute("SELECT id, part, page FROM pages")
        return self.cur.fetchall()
    
    # a التعليقات---------------------------------------
        
    def show_comment(self, id_page):
        self.cur.execute('SELECT nass FROM com WHERE pgid=?', (id_page, ))
        com = self.cur.fetchone()
        return com
    
    def update_comment(self, id_page, comment):
        self.cur.execute('UPDATE com SET nass=? WHERE pgid=?', (comment, id_page))
        self.con.commit()
    
    def add_comment(self, id_page, comment):
        self.cur.execute('INSERT INTO com VALUES (?, ?)', (id_page, comment))
        self.con.commit() 
        
    def remove_comment(self, id_page):
        self.cur.execute('DELETE FROM com WHERE pgid=?', (id_page, ))
        self.con.commit()  
    
    #---------------------------------------------------
    def close_db(self, *a):
        self.cur.close()
        self.con.close()
        self.toc_ids = None
        self.toc_uniq = None
        self.list_pages = None
        self.len_index = None
        self.cur = None
        self.con = None
        del self.cur
        del self.con
        del self.toc_ids
        del self.toc_uniq 
        del self.list_pages
        del self.len_index
    
    # a بحث في صفحة معينة-----------------------------------
    
    def search_in_page(self, id_page, text):
        self.cur.execute('SELECT id FROM pages WHERE id=? AND fuzzy(nass) LIKE ?', (id_page, '%'+text+'%'))
        if len(self.cur.fetchall()) > 0: return True
        else: return False
        
    # a عدد الصفحات والأجزاء-----------------------------------
    
    def parts_pages(self, part=1):
        self.cur.execute('SELECT part FROM pages')
        parts = self.cur.fetchall()
        self.cur.execute('SELECT page FROM pages WHERE part=?' , (part, ))
        pages = self.cur.fetchall()
        try: return parts[-1][0], pages[-1][0]
        except: return 0, 0
        
    # a بحث في فهرس كتاب-----------------------------------
    
    def search_index(self, text):
        self.cur.execute('SELECT id, tit FROM titles WHERE fuzzy(tit) LIKE ? LIMIT 100', ('%'+text+'%', ))
        books = self.cur.fetchall()
        return books

# a قاعدة بيانات المصحف-------------------------------------------------------

class Othman(object):

    def __init__(self, *a):
        self.con=sqlite3.connect(asm_path.QURAN_DB)
        self.con.create_function('fuzzy', 1, asm_araby.fuzzy) 
        self.cur=self.con.cursor()
        try:
            self.cur.execute("SELECT rowid FROM quran order by rowid desc LIMIT 1")
            i=self.cur.fetchone()[0]
        except: raise IOError
        if i!=6236: raise TypeError
        
        
    def get_suras_names(self):
        self.cur.execute("SELECT id, sura_name, ayat FROM SuraNames")
        ls = []
        for i in self.cur.fetchall():
            ls.append([i[0], i[1], i[2]])
        return ls

    def get_sura_info(self, sura):
        self.cur.execute("SELECT id, sura_name, other_names, ayat FROM SuraNames WHERE id=?", (sura, ))
        sura_info = self.cur.fetchone()
        return sura_info
    
    def get_aya(self, id_binary):
        self.cur.execute("SELECT othmani FROM quran WHERE id_binary=?", (id_binary,))
        return self.cur.fetchone()[0]
    
    def get_ayat(self, sura, aya1, aya2):
        self.cur.execute("SELECT othmani FROM quran WHERE sura=? and aya BETWEEN ? and ?", (sura, aya1, aya2-1))
        return list(map(lambda i: i[0], self.cur.fetchall()))

    def search(self, text):
        s = '''fuzzy(imlai) LIKE ? ESCAPE "|"'''
        text=asm_araby.fuzzy(text)
        self.search_tokens=asm_araby.tokenize_search(text)
        l = list(map(lambda s: '%'+s.replace('|', '||').replace('%', '|%')+'%', self.search_tokens))
        if len(l) < 1: return []
        condition = ' AND '.join([s]*len(l))
        self.cur.execute("""SELECT sura, aya, page, othmani, imlai, id_binary  FROM Quran WHERE {} LIMIT 50""".format(condition, ), l)
        ayat = self.cur.fetchall()
        return ayat
    
    #-------------------------------------------------- 
    
    def text_in_page(self, page):
        self.cur.execute("SELECT id, othmani, sura, aya FROM quran WHERE page=?", (page, ))
        nasse = self.cur.fetchall()
        ls_text = [[],]
        for a in nasse:
            if a[3] == 1:
                ls_text.append(self.get_sura_info(a[2]))
                ls_text.append([a[1],])
            else:
                ls_text[-1].append(a[1])
        #del ls_text[0]
        return ls_text
 
    def first_page(self, id_m, data='sura'):
        self.cur.execute("SELECT page FROM quran WHERE {}=? LIMIT 1;".format(data,), (id_m, ))
        return self.cur.fetchone()[0]
    
    def aya_page(self, aya, sura):
        self.cur.execute("SELECT page FROM quran WHERE aya=? AND sura=? LIMIT 1;", (aya, sura))
        return self.cur.fetchone()[0]
    
    def ayat_in_page(self, page):
        self.cur.execute("SELECT sura, aya FROM quran WHERE page=?", (page,))
        return self.cur.fetchall()
    
    def info_page(self, page):
        self.cur.execute("SELECT sura, joze FROM quran WHERE page=? LIMIT 1;", (page,))
        p = self.cur.fetchone()
        info = self.get_sura_info(p[0])
        return info[1], p[1]
        
# a قاعدة بيانات المعجم----------------------------------
      
class DictDB(object):
    
    def firstletter(self, term):
        return term[0]
    
    def __init__(self, *a):
        self.con = sqlite3.connect(asm_path.MOEJAM_DB)
        self.con.create_function('firstletter', 1, self.firstletter)
        self.cur = self.con.cursor()
        
    
    def all_index(self, f_letter):
        self.cur.execute('SELECT term FROM dict WHERE firstletter(term)=? ORDER BY term', (f_letter, ))
        terms = self.cur.fetchall()
        return terms
    
    def show_charh(self, term):
        self.cur.execute('SELECT charh FROM dict WHERE term=?', (term, ))
        charh = self.cur.fetchall()
        return charh

# a قاعدة بيانات التراجم----------------------------------
     
class AuthorDB(object):
    
    def __init__(self, *a):
        self.con = sqlite3.connect(asm_path.AUTHOR_DB)
        self.con.create_function('fuzzy', 1, asm_araby.fuzzy_plus) 
        self.cur = self.con.cursor()
        
#        self.remove_comment()
#    
#    def remove_comment(self, *a):
#        self.cur.execute('DELETE FROM auth WHERE ad>1300')
#        self.con.commit()  
    
    def all_author(self, *a):
        self.cur.execute('SELECT authid, auth, lng FROM auth')
        auths = self.cur.fetchall()
        return auths
    
    def info_auth(self, id_auth):
        self.cur.execute('SELECT * FROM auth WHERE authid=?', (id_auth, ))
        auth = self.cur.fetchone()
        return auth
       
    def author(self, text):
        s = '''fuzzy(lng) LIKE ? ESCAPE "|"'''
        text = asm_araby.fuzzy(text)
        self.search_tokens = asm_araby.tokenize_search(text)
        l = list(map(lambda s: '%'+s.replace('|', '||').replace('%', '|%')+'%', self.search_tokens))
        if len(l) < 1: return []
        condition = ' AND '.join([s]*len(l))
        self.cur.execute("""SELECT authid, auth FROM auth WHERE {}""".format(condition), l)
        authors = self.cur.fetchall()
        return authors
    
# a قاعدة بيانات التراجم----------------------------------
   
class TarajimDB(object):
    
    def __init__(self, *a):
        self.con = sqlite3.connect(asm_path.TARAJIM_DB)
        self.con.create_function('fuzzy', 1, asm_araby.fuzzy_plus) 
        self.cur = self.con.cursor()
    
    def all_rawi(self, *a):
        self.cur.execute('SELECT id, name FROM rewat')
        rawis = self.cur.fetchall()
        return rawis
    
    def show_rawi(self, id_rawi):
        self.cur.execute('SELECT * FROM rewat WHERE id=?', (id_rawi, ))
        rawi = self.cur.fetchone()
        return rawi
       
    def tardjma(self, text):
        s = '''fuzzy(name) LIKE ? ESCAPE "|"'''
        text = asm_araby.fuzzy(text)
        self.search_tokens = asm_araby.tokenize_search(text)
        l = list(map(lambda s: '%'+s.replace('|', '||').replace('%', '|%')+'%', self.search_tokens))
        if len(l) < 1: return []
        condition = ' AND '.join([s]*len(l))
        self.cur.execute("""SELECT id, name FROM rewat WHERE {}""".format(condition), l)
        tarjama = self.cur.fetchall()
        return tarjama
