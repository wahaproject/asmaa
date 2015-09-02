# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import Gtk, GObject, Pango
import Asmaa.asm_path as asm_path
import Asmaa.asm_customs as asm_customs
import Asmaa.asm_araby as asm_araby 
import Asmaa.asm_stemming as asm_stemming
from Asmaa.asm_contacts import listDB, bookDB
from whoosh import index
from whoosh.fields import Schema, ID, TEXT
from whoosh.analysis import StandardAnalyzer, StemFilter
from whoosh.lang.porter import stem
from whoosh.qparser import QueryParser, OperatorsPlugin
from os.path import exists, join
import os, re




#normalize_tb = {
#    65: 97, 66: 98, 67: 99, 68: 100, 69: 101, 70: 102,
#    71: 103, 72: 104, 73: 105, 74: 106, 75: 107, 76: 108,
#    77: 109, 78: 110, 79: 111, 80: 112, 81: 113, 82: 114,
#    83: 115, 84: 116, 85: 117, 86: 118, 87: 119, 88: 120,
#    89: 121, 90: 122, 1600: None, 1569: 1575, 1570: 1575, 1571: 1575,
#    1572: 1575, 1573: 1575, 1574: 1575, 1577: 1607, # teh marboota ->    haa
#    1611: None, 1612: None, 1613: None, 1614: None, 1615: None,
#    1616: None, 1617: None, 1618: None, 1609: 1575}

#
def get_stem(word):
    word =  asm_araby.normalize(word)
    print (word)
    if len(word) < 3: return word
    root = re.match("^(?:ا?(و|ف)?(((((ك|ب)?(ال)?)|(لل?))?(م?(ن|ست|ت)?))|((س|ل)?(ي|ن|ت|ا)?(ن|ست|ت)?))?)"+\
                    "(?P<root>([ا-ي]{3}))"\
                    +"(?:ي?(((((و|ا|ي)ن?)|(ا?ت)|(نا?))?(((ك|ه|ت)(م(ا|و)|ن)?)|ي|نا)?((ك|ه)(م(ا|و)|ن)?)?)|ه)?)$"\
                    , word)
    if root == None: 
        root = re.match("^(?:ا?(و|ف)?(((((ك|ب)?(ال)?)|(لل?))?(م?(ن|ست|ت)?))|((س|ل)?(ي|ن|ت|ا)?(ن|ست|ت)?))?)"+\
                        "(?P<root>([ا-ي][ا-ي][ا-ي][ا-ي]))"\
                        +"(?:ي?(((((و|ا|ي)ن?)|(ا?ت)|(نا?))?(((ك|ه|ت)(م(ا|و)|ن)?)|ي|نا)?((ك|ه)(م(ا|و)|ن)?)?)|ه)?)$"\
                        , word)
    if root == None: 
        root = re.match("^(?:ا?(و|ف)?(((((ك|ب)?(ال)?)|(لل?))?(م?(ن|ست|ت)?))|((س|ل)?(ي|ن|ت|ا)?(ن|ست|ت)?))?)"+\
                        "(?P<root>([ا-ي][ا-ي][ا-ي][ا-ي][ا-ي]))"\
                        +"(?:ي?(((((و|ا|ي)ن?)|(ا?ت)|(نا?))?(((ك|ه|ت)(م(ا|و)|ن)?)|ي|نا)?((ك|ه)(م(ا|و)|ن)?)?)|ه)?)$"\
                        , word)

    g = root.groupdict()
    r = g.get("root")
    print (r, "fffffffffffffffffffffffff")
    return r


def get_match(word, exp, n):
    if n == 0:
        root = re.match(exp+"(?P<root>([ا-ي][ا-ي][ا-ي]))$", word)
        if root == None: root = re.match(exp+"(?P<root>([ا-ي][ا-ي][ا-ي][ا-ي]))$", word)
        if root == None: root = re.match(exp+"(?P<root>([ا-ي][ا-ي][ا-ي][ا-ي][ا-ي]))$", word)
        if root == None: root = re.match(exp+"(?P<root>([ا-ي][ا-ي][ا-ي][ا-ي][ا-ي][ا-ي]))$", word)
    elif n == 1:
        root = re.match("^(?P<root>([ا-ي][ا-ي][ا-ي]))"+exp, word)
        if root == None: root = re.match("^(?P<root>([ا-ي][ا-ي][ا-ي][ا-ي]))"+exp, word)
        if root == None: root = re.match("^(?P<root>([ا-ي][ا-ي][ا-ي][ا-ي][ا-ي]))"+exp, word)
        if root == None: root = re.match("^(?P<root>([ا-ي][ا-ي][ا-ي][ا-ي][ا-ي][ا-ي]))"+exp, word)
        if root == None: root = re.match("^(?P<root>([ا-ي][ا-ي][ا-ي][ا-ي][ا-ي][ا-ي][ا-ي]))"+exp, word)
        if root == None: root = re.match("^(?P<root>([ا-ي][ا-ي][ا-ي][ا-ي][ا-ي][ا-ي][ا-ي][ا-ي]))"+exp, word)
    if root == None:  return word
    else:
        g = root.groupdict()
        r = g.get("root")
        return r

