# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################


from gi.repository import Gtk, WebKit
import re
import asm_path
import asm_customs
from os.path import join

head_html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<meta http-equiv="content-type" content="text/html; charset=utf-8" />\n'''

mafasil = ['</body>', '</html>','</pre>','/>','<head>','</title>','</head>','<body dir="rtl">','</div>']

# class نافذة أوراق البحث----------------------------------------------------------       
        
class EditHTML(Gtk.VBox):
    
    def on_action(self, w, action):
        self.editor.execute_script(
            "document.execCommand('{}', false, false);".format(action,))
    
    def on_unorderedlist(self, *a):
            self.editor.execute_script("document.execCommand('insertUnorderedList', null, '%s');")

    def on_orderedlist(self, *a):
            self.editor.execute_script("document.execCommand('insertOrderedList', null, '%s');")

    def on_select_fontnm(self, *a):
        if self.fontname.get_active() == -1: return
        v = self.fontname.get_active_iter()
        model = self.fontname.get_model()
        fname = model.get_value(v, 0)
        self.editor.execute_script("document.execCommand('fontname', null, '{}');".format(fname,))
        self.fontname.set_active(-1)
        
    def on_select_fontsz(self, *a):
        if self.fontsize.get_active() == -1: return
        v = self.fontsize.get_active_iter()
        model = self.fontsize.get_model()
        fsize = model.get_value(v, 1)
        self.editor.execute_script("document.execCommand('fontsize', null, '{}');".format(fsize,))
        self.fontsize.set_active(-1)

    def on_select_color(self, *a):
        dialog = Gtk.ColorSelectionDialog("اختر لونا")
        colorsel = dialog.get_color_selection()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            color = colorsel.get_current_color().to_string()
            color = "#" + "".join([color[1:3], color[5:7], color[9:11]])
            self.editor.execute_script("document.execCommand('forecolor', null, '{}');".format(color,))
        dialog.destroy()

    def on_removeFormat(self, *a):
        self.editor.execute_script("document.execCommand('removeFormat', null, '%s');")

    def on_save(self, *a):
        if self.myfile != None:
            with open(self.myfile, 'w+') as f: f.write(self.get_html())
            
    def on_print(self, *a):
        self.editor.execute_script("window.print();")
    
    def on_source(self, w):  
        self.editor.set_view_source_mode(w.get_active())
        self.open_html(self.myfile)
        if w.get_active():
            for a in self.toolbar.get_children():
                a.set_sensitive(False)
            w.set_sensitive(True)
        else:
            for a in self.toolbar.get_children():
                a.set_sensitive(True)
    
    def on_export(self, *a):
        template = head_html+self.get_html()+'\n</html>'
        save_dlg = Gtk.FileChooserDialog("تصدير إلى ملف HTML", None,
                                    Gtk.FileChooserAction.SAVE,
                                    (Gtk.STOCK_OK, Gtk.ResponseType.OK,
                                    Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        res = save_dlg.run()
        if res == Gtk.ResponseType.OK:
            file_save = save_dlg.get_filename()
            if file_save == None: return
            file_save = open(file_save+'.html', 'w')
            file_save.write(template)
            file_save.close()
        save_dlg.destroy()

    def get_html(self):
        self.editor.execute_script("document.title=document.documentElement.innerHTML;")
        text = self.editor.get_main_frame().get_title()
        f = re.compile(r'<title>.*</title>')
        new_text = re.sub(f, '<title>new</title>', text)
        for a in mafasil:
            new_text = re.sub(a, a+'\n', new_text)
        return new_text
    
    def  open_html(self, file_html):
        self.myfile = file_html
        with open(file_html) as f: self.editor.load_html_string(f.read(), "file:///")
    
    def clear_page(self):
        self.editor.load_html_string('', "file:///")
    
    def search_on_active(self, text):
        self.editor.search_text(text, False, True, True)
    
    def search_on_page(self, text):
        self.editor.search_text(text, False, True, True)
    
    def __init__(self):
        self.myfile = None
        Gtk.VBox.__init__(self)
        self.editor = WebKit.WebView()
        self.editor.set_editable(True)
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.editor)
        
        self.toolbar = Gtk.Toolbar()
        self.hb_tb = Gtk.Box(spacing=3,orientation=Gtk.Orientation.HORIZONTAL)
        self.pack_start(scroll, True, True, 0)
        self.hb_tb.pack_start(self.toolbar, True, True, 0)
        self.pack_start(self.hb_tb, False, False, 0)
        save = Gtk.ToolButton(stock_id=Gtk.STOCK_SAVE)
        save.connect('clicked', self.on_save)
        self.toolbar.insert(save, 0)
        export = asm_customs.tool_button(join(asm_path.ICON_DIR, 'html-24.png'), "", self.on_export)
        self.toolbar.insert(export, 1)
        source = Gtk.ToggleToolButton(stock_id=Gtk.STOCK_FILE)
        source.connect('toggled', self.on_source)
        self.toolbar.insert(source, 2)
        printi = Gtk.ToolButton(stock_id=Gtk.STOCK_PRINT)
        printi.connect('clicked', self.on_print)
        self.toolbar.insert(printi, 3)
        #self.toolbar.insert(Gtk.SeparatorToolItem(), 3)
        undo = Gtk.ToolButton(stock_id=Gtk.STOCK_UNDO)
        undo.connect('clicked', self.on_action, 'Undo')
        self.toolbar.insert(undo, 4)
        redo = Gtk.ToolButton(stock_id=Gtk.STOCK_REDO)
        redo.connect('clicked', self.on_action, 'Redo')
        self.toolbar.insert(redo, 5)
        self.toolbar.insert(Gtk.SeparatorToolItem(), 6)
        fontname_item = Gtk.ToolItem.new()
        hb, self.fontname = asm_customs.button_fontnm()
        fontname_item.add(hb)
        self.fontname.connect('changed', self.on_select_fontnm)
        self.toolbar.insert(fontname_item, 7)
        fontsize_item = Gtk.ToolItem.new()
        hb, self.fontsize = asm_customs.button_fontsz()
        fontsize_item.add(hb)
        self.fontsize.connect('changed', self.on_select_fontsz)
        self.toolbar.insert(fontsize_item, 8)
        bold = Gtk.ToolButton(stock_id=Gtk.STOCK_BOLD)
        bold.connect('clicked', self.on_action, 'Bold')
        self.toolbar.insert(bold, 9)
        italic = Gtk.ToolButton(stock_id=Gtk.STOCK_ITALIC)
        italic.connect('clicked', self.on_action, 'Italic')
        self.toolbar.insert(italic, 10)
        underline = Gtk.ToolButton(stock_id=Gtk.STOCK_UNDERLINE)
        underline.connect('clicked', self.on_action, 'Underline')
        self.toolbar.insert(underline, 11)
        strikethrough = Gtk.ToolButton(stock_id=Gtk.STOCK_STRIKETHROUGH)
        strikethrough.connect('clicked', self.on_action, 'Strikethrough')
        self.toolbar.insert(strikethrough, 12)
        self.toolbar.insert(Gtk.SeparatorToolItem(), 13)
        color = Gtk.ToolButton(stock_id=Gtk.STOCK_SELECT_COLOR)
        color.connect('clicked', self.on_select_color)
        self.toolbar.insert(color, 14)
        self.toolbar.insert(Gtk.SeparatorToolItem(), 15)
        justifyleft = Gtk.ToolButton(stock_id=Gtk.STOCK_JUSTIFY_LEFT)
        justifyleft.connect('clicked', self.on_action, 'Justifyleft')
        self.toolbar.insert(justifyleft, 16)
        justifyright = Gtk.ToolButton(stock_id=Gtk.STOCK_JUSTIFY_RIGHT)
        justifyright.connect('clicked', self.on_action, 'Justifyright')
        self.toolbar.insert(justifyright, 17)
        justifycenter = Gtk.ToolButton(stock_id=Gtk.STOCK_JUSTIFY_CENTER)
        justifycenter.connect('clicked', self.on_action, 'Justifycenter')
        self.toolbar.insert(justifycenter, 18)
        justifyfull = Gtk.ToolButton(stock_id=Gtk.STOCK_JUSTIFY_FILL)
        justifyfull.connect('clicked', self.on_action, 'Justifyfull')
        self.toolbar.insert(justifyfull, 19)
        self.toolbar.insert(Gtk.SeparatorToolItem(), 20)
        orderedlist = asm_customs.tool_button(join(asm_path.ICON_DIR, 'OrderedList.png'), "", self.on_orderedlist)
        self.toolbar.insert(orderedlist, 21)
        unorderedlist = asm_customs.tool_button(join(asm_path.ICON_DIR, 'UnorderedList.png'), "", self.on_unorderedlist)
        self.toolbar.insert(unorderedlist, 22)
        self.toolbar.insert(Gtk.SeparatorToolItem(), 23)
        removeFormat = Gtk.ToolButton(stock_id=Gtk.STOCK_REMOVE)
        removeFormat.set_tooltip_text('حذف جميع التنسيقات')
        removeFormat.connect('clicked', self.on_removeFormat)
        self.toolbar.insert(removeFormat, 24)

 
    