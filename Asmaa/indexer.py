# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import Gtk, GObject, Pango
import asm_customs, asm_araby, asm_path, asm_stemming
from asm_contacts import listDB, bookDB
from whoosh import index
from whoosh.fields import Schema, ID, TEXT
from whoosh.analysis import StandardAnalyzer, StemFilter
from whoosh.lang.porter import stem
from whoosh.qparser import QueryParser, OperatorsPlugin
from os.path import exists, join
import os, re




normalize_tb = {
    65: 97, 66: 98, 67: 99, 68: 100, 69: 101, 70: 102,
    71: 103, 72: 104, 73: 105, 74: 106, 75: 107, 76: 108,
    77: 109, 78: 110, 79: 111, 80: 112, 81: 113, 82: 114,
    83: 115, 84: 116, 85: 117, 86: 118, 87: 119, 88: 120,
    89: 121, 90: 122, 1600: None, 1569: 1575, 1570: 1575, 1571: 1575,
    1572: 1575, 1573: 1575, 1574: 1575, 1577: 1607, # teh marboota ->    haa
    1611: None, 1612: None, 1613: None, 1614: None, 1615: None,
    1616: None, 1617: None, 1618: None, 1609: 1575}
rm_prefix = re.compile(u"^(?:ا?[وف]?((?:[بك]?ال|لل?)|[اينت])?)")

rm_suffix = re.compile(u"(?:ا[نت]|[يهة]|ها|ي[هنة]|ون)$")
def removeArabicSuffix(word):
    if len(word) > 4:
        w = rm_suffix.sub("", word, 1)
        if len(w) > 2:
            return w
    return word
def removeArabicPrefix(word):
    if len(word) > 3:
        w = rm_prefix.sub("", word, 1)
        if len(w)>2:
            return w
    return word
def stemArabic(word):
    return removeArabicPrefix(removeArabicSuffix(unicode(word).translate(normalize_tb)))





def stemfn(word): return asm_stemming.get_root(stem(word))[0][0]
analyzer = StandardAnalyzer(expression = r"[\w\u064e\u064b\u064f\u064c\u0650\u064d\u0652\u0651\u0640]+\
(?:\.?[\w\u064e\u064b\u064f\u064c\u0650\u064d\u0652\u0651\u0640]+)*") | StemFilter(stemArabic)

schema = Schema(title=TEXT(stored=False, analyzer=analyzer), 
                content=TEXT(stored=False, analyzer=analyzer), 
                page=ID(stored=True))

if not exists(asm_path.INDEX_DIR_rw):
        os.mkdir(asm_path.INDEX_DIR_rw)
def indexing(id_book, title, content, page):
        new_idx = join(asm_path.INDEX_DIR_rw, str(id_book))
        if not exists(new_idx):
            os.mkdir(new_idx)
        ix = index.create_in(new_idx, schema)
        writer =  ix.writer()
        writer.add_document(title=title, content=content, page=page)
        writer.commit()