rm_prefix = re.compile("^(?:ا?(و|ف)?(((((ك|ب)?(ال)?)|(لل?))?(م?(ن|ست|ت)?))|((س|ل)?(ي|ن|ت|ا)?(ن|ست|ت)?))?)")
rm_suffix = re.compile("(?:ي?(((((و|ا|ي)ن?)|(ا?ت)|(نا?))?(((ك|ه|ت)(م(ا|و)|ن)?)|ي|نا)?((ك|ه)(م(ا|و)|ن)?)?)|ه)?)$")

print (rm_prefix.match("افبالطائف").group())

word_prefix = "^(?:ا?[وف]?((لل?|س)|([كبو]?(ال)?))?)"
word_suffix = "(?:(ت((م[او]?)|ن)?|(وا?))?(ن[اي]?)?([كه]((م?[او]?)|ن)?|نا)?([كه]((م?ا?)|ن)?|نا)?)$"
letter_prefix = "^(?:([اميت](ن|ت|ست)?)?)"
letter_suffix = "(?:(ي?((ا[تن]?)|([يو]?ن?)|ة)?)|(انة|اء|ا[ءو]ات)?)$"
#
#def get_stem(text):
#    print (text)
#    text = asm_araby.normalize(text)
#    print (text)
#    if len(text) < 3: return text
#    text = get_match(text, word_suffix, 1)
#    text = get_match(text, "^(?:ا?(و|ف)?(((((ك|ب)?(ال)?)|(لل?))?(م?(ن|ست|ت)?))|((س|ل)?(ي|ن|ت|ا)?(ن|ست|ت)?))?)", 0)
#    text = get_match(text, letter_suffix, 1)
#    text = get_match(text, letter_prefix, 0)
#    print (text)
#    return text

#print (get_stem('بالطائف'))

#rm_prefix = re.compile(u"^(?:ا?[وف]?((?:[بك]?ال|لل?)|[اينت])?)")
#
#rm_suffix = re.compile(u"(?:ا[نت]|[يهة]|ها|ي[هنة]|ون)$")
#
#def rv_Suffix_Prefix(word):
##    word = str(word).translate(normalize_tb)
#    if len(word) < 3: return word
#    print (word)
##    if len(word) > 3:
##        word = rm_suffix.sub("", word, 1)
##    if len(word) > 3:
##        word = rm_prefix.sub("", word, 1)
#    try: word = asm_stemming.get_root(word)[0][0]
#    except: pass
#    print (word)
#    return word

analyzer = StandardAnalyzer() | StemFilter(get_stem)

schema = Schema(
                book=ID(stored=True),
                title=TEXT(stored=False, analyzer=analyzer), 
                content=TEXT(stored=False, analyzer=analyzer), 
                page=ID(stored=True))

if not exists(asm_path.INDEX_DIR_rw):
        os.mkdir(asm_path.INDEX_DIR_rw)

