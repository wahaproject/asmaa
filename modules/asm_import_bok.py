# -*- coding: utf-8 -*-

import sqlite3
from gi.repository import Gtk
from os.path import join, exists
import re, os, sys
import asm_path
import asm_customs
from asm_contacts import listDB
from subprocess import Popen, PIPE

class load_list_books_from_shamela(object):
    
    def __init__(self, ifile_main, ifile_spacial, store_books, comments, shorts):
        self.cats = []
        self.store_books = store_books
        self.store_books.clear()
        self.no_all_book = 0
        self.comments = comments
        self.shorts = shorts
        self.ifile_main = ifile_main
        self.ifile_spacial = ifile_spacial
        self.load_list()
    
    def get_books_part(self, id_part, ss):
        contents = Popen(['mdb-export', '-d', 'new_col', '-R', '\nnew_row', self.ifile_main, "0bok"], 
               0, stdout=PIPE, env={'MDB_JET3_CHARSET':'cp1256'}).communicate()[0].decode("utf8")
        list_contents = contents.split('new_row')
        for a in range(len(list_contents)-1):
            contents0 = re.sub(r'"', '', list_contents[a])
            contents0 = contents0.strip()
            #contents0 = contents0.lower()
            if a == 0: 
                motif = contents0.split('\n')
                motif0 = motif[0].split('new_col')
                motif0 = list(map(lambda i: i.lower(), motif0))
                cols = self.get_cols("0bok", motif0)
            else:
                motif0 = contents0.split('new_col')
                if len(motif0) == 1: continue
                else:
                    if motif0[cols['cat']] == id_part:
                        self.store_books.append(ss, [True, int(motif0[cols[u'bkid']]), motif0[cols[u'bk']], int(motif0[cols[u'cat']]), 
                                                     motif0[cols[u'betaka']], motif0[cols[u'inf']],motif0[cols[u'auth']],
                                                     motif0[cols[u'tafseernam']], int(motif0[cols[u'islamshort']]), 
                                                     int(motif0[cols[u'archive']])])
                    self.no_all_book += 1
    
    def get_cols(self, table, motif):
        cols_dict = {}
        if table == '0bok':
            for a in [u'bkid', u'bk', u'cat', u'betaka', u'inf',u'auth',u'tafseernam', u'islamshort', u'archive']:
                cols_dict[a] = motif.index(a)
        elif table == '0cat':
            for a in [u'id', u'name']:
                cols_dict[a] = motif.index(a)
        elif table == 'com':
            for a in [u'com', u'bk', u'id']:
                cols_dict[a] = motif.index(a)
        elif table == 'shorts':
            for a in [u'bk', u'ramz', u'nass']:
                cols_dict[a] = motif.index(a)
        return cols_dict
    
    def load_list(self):
        for a in [u'0cat',u'com', u'shorts']:
            if a  == u'0cat': file0 = self.ifile_main
            else: file0 = self.ifile_spacial
            contents_main = Popen(['mdb-export', '-d', 'new_col', '-R', '\nnew_row', file0, a],   
                                  0, stdout=PIPE, env={'MDB_JET3_CHARSET':'cp1256'}).communicate()[0].decode("utf8")
            list_contents_main = contents_main.split('new_row')
            for p in range(len(list_contents_main)):
                contents0_main = re.sub(r'"', '', list_contents_main[p])
                #contents0_main = contents0_main.strip()
                if p == 0: 
                    motif = contents0_main.split('\n')
                    motif0 = motif[0].split('new_col')
                    motif0 = list(map(lambda i: i.lower(), motif0))
                    cols = self.get_cols(a, motif0)
                else:
                    motif0 = contents0_main.split('new_col')
                    if len(motif0) == 1: continue
                    else:
                        if a == '0cat':
                            while (Gtk.events_pending()): Gtk.main_iteration()
                            ss = self.store_books.append(None, [True, int(motif0[cols['id']]), motif0[cols['name']],0, 
                                                               u'', u'', u'', u'', 0, 0])
                            self.get_books_part(motif0[cols['id']], ss)
                        elif a == 'com':
                            if int(motif0[cols['bk']]) in self.comments : 
                                ls = self.comments[int(motif0[cols['bk']])]
                                ls1 = [[int(motif0[cols['id']]), motif0[cols['com']]]]
                                self.comments[int(motif0[cols['bk']])] = ls+ls1
                            else: self.comments[int(motif0[cols['bk']])] = [[int(motif0[cols['id']]), motif0[cols['com']]],]
                        elif a == 'shorts':
                            if int(motif0[cols['bk']]) in self.shorts : 
                                ls = self.shorts[int(motif0[cols['bk']])]
                                ls1 = [[motif0[cols['ramz']], motif0[cols['nass']]]]
                                self.shorts[int(motif0[cols['bk']])] = ls+ls1
                            else: 
                                self.shorts[int(motif0[cols['bk']])] = [[motif0[cols['ramz']], motif0[cols['nass']]],]
        
