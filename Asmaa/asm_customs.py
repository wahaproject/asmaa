# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  ########
##############################################################################

from gi.repository import Gtk, Gdk, Pango
import Asmaa.asm_araby as asm_araby
import re

Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL)

#a------------------------------------------
version = '2.5.2'
#a--------------------------------------------------
schema = {
        'main': "bk TEXT, shortname TEXT, cat INTEGER, betaka TEXT, inf TEXT, authno INTEGER DEFAULT 0, \
            auth_death INTEGER DEFAULT 0, islamshort INTEGER DEFAULT 0, is_tafseer INTEGER DEFAULT 0, \
            is_sharh INTEGER DEFAULT 0, version INTEGER DEFAULT 0.1", 
        'shorts': "ramz TEXT, nass TEXT", 
        'shrooh': "matnid INTEGER, sharhid INTEGER, matnpg INTEGER, sharhpg INTEGER", 
        'pages': "id INTEGER PRIMARY KEY, nass TEXT, part INTEGER DEFAULT 1, page INTEGER DEFAULT 1, hno INTEGER DEFAULT 0, \
            sora INTEGER DEFAULT 0, aya INTEGER DEFAULT 0, na INTEGER DEFAULT 0", 
        'titles': "id INTEGER, tit TEXT, lvl INTEGER DEFAULT 1, sub INTEGER DEFAULT 0", 
        'com': "pgid INTEGER PRIMARY KEY, nass TEXT"
}

#a------------------------------------------
def info(parent, msg):
    dlg = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL,
                            Gtk.MessageType.INFO, Gtk.ButtonsType.CLOSE, msg)
    dlg.run()
    dlg.destroy()

#a------------------------------------------
def erro(parent, msg):
    dlg = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL,
                            Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, msg)
    dlg.run()
    dlg.destroy()

#a------------------------------------------
def sure(parent, msg):
    dlg = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL, Gtk.MessageType.WARNING,
                             Gtk.ButtonsType.YES_NO)
    dlg.set_markup(msg)                         
    r = dlg.run()
    dlg.destroy()
    return r

#a------------------------------------------
def rgba(value):
    if value.startswith('#'):
        value = value.lstrip('#')
        v = int(len(value)/3)
        R = int(value[0:v], 16)/15.999**v
        G = int(value[v:2*v], 16)/15.999**v
        B = int(value[2*v:3*v], 16)/15.999**v
    else:
        value = value.lstrip('rgb')
        v = eval(value)
        R = v[0]/255.0
        G = v[1]/255.0
        B = v[2]/255.0
    A = 1.0
    return Gdk.RGBA(R, G, B, A)

#a-------------------------------------------
def rgb(value):
    if value.startswith('#'):
        value = value.lstrip('#')
        v = int(len(value)/3)
        R = int(value[0:v], 16)/16**(v-2)
        G = int(value[v:2*v], 16)/16**(v-2)
        B = int(value[2*v:3*v], 16)/16**(v-2)
    else:
        value = value.lstrip('rgb')
        v = eval(value)
        R = v[0]
        G = v[1]
        B = v[2]
    return  'rgb({}, {}, {})'.format(R, G, B)

#a------------------------------------------
def tool_button(icon_file, tooltip, function, data=None):
        ''' Build custom toolbutton '''
        toolbtn = Gtk.ToolButton()
        widget = Gtk.Image.new_from_file(icon_file)
        toolbtn.set_icon_widget(widget)
        toolbtn.set_tooltip_text(tooltip)
        toolbtn.connect('clicked', function, data)
        return toolbtn

#a------------------------------------------
def combo(ls, name):
    new_ls = []
    new_ls.extend(ls)
    hb = Gtk.HBox(False, 6) 
    store = Gtk.ListStore(int, str, int)
    cmt = Gtk.ComboBox.new_with_model(store)
    for a in new_ls:
        if len(a) == 3: store.append([a[0], a[1], a[2]])
        else: store.append([a[0], a[1], 0])
    renderer_text = Gtk.CellRendererText()
    renderer_text.set_property("ellipsize-set", True)
    renderer_text.set_property("ellipsize", Pango.EllipsizeMode.END)
    if name == u"التفسير":
        renderer_text.set_property("max-width-chars",24)
        renderer_text.set_property("weight", 24)
    else:
        renderer_text.set_property("max-width-chars",14)
        renderer_text.set_property("weight", 14)
    cmt.pack_start(renderer_text, True)
    cmt.add_attribute(renderer_text, "text", 1)
    lab = Gtk.Label(name)
    lab.set_alignment(0,0.5)
    if name == u"التفسير":
        return cmt
    else:
        hb.pack_start(lab, False, False, 0)
        hb.pack_end(cmt, False, False, 0)
        return hb, cmt
    

