# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

import asm_path
from os.path import join
from gi.repository import Gtk
from asm_contacts import listDB

class Count(Gtk.Box):
    
    def __init__(self, *a):
        self.db = listDB()
    
    def fast(self, *a):
        template0  = u'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <html>
        <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>إحصاءات مكتبة أسماء</title>
        </head>
        <body>
        <table
        style="vertical-align: middle; text-align: center; width: 500px; height: 700px; margin-left: auto; margin-right: auto;"
        border = 1"1" cellpadding = 1"2" cellspacing = 1"2">
        <caption style="caption-side: right;"><br>
        </caption><tbody>
        <tr>
        <td style="background-color: rgb(204, 51, 204);">عدد الكتب<br>
        </td>
        <td style="background-color: rgb(51, 204, 255);">الأقسام</td>
        </tr>
        '''
        template1  = u''''''
        for a in self.db.all_parts():
            template1 += u'''
            <tr>
            <td>{}<br>
            </td>
            <td style="background-color: rgb(255, 190, 94);">{}<br>
            </td>
            </tr>
            '''.format(len(self.db.books_part(a[0])), a[1])
            
        template2  = u'''
        </tbody>
        </table>
        <br>
        <br>
        </body>
        </html>
        '''
        
        file_html = join(asm_path.HOME_DIR, u'count.html')
        file_count = open(file_html, 'w')
        new_template = template0+template1+template2
        file_count.write(new_template)
        file_count.close()
        return file_html
        
    def detail(self, *a):
        template0  = u'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <html>
        <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <title>إحصاءات مكتبة أسماء</title>
        </head>
        <body>
        <table
        style="vertical-align: middle; text-align: center; width: 900px; height: 700px; margin-left: auto; margin-right: auto;"
        border = 1"1" cellpadding = 1"2" cellspacing = 1"2">
        <caption style="caption-side: right;"><br>
        </caption><tbody>
        <tr>
        <td style="background-color: rgb(204, 51, 204);">عدد الكتب<br>
        </td>
        <td style="background-color: rgb(51, 204, 255);">الأقسام</td>
        </tr>
        '''
        template1  = u''
        for a in self.db.all_parts():
            books = u''
            for b in self.db.books_part(a[0]):
                books += b[1]+u'<br>'
            template1 += u'''
            <tr>
            <td>{}<br>
            </td>
            <td style="background-color: rgb(255, 190, 94);">{}<br>
            </td>
            </tr>
            '''.format(books, a[1])
            
        template2  = u'''
        </tbody>
        </table>
        <br>
        <br>
        </body>
        </html>
        '''
        
        file_html = join(asm_path.HOME_DIR, u'count.html')
        file_count = open(file_html, 'w')
        new_template = template0+template1+template2
        file_count.write(new_template)
        file_count.close()
        return file_html