class DB_from_MDB(object):
    
    def __init__(self, ifile, nm_group, info_list, comments, shorts, archive):
        # info_list = 0='BkId', 1='Bk', 2='Betaka', 3='Inf', 4='Auth', 5='TafseerNam', 6='IslamShort'
        #self.cols = []
        self.info_list = info_list
        self.comments = comments
        self.shorts = shorts
        self.archive = archive
        #self.table_list = []
        self.list_book = listDB()
        self.nm_group = nm_group
        self.id_group = self.list_book.add_part(self.nm_group)
        if not exists(join(asm_path.BOOK_DIR, self.nm_group)):
            os.mkdir(join(asm_path.BOOK_DIR, self.nm_group))
        self.ifile = ifile
        self.creat_newDB()
    
    def get_cols(self, table, motif, id_book=0):
        cols_dict = {}
        if table == 't'+str(id_book) or table == 'title':
            for a in [u'tit', u'lvl', u'sub', u'id']:
                cols_dict[a] = motif.index(a)
        elif table == 'b'+str(id_book) or table == 'book':
            for a in [u'id', u'nass', u'part', u'page', u'hno', u'sora', u'aya', u'na']:
                try: cols_dict[a] = motif.index(a)
                except: pass
        return cols_dict
    
    def get_ids_titles(self, id_book):
        if self.archive == 0: table = 'title'
        else: table = 't'+str(id_book)
        ids_titles = []
        contents = Popen(['mdb-export', '-d', 'new_col', '-R', '\nnew_row', self.ifile, table], 
               0, stdout=PIPE, env={'MDB_JET3_CHARSET':'cp1256'}).communicate()[0].decode("utf8")
        list_contents = contents.split('new_row')
        for a in range(len(list_contents)-1):
            contents0 = re.sub(r'"', '', list_contents[a])
            #contents0 = contents0.strip()
            if a == 0:
                motif = contents0.split('\n')
                motif0 = motif[0].split('new_col') 
                motif0 = list(map(lambda i: i.lower(), motif0))
                cols = self.get_cols(table, motif0, id_book)
            else:
                motif0 = contents0.split('new_col')
                if len(motif0) == 1: continue
                else:
                    ids_titles.append(motif0[cols['id']])
        return ids_titles
        
    def get_tables(self):
        table_names = Popen(["mdb-tables", "-1", self.ifile], stdout=PIPE).communicate()[0].decode("utf8")
        self.table_list = table_names.splitlines()
        sys.stdout.flush()
   
    def creat_newDB(self):
        # info_list = 0='BkId', 1='Bk', 2='Betaka', 3='Inf', 4='Auth', 5='TafseerNam', 6='IslamShort'
        self.get_tables()
        id_book = self.info_list[0]
        nm_book = (self.info_list[1]).replace(u"/", u"-")
        ids_titles = self.get_ids_titles(id_book)
        page_dict = {}
        if len(self.info_list[5]) > 2: is_tafsir = 1
        else: is_tafsir = 0
        db = join(asm_path.BOOK_DIR, self.nm_group, nm_book+u'.asm')
        if exists(db): os.unlink(db)
        con = sqlite3.connect(db, isolation_level=None)
        cur = con.cursor() 
        for tb in asm_customs.schema.keys():
            cur.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(tb, asm_customs.schema[tb]))
        cur.execute("BEGIN;")
        cur.execute('INSERT INTO main VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (self.info_list[1], u'',
                     0, self.info_list[2], self.info_list[3], 
                     self.info_list[4], 0, self.info_list[6], is_tafsir, 0, 0.1))
        if self.archive == 0: tables = ['book', 'title']
        else: tables = ['b'+str(id_book), 't'+str(id_book)]
        for table in tables:
            contents = Popen(['mdb-export', '-d', 'new_col', '-R', '\nnew_row', self.ifile, table], 
                   0, stdout=PIPE, env={'MDB_JET3_CHARSET':'cp1256'}).communicate()[0].decode("utf8")
            list_contents = contents.split('new_row')
            for b in range(len(list_contents)-1):
                contents0 = re.sub(r'"', '', list_contents[b])
                #contents0 = contents0.strip()
                if b == 0: 
                    motif = contents0.split('\n')
                    motif0 = motif[0].split('new_col')
                    motif0 = list(map(lambda i: i.lower(), motif0))
                    cols = self.get_cols(table, motif0, id_book)
                else:
                    motif0 = contents0.split('new_col')
                    if len(motif0) == 1: continue
                    else:
                        if table == 'b'+str(id_book) or table == 'book':
                            if motif0[cols['id']] in ids_titles: page_dict[motif0[cols['id']]] = b
                            if 'hno' in cols: hno = motif0[cols['hno']]
                            else: hno = 0
                            if 'aya' in cols: aya = motif0[cols['aya']]
                            else: aya = 0
                            if 'sora' in cols: sora = motif0[cols['sora']]
                            else: sora = 0
                            if 'na' in cols: na = motif0[cols['na']]
                            else: na = 0
                            if 'part' in cols: part = motif0[cols['part']]
                            else: part = 1
                            cur.execute('INSERT INTO pages VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (b, motif0[cols['nass']],
                                                        part, motif0[cols['page']], hno, sora, aya, na))
                        elif table == 't'+str(id_book) or table == 'title':
                            if motif0[cols['id']] in page_dict :
                                cur.execute('INSERT INTO titles VALUES (?, ?, ?, ?)', (page_dict[motif0[cols['id']]],
                                                             motif0[cols['tit']], motif0[cols['lvl']], motif0[cols['sub']]))
        #------------------------------------------------------------------
        if int(id_book) in self.comments :
            for c in self.comments[int(id_book)]:
                cur.execute('INSERT INTO com VALUES (?, ?)', (c[0], c[1]))
        if int(id_book) in self.shorts:        
            for s in self.shorts[int(id_book)]:
                cur.execute('INSERT INTO shorts VALUES (?, ?)', (s[0], s[1]))
            
        con.commit()
        self.list_book.add_book(nm_book, self.id_group, is_tafsir, 0)


