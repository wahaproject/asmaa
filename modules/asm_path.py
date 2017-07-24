# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from os.path import join, dirname, realpath, exists, expanduser, getsize
from gi.repository import Gtk
import asm_config
import asm_customs
from shutil import copyfile
from os import mkdir, getcwd
import sqlite3
import sys


#a------------------------------------------
if getattr(sys, 'frozen', False):
    APP_DIR = dirname(dirname(sys.executable))
else:
    APP_DIR = dirname(dirname(realpath(__file__)))
HOME_DIR       =   expanduser('~/.asmaa')
DATA_DIR          =   join(APP_DIR, 'asmaa-data')
ICON_DIR         =   join(DATA_DIR, 'icons')
DB_DIR             =   join(DATA_DIR, 'db')
QURAN_DB        =   join(DB_DIR, 'Quran.db')
TAFSIR_DB        =   join(DB_DIR, 'Tafsir.db')
AUTHOR_DB      =   join(DB_DIR, 'Author.db')
DALIL_DB          =   join(DB_DIR, 'Dalil.db')
MOEJAM_DB      =   join(DB_DIR, 'Moejam.db')
TARAJIM_DB      =   join(DB_DIR, 'Tarajim.db')
MOSHAF_DIR     =   join(DATA_DIR, 'moshaf')
DEFAULT_LIBRERY_DIR  =   join(APP_DIR, 'asmaa-librery') 
DEFAULT_LISTBOOK_FILE  =   join(DEFAULT_LIBRERY_DIR, 'Listbooks.db') 

#a------------------------------------------
def sure_start():
    dlg = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, Gtk.MessageType.WARNING,
                             Gtk.ButtonsType.NONE)
    dlg.set_markup('''
    لم يتمكن البرنامج من الاتصال بقاعدة البيانات،
    إذا كانت موجودة بالفعل فربما لم تربطها بالبرنامج، 
    أو قد يكون القرص الموجود عليه القاعدة غير مضموم،
    ماذا تريد أن تفعل ؟''')
    db_void = Gtk.LinkButton.new_with_label("http://sourceforge.net/projects/asmaalibrary/files/AsmaaLibrary.tar.gz/download",
                                                'تنزيل قاعدة بيانات للتجربة')
    no_lib = Gtk.Button('خروج')
    dlg.add_action_widget(no_lib, 1)
    sel_lib = Gtk.Button('تحديد المسار')
    dlg.add_action_widget(sel_lib, 2)
    new_lib = Gtk.Button('إنشاء قاعدة بيانات مفرغة')
    dlg.add_action_widget(new_lib, 3)
    if  exists(DEFAULT_LISTBOOK_FILE): 
        def_lib = Gtk.Button('المسار الافتراضي')
        dlg.add_action_widget(def_lib, 4)
    
    area = dlg.get_content_area()
    area.set_spacing(7)
    hbox = Gtk.HBox(False, 7)
    hbox.pack_end(db_void, False, False, 0)
    area.pack_start(hbox, False, False, 0)
    area.show_all()
    r = dlg.run()
    dlg.destroy()
    return r

if not exists(asm_config.getv('path')): 
    res = sure_start()
    # a تحديد المسار--------------------------
    if res == 2:
        open_dlg = Gtk.FileChooserDialog('تحديد مسار قاعدة البيانات',
                                         None, Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                         Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        
        Filter = Gtk.FileFilter()
        Filter.set_name(u"قاعدة البيانات")
        Filter.add_pattern("Listbooks.db")
        open_dlg.add_filter(Filter)
        res = open_dlg.run()
        if res == Gtk.ResponseType.OK:
            asm_config.setv('path', open_dlg.get_filenames()[0])          
            open_dlg.destroy()
        else:
            open_dlg.destroy()
            quit()   
        
    # a إلغاء التحديد-------------------------
    elif res == 1:
        my_return = 0
        quit()
        
    # a مكتبة مفرغة--------------------------
    elif res == 3:
        save_dlg = Gtk.FileChooserDialog('مسار قاعدة البيانات الجديدة', None,
                                    Gtk.FileChooserAction.SELECT_FOLDER,
                                    (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        res = save_dlg.run()
        if res == Gtk.ResponseType.OK:
            new_dir = join(save_dlg.get_filename(), 'مكتبة أسماء')
            if exists(join(new_dir, 'data', 'Listbooks.db')):
                asm_customs.erro(None, 'يوجد مكتبة في هذا الدليل بالفعل')
            else:
                if not exists(new_dir):
                    mkdir(new_dir)
                if not exists(join(new_dir, 'data')):
                    mkdir(join(new_dir, 'data'))
                if not exists(join(new_dir, 'books')):
                    mkdir(join(new_dir, 'books'))
                if not exists(join(new_dir, 'index')):
                    mkdir(join(new_dir, 'index'))
                con = sqlite3.connect(join(new_dir, 'data', 'Listbooks.db'))
                cur = con.cursor()
                cur.execute('CREATE TABLE groups (id_group integer primary key, \
                tit varchar(255), sub INTEGER, cat INTEGER)') 
                cur.execute('CREATE TABLE books (id_book integer primary key, tit varchar(255), \
                parent INTEGER, fav  INTEGER DEFAULT 0, last  INTEGER DEFAULT 1, cat  INTEGER DEFAULT 0,\
                tafsir  INTEGER DEFAULT 0, indx INTEGER DEFAULT 0)')
                asm_config.setv('path', join(new_dir, 'data', 'Listbooks.db'))
                asm_customs.info(None, 'تم إضافة مكتبة مفرغة جديدة')
        else:
            y_return = 0
            quit()
        save_dlg.destroy()
        
    # a المسار الافتراضي--------------------------
    elif res == 4:
        asm_config.setv('path', DEFAULT_LISTBOOK_FILE)
        
    # a إلغاء التحديد----------------------------    
    else:
        my_return = 0
        quit()
    library_path  = asm_config.getv('path')
    LIBRARY_DIR = dirname(dirname(library_path))
else:
    library_path = asm_config.getv('path')
    LIBRARY_DIR = dirname(dirname(library_path))
BOOK_DIR      =   join(LIBRARY_DIR, 'books')
DATA_DIR     =   join(LIBRARY_DIR, 'data')
INDEX_DIR     =   join(LIBRARY_DIR, 'index') 
LISTBOOK_FILE =   join(LIBRARY_DIR, 'data', 'Listbooks.db')  
    
# a إصلاحات------------------------------------------
try:    
    if not exists(join(LIBRARY_DIR, 'books')):
        mkdir(join(LIBRARY_DIR, 'books'))
except: pass
try:    
    if not exists(join(LIBRARY_DIR, 'index')):
        mkdir(join(LIBRARY_DIR, 'index'))
except: pass
try:
    if not exists(join(LIBRARY_DIR, 'fields-search')):
        mkdir(join(LIBRARY_DIR, 'fields-search'))
except: pass
try:    
    if not exists(join(LIBRARY_DIR, 'waraka-search')):
        mkdir(join(LIBRARY_DIR, 'waraka-search'))
except: pass

#a------------------------------------------
def can_modify(parent):
    if LIBRARY_DIR.startswith('/usr'):
        dlg = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL,
                                Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, 'لا يمكن التعديل على قاعدة البيانات إلا إذا قمت بنسخها إلى مسار تملك صلاحية التعديل عليه')
        dlg.run()
        dlg.destroy()
        return False
    else: return True
    