class WinIndexer(Gtk.Dialog):
    
    def __init__(self, parent):
        self.parent = parent
        self.db = listDB()
        self.selected_books = []
        self.build()

    def creat_writer_index(self, nm_index):
        new_idx = join(asm_path.INDEX_DIR_rw, nm_index)
        if not exists(new_idx):
            os.mkdir(new_idx)
            ix = index.create_in(new_idx, schema)
        else: 
            ix = index.open_dir(new_idx)
        return ix.writer()
    
    def start_indexation(self, *a):
        self.btn_index_start.set_sensitive(False)
        writer = self.creat_writer_index('my_index')
        s = 0
        for id_book in self.selected_books:
            s += 1
            self.progress.set_fraction(float(s)/float(len(self.selected_books)))
            filebook = self.db.file_book(id_book)
            db = bookDB(filebook, id_book)
            for a in db.all_page():
                title = "-".join(db.titles_page(a[0]))
                if title == "": title = "-"
                content = db.get_text_body(a[0])[2]
                page = str(a[0])  
                book = str(id_book)
                writer.add_document(book=book, title=title, content=content, page=page)
                print (s)
            self.db.add_indexed(id_book)
        writer.commit()
        asm_customs.info(self, "تمت عملية الفهرسة")
        self.destroy()
    
    def load_books(self, *a):
        self.store_books.clear()
        groups = self.db.all_parts()
        for a in groups:
            while (Gtk.events_pending()): Gtk.main_iteration()
            aa = self.store_books.append(None, [None, a[1], a[0]])
            books = self.db.books_part(a[0])
            for b in books:
                if not self.db.is_indexed(b[0]):
                    self.store_books.append(aa, [None, b[1], b[0]])
    
    def add_to_listbooks(self, model, itr, fixed):
        id_book = model.get_value(itr, 2)
        i = model.iter_parent(itr)
        if i != None: 
            if fixed: 
                if id_book not in self.selected_books:
                    self.selected_books.append(id_book)
            else:
                if id_book in self.selected_books:
                    self.selected_books.remove(id_book)
    
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
                self.add_to_listbooks(model, iter1, fixed1)
                d += 1
        fixed = not fixed
        model.set(itr, 0, fixed)
        self.add_to_listbooks(model, itr, fixed)
    
    def select_o(self, model, path, i, bool1):
        bool0 = model.get_value(i,0)
        if bool0 != bool1: 
            model.set_value(i,0, bool1)
            self.add_to_listbooks(model, i, bool1)
            return False
    
    def select_all(self, *a):
        if self.all_books.get_active():
            try: self.store_books.foreach(self.select_o, True)
            except: pass
        else:
            try: self.store_books.foreach(self.select_o, False)
            except: pass
    
    # a دوال البحث في قائمة الكتب
    
    def search_in_index(self, model, path, i, my_books):
        txt = model.get(i,1)[0]
        text, path0 = my_books[0], my_books[2]
        if asm_araby.fuzzy(text) in asm_araby.fuzzy(txt) and path.compare(path0) > 0: 
            self.tree_books.expand_to_path(path)
            self.tree_books.scroll_to_cell(path)
            self.sel_books.select_path(path)
            return True 
        else:
            return False
    
    def search_entry_cb(self, *a):
        text = self.entry_search.get_text()
        model = self.store_books
        i = model.get_iter_first()
        path = model.get_path(i)
        try: self.store_books.foreach(self.search_in_index, [text, model, path, i])
        except: pass
    
    def search_cb(self, *a):
        model, i = self.sel_books.get_selected()
        if not i:
            i = model.get_iter_first()
        path = model.get_path(i)
        text = self.entry_search.get_text()
        if text == u'': return
        try: self.store_books.foreach(self.search_in_index, [text, model, path, i])
        except: pass
    
    def build(self, *a):
        Gtk.Dialog.__init__(self, parent=self.parent)
        self.set_border_width(3)
        self.set_icon_name("asmaa")
        self.set_size_request(620, 450)
        self.connect('delete-event', lambda *a: self.destroy())
        vbox = self.vbox
        
        hb_bar = Gtk.HeaderBar()
        hb_bar.set_title("نافذة الفهرسة")
        hb_bar.set_show_close_button(True)
        self.set_titlebar(hb_bar)

        hbox = Gtk.Box(spacing=7,orientation=Gtk.Orientation.HORIZONTAL)
        try: self.entry_search = Gtk.SearchEntry()
        except: self.entry_search = Gtk.Entry()
        self.entry_search.set_placeholder_text('بحث عن كتاب')
        self.entry_search.connect('changed', self.search_entry_cb)
        hbox.pack_end(self.entry_search, False, False, 0)
        search_btn = Gtk.ToolButton(stock_id=Gtk.STOCK_FIND)
        search_btn.connect('clicked', self.search_cb)
        search_btn.set_tooltip_text('ابحث عن النتيجة الموالية')
        hbox.pack_end(search_btn, False, False, 0)
        
        self.store_books = Gtk.TreeStore(GObject.TYPE_BOOLEAN, GObject.TYPE_STRING, GObject.TYPE_INT)
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
        columntoggle = Gtk.TreeViewColumn("#", celltoggle)
        columntext = Gtk.TreeViewColumn("الكتب غير المفهرسة", celltext, text = 1 )
        columntext.set_expand(True)
        columntoggle.add_attribute( celltoggle, "active", 0)
        celltoggle.connect('toggled', self.fixed_toggled, self.store_books)
        self.tree_books.append_column(columntoggle)
        self.tree_books.append_column(columntext)
        vbox.pack_start(scroll, True, True, 3)
        
        self.progress = Gtk.ProgressBar()
        vbox.pack_start(self.progress, False, False, 3)
        
        self.all_books = Gtk.CheckButton('الكل')
        self.all_books.connect('toggled', self.select_all) 
        hbox.pack_start(self.all_books, False, False, 0)
        
        self.btn_index_start = asm_customs.ButtonClass('فهرسة')
        self.btn_index_start.connect('clicked', self.start_indexation)
        hb_bar.pack_start(self.btn_index_start)
        vbox.pack_start(hbox, False, False, 0)
        self.show_all()
        self.load_books()

# a-----------------------------------
class SearchIndexed():
    
    def search_in_index(self, text, dict_perf, dict_field, limit):
        if dict_field == 'nass': 
            field = 'content'
        else: 
            field = 'title'
        new_index = join(asm_path.INDEX_DIR_rw, 'my_index')
        ix = index.open_dir(new_index)
        qp = QueryParser(field, schema=ix.schema)
        op = OperatorsPlugin(And = r"&", Or = r"\|", AndNot = r"&!", AndMaybe = r"&~", Not = r'!')
        qp.replace_plugin(op)
        q = qp.parse(text)
        with ix.searcher() as s:
            r = s.search(q, limit=limit)
            return r
            
#for a in os.listdir(path='/media/rr/raghdi-01/مكتبة أسماء/index'):
#print (SearchIndexed().search_in_index('الجميل الصادر', 0, 'nass', 10000))