#a------------------------------------------
def button_fontnm():
    list_font = [[u"Amiri", u"أميري"], [u"Simplified Naskh", u"نسخ مبسط"], [u'AlHor', u"الحور"], [u"KacstBook", u"KacstBook"],
             [u"KacstLetter", u"KacstLetter"], [u'KacstNaskh', u"KacstNaskh"], [u'KacstFarsi', u"KacstFarsi"], 
             [u"KacstOne", u"KacstOne"], [u"KacstQurn", u"KacstQurn"], [u'KacstTitle', u"KacstTitle"]]
    store = Gtk.ListStore(str, str)
    cmt = Gtk.ComboBox.new_with_model(store)
    for a in list_font:
        store.append([a[0], a[1]])
    renderer_text = Gtk.CellRendererText()
    renderer_text.set_property("ellipsize-set", True)
    renderer_text.set_property("weight", 14)
    renderer_text.set_property("ellipsize", Pango.EllipsizeMode.END)
    cmt.pack_start(renderer_text, True)
    cmt.add_attribute(renderer_text, "text", 1)
    cmt.set_size_request(40, -1)
    lab = Gtk.Label('الخط')
    hb = Gtk.HBox(False, 0) 
    hb.set_border_width(3)
    hb.pack_start(lab, False, False, 0)
    hb.pack_start(cmt, False, False, 0)
    return hb, cmt
 
#a------------------------------------------
def button_fontsz():
    list_font = [[u'1', u'1'], [u'2', u'2'], [u'3', u'3'], [u'4', u'4'], 
                [u'5', u'5'], [u'6', u'6'], [u'7', u'7']] 
    store = Gtk.ListStore(str, str)
    cmt = Gtk.ComboBox.new_with_model(store)
    for a in list_font:
        store.append([a[0], a[1]])
    renderer_text = Gtk.CellRendererText()
    renderer_text.set_property("ellipsize-set", True)
    renderer_text.set_property("weight", 14)
    renderer_text.set_property("ellipsize", Pango.EllipsizeMode.END)
    cmt.pack_start(renderer_text, True)
    cmt.add_attribute(renderer_text, "text", 0)
    cmt.set_size_request(40, -1)
    lab = Gtk.Label('حجم')
    hb = Gtk.HBox(False, 0) 
    hb.set_border_width(3)
    hb.pack_start(lab, False, False, 0)
    hb.pack_start(cmt, False, False, 0)
    return hb, cmt

#a------------------------------------------
def value_active(combo, n=0):
    if combo.get_active() == -1: return None
    v = combo.get_active_iter()
    model = combo.get_model()
    value = model.get_value(v, n)
    return value

#a------------------------------------------
def search_and_mark(text_buff, text_tag, text, start, tt, view):
    iter_min = None
    end = text_buff.get_end_iter()
    match = start.forward_search(text, Gtk.TextSearchFlags.CASE_INSENSITIVE, end)
    if match != None:
        match_start, match_end = match
        text_buff.apply_tag(text_tag, match_start, match_end)
        if match_start and (not iter_min or iter_min.compare(match_start) > 0): 
                iter_min = match_start
        if tt == 1:
            search_and_mark(text_buff, text_tag, text, match_end, 1, view)
    return iter_min
        
        
def with_tag(text_buff, text_tag, ls, tt=0, view=None):
    iter_min = None
    for text in ls:
        cursor_mark = text_buff.get_insert()
        start = text_buff.get_iter_at_mark(cursor_mark)
        if start.get_offset() == text_buff.get_char_count():
            start = text_buff.get_start_iter()
        iter_min = search_and_mark(text_buff, text_tag, text, start, tt, view)
    if iter_min and view != None:
        view.scroll_to_iter(iter_min, 0, True, 0.0, 1.0)

#a------------------------------------------
class ViewClass(Gtk.TextView):
    __gtype_name__ = 'View'
    def __init__(self, *a):
        Gtk.TextView.__init__(self)
        self.set_cursor_visible(False)
        self.set_editable(False)
        self.set_right_margin(10)
        self.set_left_margin(10)
        self.set_wrap_mode(Gtk.WrapMode.WORD)
        #self.get_width = self.get_size_request()[0]
        
#a------------------------------------------
class ViewBitaka(Gtk.TextView):
    __gtype_name__ = 'Viewbitaka'
    def __init__(self, *a):
        Gtk.TextView.__init__(self)
        self.set_cursor_visible(False)
        self.set_editable(False)
        self.set_right_margin(5)
        self.set_left_margin(5)
        self.set_wrap_mode(Gtk.WrapMode.WORD)
                
#a------------------------------------------
class ButtonClass(Gtk.Button):
    __gtype_name__ = 'button'
    def __init__(self, name):
        Gtk.Button.__init__(self, name)
        label = Gtk.Label()
        label.set_text(name)
        pangolayout = label.get_layout()
        d = pangolayout.get_pixel_size()
        w = ((d[0]/25)+2)*25
        self.set_size_request(w, 30)
    
#a------------------------------------------
class TreeIndex(Gtk.TreeView):
    __gtype_name__ = 'Treeindex'
    def __init__(self, *a):
        Gtk.TreeView.__init__(self)
        
#a------------------------------------------
class TreeParts(Gtk.TreeView):
    __gtype_name__ = 'TreeParts'
    def __init__(self, *a):
        Gtk.TreeView.__init__(self)
        
#a------------------------------------------
class TreeBooks(Gtk.TreeView):
    __gtype_name__ = 'TreeBooks'
    def __init__(self, *a):
        Gtk.TreeView.__init__(self)

def first_term(text):
    text = re.sub('\n', ' ', text)
    text = re.sub(' +', ' ', text)
    text = text.strip()
    ls = text.split(' ')
    txt = asm_araby.stripTatweel(ls[0])
    return txt
        