class DB_from_BOK(object):
    
    def __init__(self, ifile, nm_group, id_group):
        self.cols = []
        self.nm_group = nm_group
        self.id_group = id_group
        self.table_list = []
        self.list_book = listDB()
        self.ifile = ifile
        self.creat_newDB()
    
    def get_cols(self, table, motif, id_book=0):
        cols_dict = {}
        if table == 'Main':
            for a in [u'bkid', u'bk', u'betaka', u'inf',u'auth',u'tafseernam', u'islamshort', u'ad']:
                cols_dict[a] = motif.index(a)
        elif table == 'Shorts':
            for a in [u'bk', u'ramz', u'nass']:
                cols_dict[a] = motif.index(a)
        elif table == 'com':
            for a in [u'com', u'bk', u'id']:
                cols_dict[a] = motif.index(a)
        elif table == 't'+str(id_book):
            for a in [u'tit', u'lvl', u'sub', u'id']:
                cols_dict[a] = motif.index(a)
        elif table == 'b'+str(id_book):
            for a in [u'id', u'nass', u'part', u'page', u'hno', u'sora', u'aya', u'na']:
                try: cols_dict[a] = motif.index(a)
                except: pass
        return cols_dict
    
    def get_ids_titles(self, id_book):
        ids_titles = []
        contents = Popen(['mdb-export', '-d', 'new_col', '-R', '\nnew_row', self.ifile, "t"+str(id_book)], 
               0, stdout=PIPE, env={'MDB_JET3_CHARSET':'cp1256'}).communicate()[0].decode("utf8")
        list_contents = contents.split('new_row')
        for a in range(len(list_contents)-1):
            contents0 = re.sub(r'"', '', list_contents[a])
            #contents0 = contents0.strip()
            if a == 0: 
                motif = contents0.split('\n')
                motif0 = motif[0].split('new_col')
                motif0 = list(map(lambda i: i.lower(), motif0))
                cols = self.get_cols("t"+str(id_book), motif0, id_book)
            else:
                motif0 = contents0.split('new_col')
                if len(motif0) == 1: continue
                else:
                    ids_titles.append(motif0[cols['id']])
        return ids_titles
        
    def get_tables(self):
        table_names = Popen(["mdb-tables", "-1", self.ifile], stdout=PIPE).communicate()[0].decode("utf8")
        self.table_list = table_names.splitlines()
        sys.stdout.flush()
   
    def creat_newDB(self):
        self.get_tables()
        contents_main = Popen(['mdb-export', '-d', 'new_col', '-R', '\nnew_row', self.ifile, 'Main'], 
                       0, stdout=PIPE, env={'MDB_JET3_CHARSET':'cp1256'}).communicate()[0].decode("utf8")
        list_contents_main = contents_main.split('new_row')
        for a in range(len(list_contents_main)):
            contents0_main = re.sub(r'"', '', list_contents_main[a])
            #contents0_main = contents0_main.strip()
            if a == 0: 
                motif = contents0_main.split('\n')
                motif_main = motif[0].split('new_col')
                motif_main = list(map(lambda i: i.lower(), motif_main))
                cols_main = self.get_cols('Main', motif_main)
            else:
                motif_main = contents0_main.split('new_col')
                if len(motif_main) == 1: continue
                else:
                    id_book = motif_main[cols_main['bkid']]
                    nm_book = motif_main[cols_main['bk']].replace(u"/", u"-")
                    ids_titles = self.get_ids_titles(id_book)
                    page_dict = {}
                    if len(motif_main[cols_main['tafseernam']]) > 2: is_tafsir = 1
                    else: is_tafsir = 0
                    db = join(asm_path.BOOK_DIR, self.nm_group, nm_book+".asm")
                    if exists(db): os.unlink(db)
                    con = sqlite3.connect(db, isolation_level=None)
                    cur = con.cursor() 
                    for tb in asm_customs.schema.keys():
                        cur.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(tb, asm_customs.schema[tb]))
                    cur.execute("BEGIN;")
                    cur.execute('INSERT INTO main VALUES (?,?,?,?,?,?,?,?,?,?,?)', (motif_main[cols_main['bk']], '',
                                 0, motif_main[cols_main['betaka']], motif_main[cols_main['inf']], 
                                 motif_main[cols_main['auth']], motif_main[cols_main['ad']], 
                                 motif_main[cols_main['islamshort']], is_tafsir, 0, 0.1))
                    for table in ['Shorts', 'b'+str(id_book), 't'+str(id_book), 'com']:
                        contents = Popen(['mdb-export', '-d', 'new_col', '-R', '\nnew_row', self.ifile, table], 
                               0, stdout=PIPE, env={'MDB_JET3_CHARSET':'cp1256'}).communicate()[0].decode("utf8")
                        list_contents = contents.split('new_row')
                        for b in range(len(list_contents)-1):
                            contents0 = re.sub(r'"', '', list_contents[b])
                            #contents0 = contents0.strip()
                            if b == 0: 
                                motif = contents0.split('\n')
                                motif0 = motif[0].split('new_col')
                                motif0 = list(map(lambda i: i.lower(), motif0))
                                cols = self.get_cols(table, motif0, id_book)
                            else:
                                motif0 = contents0.split('new_col')
                                if len(motif0) == 1: continue
                                else:
                                    if table == 'Shorts':
                                        try: 
                                            if motif0[cols['bk']] == id_book:
                                                cur.execute('INSERT INTO shorts VALUES (?, ?)', (motif0[cols['ramz']], motif0[cols['nass']]))
                                        except: pass
                                    elif table == 'b'+str(id_book):
                                        if motif0[cols['id']] in ids_titles: page_dict[motif0[cols['id']]] = b
                                        if 'hno' in cols: hno = motif0[cols['hno']]
                                        else: hno = 0
                                        if 'aya' in cols: aya = motif0[cols['aya']]
                                        else: aya = 0
                                        if 'sora' in cols: sora = motif0[cols['sora']]
                                        else: sora = 0
                                        if 'na' in cols: na = motif0[cols['na']]
                                        else: na = 0
                                        if 'part' in cols: part = motif0[cols['part']]
                                        else: part = 1
                                        cur.execute('INSERT INTO pages VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (b, motif0[cols['nass']],
                                                                    part, motif0[cols['page']], hno, sora, aya, na))
                                    elif table == 't'+str(id_book):
                                        if motif0[cols['id']] in page_dict :
                                            cur.execute('INSERT INTO titles VALUES (?, ?, ?, ?)', (page_dict[motif0[cols['id']]],
                                                                         motif0[cols['tit']], motif0[cols['lvl']], motif0[cols['sub']]))
                                    elif table == 'com':
                                            try: 
                                                if motif0[cols['bk']] == id_book:
                                                    cur.execute('INSERT INTO com VALUES (?, ?)', (motif0[cols['id']], motif0[cols['com']]))
                                            except: pass
                    con.commit()
                    self.list_book.add_book(nm_book, self.id_group, is_tafsir, 0)
        
def DB_from_doc(nm_book, id_group, nm_group, list_page, list_title):
    db = join(asm_path.BOOK_DIR, nm_group, nm_book+'.asm')
    if exists(db): os.unlink(db)
    con = sqlite3.connect(db, isolation_level=None)
    cur = con.cursor() 
    for tb in asm_customs.schema.keys():
        cur.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(tb, asm_customs.schema[tb]))
    cur.execute("BEGIN;")
    cur.execute('INSERT INTO main VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                (nm_book,'', 0, nm_book, nm_book, 0, 0, 0, 0, 0, 0.1))
    for pg in list_page:
        cur.execute('INSERT INTO pages VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (pg[0], pg[1], pg[2], 
                        pg[3], 0, 0, 0, 0))
    for ti in list_title:
        cur.execute('INSERT INTO titles VALUES (?, ?, ?, ?)', (ti[0], ti[1], ti[2], ti[3]))
    con.commit()
    listDB().add_book(nm_book, id_group, 0)