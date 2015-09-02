# -*- coding: utf-8 -*-

##############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
##############################################################################

from gi.repository import Gtk


class About(Gtk.AboutDialog):
    
    def __init__(self, parent):
        self.parent = parent
        Gtk.AboutDialog.__init__(self, parent = self.parent, wrap_license = True)
        self.set_program_name("مكتبة أسماء")
        self.set_version("2.5.2")
        self.set_icon_name("asmaa")
        self.set_logo_icon_name('asmaa')
        self.set_comments("""بديل للمكتبة الشاملة على لينكس""")
        self.set_website("http://www.linuxac.org")
        self.set_website_label('مجتمع لينكس العربي')
        self.set_authors(['',
                          '<asmaaarab@gmail.com> أحمد رغدي ',
                           ])
        self.set_license("""
        مكتبة أسماء2 برمجية حرة ؛
        بإمكانك إعادة توزيعها مع أو دون تعديلها ،
        تحت شروط الرخصة "وقف" ، توزّع مكتبة أسماء
        على أمل أن تكون مفيدةً لمن يستخدمها دون أدنى ضمان  ؛
        يمكنك أن تطلع على هذه الرخصة في صفحتها الموجودة
        على هذا الرابط
        http://www.ojuba.org/wiki/doku.php/waqf/license 
        """)
        self.run()
        self.destroy()
