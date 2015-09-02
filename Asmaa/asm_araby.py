#!/usr/bin/python
# -*- coding=utf-8 -*-
#---
#
# ------------
# Description:
# ------------
#
# Arabic codes
#
# (C) Copyright 2010, Taha Zerrouki
# -----------------
#  $Date: 2010/03/01
#  $Author: Taha Zerrouki$
#  $Revision: 0.1 $
#  This program is written under the Gnu Public License.
#
"""
Arabic module
"""
import re, itertools
#class araby:
"""
the arabic chars contains all arabic letters, a sub class of unicode,
"""

COMMA            = '\u060C'
SEMICOLON        = '\u061B'
QUESTION         = '\u061F'
HAMZA            = '\u0621'
ALEF_MADDA       = '\u0622'
ALEF_HAMZA_ABOVE = '\u0623'
WAW_HAMZA        = '\u0624'
ALEF_HAMZA_BELOW = '\u0625'
YEH_HAMZA        = '\u0626'
ALEF             = '\u0627'
BEH              = '\u0628'
TEH_MARBUTA      = '\u0629'
TEH              = '\u062a'
THEH             = '\u062b'
JEEM             = '\u062c'
HAH              = '\u062d'
KHAH             = '\u062e'
DAL              = '\u062f'
THAL             = '\u0630'
REH              = '\u0631'
ZAIN             = '\u0632'
SEEN             = '\u0633'
SHEEN            = '\u0634'
SAD              = '\u0635'
DAD              = '\u0636'
TAH              = '\u0637'
ZAH              = '\u0638'
AIN              = '\u0639'
GHAIN            = '\u063a'
TATWEEL          = '\u0640'
FEH              = '\u0641'
QAF              = '\u0642'
KAF              = '\u0643'
LAM              = '\u0644'
MEEM             = '\u0645'
NOON             = '\u0646'
HEH              = '\u0647'
WAW              = '\u0648'
ALEF_MAKSURA     = '\u0649'
YEH              = '\u064a'
MADDA_ABOVE      = '\u0653'
HAMZA_ABOVE      = '\u0654'
HAMZA_BELOW      = '\u0655'
ZERO             = '\u0660'
ONE              = '\u0661'
TWO              = '\u0662'
THREE            = '\u0663'
FOUR             = '\u0664'
FIVE             = '\u0665'
SIX              = '\u0666'
SEVEN            = '\u0667'
EIGHT            = '\u0668'
NINE             = '\u0669'
PERCENT          = '\u066a'
DECIMAL          = '\u066b'
THOUSANDS        = '\u066c'
STAR             = '\u066d'
MINI_ALEF        = '\u0670'
ALEF_WASLA       = '\u0671'
FULL_STOP        = '\u06d4'
BYTE_ORDER_MARK  = '\ufeff'

# Diacritics
FATHATAN         = '\u064b'
DAMMATAN         = '\u064c'
KASRATAN         = '\u064d'
FATHA            = '\u064e'
DAMMA            = '\u064f'
KASRA            = '\u0650'
SHADDA           = '\u0651'
SUKUN            = '\u0652'

# Small Letters
SMALL_ALEF      ="\u0670"
SMALL_WAW       ="\u06E5"
SMALL_YEH       ="\u06E6"
#Ligatures
LAM_ALEF                    ='\ufefb'
LAM_ALEF_HAMZA_ABOVE        ='\ufef7'
LAM_ALEF_HAMZA_BELOW        ='\ufef9'
LAM_ALEF_MADDA_ABOVE        ='\ufef5'
simple_LAM_ALEF             ='\u0644\u0627'
simple_LAM_ALEF_HAMZA_ABOVE ='\u0644\u0623'
simple_LAM_ALEF_HAMZA_BELOW ='\u0644\u0625'
simple_LAM_ALEF_MADDA_ABOVE ='\u0644\u0622'
# groups
LETTERS=''.join([
        ALEF , BEH , TEH  , TEH_MARBUTA  , THEH  , JEEM  , HAH , KHAH ,
        DAL   , THAL  , REH   , ZAIN  , SEEN   , SHEEN  , SAD , DAD , TAH   , ZAH   ,
        AIN   , GHAIN   , FEH  , QAF , KAF , LAM , MEEM , NOON, HEH , WAW, YEH  ,
        HAMZA  ,  ALEF_MADDA , ALEF_HAMZA_ABOVE , WAW_HAMZA   , ALEF_HAMZA_BELOW  , YEH_HAMZA  ,ALEF_MAKSURA
        ])

TASHKEEL =(FATHATAN, DAMMATAN, KASRATAN,
            FATHA,DAMMA,KASRA,
            SUKUN,
            SHADDA);
HARAKAT =(  FATHATAN,   DAMMATAN,   KASRATAN,
            FATHA,  DAMMA,  KASRA,
            SUKUN
            );
SHORTHARAKAT =( FATHA,  DAMMA,  KASRA, SUKUN);

TANWIN =(FATHATAN,  DAMMATAN,   KASRATAN);


LIGUATURES=(
            LAM_ALEF,
            LAM_ALEF_HAMZA_ABOVE,
            LAM_ALEF_HAMZA_BELOW,
            LAM_ALEF_MADDA_ABOVE,
            );
HAMZAT=(
            HAMZA,
            WAW_HAMZA,
            YEH_HAMZA,
            HAMZA_ABOVE,
            HAMZA_BELOW,
            ALEF_HAMZA_BELOW,
            ALEF_HAMZA_ABOVE,
            );
ALEFAT=(
            ALEF,
            ALEF_MADDA,
            ALEF_HAMZA_ABOVE,
            ALEF_HAMZA_BELOW,
            ALEF_WASLA,
            ALEF_MAKSURA,
            SMALL_ALEF,

        );
WEAK   = ( ALEF, WAW, YEH, ALEF_MAKSURA);
YEHLIKE= ( YEH,  YEH_HAMZA,  ALEF_MAKSURA,   SMALL_YEH  );

WAWLIKE     =   ( WAW,  WAW_HAMZA,  SMALL_WAW );
TEHLIKE     =   ( TEH,  TEH_MARBUTA );

SMALL   =( SMALL_ALEF, SMALL_WAW, SMALL_YEH)
MOON =(HAMZA            ,
        ALEF_MADDA       ,
        ALEF_HAMZA_ABOVE ,
        ALEF_HAMZA_BELOW ,
        ALEF             ,
        BEH              ,
        JEEM             ,
        HAH              ,
        KHAH             ,
        AIN              ,
        GHAIN            ,
        FEH              ,
        QAF              ,
        KAF              ,
        MEEM             ,
        HEH              ,
        WAW              ,
        YEH
    );
SUN=(
        TEH              ,
        THEH             ,
        DAL              ,
        THAL             ,
        REH              ,
        ZAIN             ,
        SEEN             ,
        SHEEN            ,
        SAD              ,
        DAD              ,
        TAH              ,
        ZAH              ,
        LAM              ,
        NOON             ,
    );
AlphabeticOrder={
                ALEF             : 1,
                BEH              : 2,
                TEH              : 3,
                TEH_MARBUTA      : 3,
                THEH             : 4,
                JEEM             : 5,
                HAH              : 6,
                KHAH             : 7,
                DAL              : 8,
                THAL             : 9,
                REH              : 10,
                ZAIN             : 11,
                SEEN             : 12,
                SHEEN            : 13,
                SAD              : 14,
                DAD              : 15,
                TAH              : 16,
                ZAH              : 17,
                AIN              : 18,
                GHAIN            : 19,
                FEH              : 20,
                QAF              : 21,
                KAF              : 22,
                LAM              : 23,
                MEEM             : 24,
                NOON             : 25,
                HEH              : 26,
                WAW              : 27,
                YEH              : 28,
                HAMZA            : 29,

                ALEF_MADDA       : 29,
                ALEF_HAMZA_ABOVE : 29,
                WAW_HAMZA        : 29,
                ALEF_HAMZA_BELOW : 29,
                YEH_HAMZA        : 29,
                }
NAMES ={
                ALEF             :  "ألف",
                BEH              : "باء",
                TEH              : 'تاء' ,
                TEH_MARBUTA      : 'تاء مربوطة' ,
                THEH             : 'ثاء' ,
                JEEM             : 'جيم' ,
                HAH              : 'حاء' ,
                KHAH             : 'خاء' ,
                DAL              : 'دال' ,
                THAL             : 'ذال' ,
                REH              : 'راء' ,
                ZAIN             : 'زاي' ,
                SEEN             : 'سين' ,
                SHEEN            : 'شين' ,
                SAD              : 'صاد' ,
                DAD              : 'ضاد' ,
                TAH              : 'طاء' ,
                ZAH              : 'ظاء' ,
                AIN              : 'عين' ,
                GHAIN            : 'غين' ,
                FEH              : 'فاء' ,
                QAF              : 'قاف' ,
                KAF              : 'كاف' ,
                LAM              : 'لام' ,
                MEEM             : 'ميم' ,
                NOON             : 'نون' ,
                HEH              : 'هاء' ,
                WAW              : 'واو' ,
                YEH              : 'ياء' ,
                HAMZA            : 'همزة' ,

                TATWEEL          : 'تطويل' ,
                ALEF_MADDA       : 'ألف ممدودة' ,
                ALEF_MAKSURA      : 'ألف مقصورة' ,
                ALEF_HAMZA_ABOVE : 'همزة على الألف' ,
                WAW_HAMZA        : 'همزة على الواو' ,
                ALEF_HAMZA_BELOW : 'همزة تحت الألف' ,
                YEH_HAMZA        : 'همزة على الياء' ,
                FATHATAN         : 'فتحتان',
                DAMMATAN         : 'ضمتان',
                KASRATAN         : 'كسرتان',
                FATHA            : 'فتحة',
                DAMMA            : 'ضمة',
                KASRA            : 'كسرة',
                SHADDA           : 'شدة',
                SUKUN            : 'سكون',
                }

# regular expretion
HARAKAT_pattern =re.compile(r"["+"".join(HARAKAT)+"]")
TASHKEEL_pattern =re.compile(r"["+"".join(TASHKEEL)+"]")
HAMZAT_pattern =re.compile(r"["+"".join(HAMZAT)+"]");
ALEFAT_pattern =re.compile(r"["+"".join(ALEFAT)+"]");
LIGUATURES_pattern =re.compile(r"["+"".join(LIGUATURES)+"]");

################################################
#{ is letter functions
################################################
def isSukun(archar):
    """Checks for Arabic Sukun Mark.
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar==SUKUN:
        return True;
    else: return False;

def isShadda(archar):
    """Checks for Arabic Shadda Mark.
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar==SHADDA:
        return True;
    else: return False;

def isTatweel(archar):
    """Checks for Arabic Tatweel letter modifier.
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar==TATWEEL:
        return True;
    else: return False;
def isTanwin(archar):
    """Checks for Arabic Tanwin Marks (FATHATAN, DAMMATAN, KASRATAN).
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar in TANWIN:
        return True;
    else: return False;

def isTashkeel(archar):
    """Checks for Arabic Tashkeel Marks (FATHA,DAMMA,KASRA, SUKUN, SHADDA, FATHATAN,DAMMATAN, KASRATAn).
    @param archar: arabic unicode char
    @type archar: unicode
    """
##        if re.search(TASHKEEL,word):
    if  archar in  TASHKEEL:
        return True;
    else: return False;

def isHaraka(archar):
    """Checks for Arabic Harakat Marks (FATHA,DAMMA,KASRA,SUKUN,TANWIN).
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar in HARAKAT:
        return True;
    else: return False;

def isShortharaka(archar):
    """Checks for Arabic  short Harakat Marks (FATHA,DAMMA,KASRA,SUKUN).
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar in SHORTHARAKAT:
        return True;
    else: return False;

def isLigature(archar):
    """Checks for Arabic  Ligatures like LamAlef.
    (LAM_ALEF, LAM_ALEF_HAMZA_ABOVE, LAM_ALEF_HAMZA_BELOW, LAM_ALEF_MADDA_ABOVE)
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar in LIGUATURES:
        return True;
    else: return False;

def isHamza(archar):
    """Checks for Arabic  Hamza forms.
    HAMZAT are (HAMZA, WAW_HAMZA, YEH_HAMZA, HAMZA_ABOVE, HAMZA_BELOW,ALEF_HAMZA_BELOW, ALEF_HAMZA_ABOVE )
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar in HAMZAT:
        return True;
    else: return False;

def isAlef(archar):
    """Checks for Arabic Alef forms.
    ALEFAT=(ALEF, ALEF_MADDA, ALEF_HAMZA_ABOVE, ALEF_HAMZA_BELOW,ALEF_WASLA, ALEF_MAKSURA );
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar in ALEFAT:
        return True;
    else: return False;

def isYehlike(archar):
    """Checks for Arabic Yeh forms.
    Yeh forms : YEH, YEH_HAMZA, SMALL_YEH, ALEF_MAKSURA
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar in YEHLIKE:
        return True;
    else: return False;

def isWawlike(archar):
    """Checks for Arabic Waw like forms.
    Waw forms : WAW, WAW_HAMZA, SMALL_WAW
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar in WAWLIKE:
        return True;
    else: return False;

def isTeh(archar):
    """Checks for Arabic Teh forms.
    Teh forms : TEH, TEH_MARBUTA
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar in TEHLIKE:
        return True;
    else: return False;
def isSmall(archar):
    """Checks for Arabic Small letters.
    SMALL Letters : SMALL ALEF, SMALL WAW, SMALL YEH
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar in SMALL:
        return True;
    else: return False;

def isWeak(archar):
    """Checks for Arabic Weak letters.
    Weak Letters : ALEF, WAW, YEH, ALEF_MAKSURA
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar in WEAK:
        return True;
    else: return False;

def isMoon(archar):
    """Checks for Arabic Moon letters.
    Moon Letters :
    @param archar: arabic unicode char
    @type archar: unicode
    """

    if archar in MOON:
        return True;
    else: return False;

def isSun(archar):
    """Checks for Arabic Sun letters.
    Moon Letters :
    @param archar: arabic unicode char
    @type archar: unicode
    """
    if archar in SUN:
        return True;
    else: return False;
#####################################
#{ general  letter functions
#####################################
def order(archar):
    """return Arabic letter order between 1 and 29.
    Alef order is 1, Yeh is 28, Hamza is 29.
    Teh Marbuta has the same ordre with Teh, 3.
    @param archar: arabic unicode char
    @type archar: unicode
    @return: arabic order.
    @rtype: integer;
    """
    if AlphabeticOrder.has_key(archar):
        return AlphabeticOrder[archar];
    else: return 0;

def name(archar):
    """return Arabic letter name in arabic.
    Alef order is 1, Yeh is 28, Hamza is 29.
    Teh Marbuta has the same ordre with Teh, 3.
    @param archar: arabic unicode char
    @type archar: unicode
    @return: arabic name.
    @rtype: unicode;
    """
    if NAMES.has_key(archar):
        return NAMES[archar];
    else:
        return '';

#def arabicrange(self):
#    """return a list of arabic characteres .
#    Return a list of characteres between \u060c to \u0652
#    @return: list of arabic characteres.
#    @rtype: unicode;
#    """
#    mylist=[];
#    for i in range(0x0600, 0x00653):
#        try :
#            mylist.append(unichr(i));
#        except ValueError:
#            pass;
#    return mylist;


#####################################
#{ Has letter functions
#####################################
def hasShadda(word):
    """Checks if the arabic word  contains shadda.
    @param word: arabic unicode char
    @type word: unicode
    """
    if re.search(SHADDA,word):
        return True;
    else:
        return False;

#####################################
#{ word and text functions
#####################################
def isVocalized(word):
    """Checks if the arabic word is vocalized.
    the word musn't  have any spaces and pounctuations.
    @param word: arabic unicode char
    @type word: unicode
    """
    if word.isalpha(): return False;
#        n (FATHA,DAMMAN,KASRA):
    else:
        if re.search(HARAKAT_pattern,word):
            return True;
        else:
            return False;
def isVocalizedtext(text):
    """Checks if the arabic text is vocalized.
    The text can contain many words and spaces
    @param text: arabic unicode char
    @type text: unicode
    """
    if re.search(HARAKAT_pattern,text):
        return True;
    else:
        return False;
def isArabicstring(text):
    """ Checks for an  Arabic standard Unicode block characters;
    An arabic string can contain spaces, digits and pounctuation.
    but only arabic standard characters, not extended arabic
    @param text: input text
    @type text: unicode
    @return: True if all charaters are in Arabic block
    @rtype: Boolean
    """
    if re.search("([^\u0600-\u0652%s%s%s\s\d])"%(LAM_ALEF, LAM_ALEF_HAMZA_ABOVE,LAM_ALEF_MADDA_ABOVE),text):
        return False;
    return True;

def isArabicrange(text):
    """ Checks for an  Arabic Unicode block characters;
    @param text: input text
    @type text: unicode
    @return: True if all charaters are in Arabic block
    @rtype: Boolean
    """
    if re.search("([^\u0600-\u06ff\ufb50-\ufdff\ufe70-\ufeff\u0750-\u077f])",text):
        return False;
    return True;

def isArabicword(word):
    """ Checks for an valid Arabic  word.
    An Arabic word not contains spaces, digits and pounctuation
    avoid some spelling error,  TEH_MARBUTA must be at the end.
    @param word: input word
    @type word: unicode
    @return: True if all charaters are in Arabic block
    @rtype: Boolean
    """
    if len(word)==0 : return False;
    elif re.search("([^\u0600-\u0652%s%s%s])"%(LAM_ALEF, LAM_ALEF_HAMZA_ABOVE,LAM_ALEF_MADDA_ABOVE),word):
        return False;
    elif isHaraka(word[0]) or word[0] in (WAW_HAMZA,YEH_HAMZA):
        return False;
#  if Teh Marbuta or Alef_Maksura not in the end
    elif re.match("^(.)*[%s](.)+$"%ALEF_MAKSURA,word):
        return False;
    elif re.match("^(.)*[%s]([^%s%s%s])(.)+$"%(TEH_MARBUTA,DAMMA,KASRA,FATHA),word):
        return False;
    else:
        return True;

#####################################
#{Strip functions
#####################################
def stripHarakat(text):
    """Strip Harakat from arabic word except Shadda.
    The striped marks are :
    	- FATHA, DAMMA, KASRA
    	- SUKUN
    	- FATHATAN, DAMMATAN, KASRATAN, , , .
    Example:
    	>>> text="الْعَرَبِيّةُ"
    	>>> stripTashkeel(text)
    	العربيّة

    @param text: arabic text.
    @type text: unicode.
    @return: return a striped text.
    @rtype: unicode.
    """
    return  re.sub(HARAKAT_pattern,'',text)

def stripTashkeel(text):
    """Strip vowels from a text, include Shadda.
    The striped marks are :
    	- FATHA, DAMMA, KASRA
    	- SUKUN
    	- SHADDA
    	- FATHATAN, DAMMATAN, KASRATAN, , , .
    Example:
    	>>> text="الْعَرَبِيّةُ"
    	>>> stripTashkeel(text)
    	العربية

    @param text: arabic text.
    @type text: unicode.
    @return: return a striped text.
    @rtype: unicode.
    """
    return re.sub(TASHKEEL_pattern,'',text);

def stripTatweel(text):
    """
    Strip tatweel from a text and return a result text.

    Example:
    	>>> text="العـــــربية"
    	>>> stripTatweel(text)
    	العربية

    @param text: arabic text.
    @type text: unicode.
    @return: return a striped text.
    @rtype: unicode.
    """
    return re.sub(TATWEEL,'',text);

def normalizeLigature(text):
    """Normalize Lam Alef ligatures into two letters (LAM and ALEF), and Tand return a result text.
	Some systems present lamAlef ligature as a single letter, this function convert it into two letters,
	The converted letters into  LAM and ALEF are :
		- LAM_ALEF, LAM_ALEF_HAMZA_ABOVE, LAM_ALEF_HAMZA_BELOW, LAM_ALEF_MADDA_ABOVE

	Example:
		>>> text="لانها لالء الاسلام"
		>>> normalize_lamalef(text)
		لانها لالئ الاسلام

	@param text: arabic text.
	@type text: unicode.
	@return: return a converted text.
	@rtype: unicode.
	"""
    return LIGUATURES_pattern.sub('%s%s'%(LAM,ALEF), text)
#     #------------------------------------------------
def vocalizedlike( word, vocalized):
    """return True if the given word have the same or the partial vocalisation like the pattern vocalized

	@param word: arabic word, full/partial vocalized.
	@type word: unicode.
	@param vocalized: arabic full vocalized word.
	@type vocalized: unicode.
	@return: True if vocalized.
	@rtype: unicode.
    """
    if not isVocalized(vocalized) or not isVocalized(word):
        if isVocalized(vocalized):
            vocalized=stripTashkeel(vocalized);
        if isVocalized(word):
            word=stripTashkeel(word);
        if word==vocalized:
            return True;
        else:
            return False;
    else:
        for mark in TASHKEEL:
            vocalized=re.sub("[%s]"%mark,"[%s]?"%mark,vocalized)
        ocalized = "^"+vocalized+"$";
        pat=re.compile("^"+vocalized+"$");
        if pat.match("^"+vocalized+"$",word):
            return True;
        else: return False;

# a من هنا إلى آخر الوحدة من زيادة أحمد رغدي
# a قائمة بالمواضع التي يصلح فيها زيادة التطويل-----------------------

_l1 = ['ج','ـ','ح','خ','ه','ع','غ','ف','ق','ث','ص','ض',
      'ط','ك','م','ن','ت','ل','ب','ي','س','ش','ظ','ئ']
_l2 = ['ج','ح','خ','ه','ع','غ','ف','ق','ث','ص','ض','ط',
      'ك','م','ن','ت','ل','ب','ي','س','ش','ظ','ئ','د',
      'ز','و','ى','ا','ر','ؤ']
_ch = ['ّ','']
_ha = ['َ','ُ','ِ','ْ','']
tatwil_locations = list(itertools.product(_l1, _ch, _ha, _l2))

# a الحروف المستبدلة في البحث --------------------------------------------

normalize_tb={
65: 97, 66: 98, 67: 99, 68: 100, 69: 101, 70: 102, 71: 103, 72: 104, 73: 105, 
74: 106, 75: 107, 76: 108, 77: 109, 78: 110, 79: 111, 80: 112, 81: 113, 82: 114, 
83: 115, 84: 116, 85: 117, 86: 118, 87: 119, 88: 120, 89: 121, 90: 122,
1600: None, 1569: 1575, 1570: 1575, 1571: 1575, 1572: 1575, 1573: 1575, 1574: 1575,
1577: 1607, # teh marboota ->  haa
1611: None, 1612: None, 1613: None, 1614: None, 1615: None, 1616: None, 1617: None, 1618: None, 1609: 1575}
__sq_re=re.compile('[\s"]')

def fuzzy(word):
    return str(word).translate(normalize_tb)

def fuzzy_plus(word):
    word = str(word).translate(normalize_tb)
    word = re.sub('\n+', ' ', word)
    word = word.strip()
    word = word.replace('*', '')
    word = re.sub(' +', ' ', word)
    return word

def tokenize_search(s):
    '''Take a string and return a list of non-empty tokens, double quotes are group tokens,
    and double double quotes are escaped
    s='abc def' -> ['acb', 'def']
    s='abc def "Hello, world!"' -> ['acb', 'def','Hello, world!']
    s='abc"def"ghi' -> ['acb', 'def', 'ghi']

    s='abc def "He said: ""Hello, world!"""' -> ['abc', 'def', 'He said: "Hello, world!"']
    '''
    global __sq_re
    skip,last,t=0,0,1
    l=[]
    for m in __sq_re.finditer(s):
        s1=s[last:m.start()].replace('""','"')
        if s[m.start()]=='"':
            if skip: skip=0; continue
            elif s[m.start():m.start()+2]=='""': skip=1; continue
            elif t==1: t=-1; l.append(s1); last=m.end(); continue
            else: t=1; l.append(s1); last=m.end(); continue
        elif t==-1: continue
        else: t=1; l.append(s1); last=m.end(); continue
    if len(s[last:])>0: l.append(s[last:])
    return filter(lambda a: len(a)>0, l)

def tashkil(s):
    t = []
    for a in range(len(s)):
        for a1 in range(len(s[a])):
            for a2 in s[a][a1]:
                for a3 in ['ّ','']:
                    for a4 in ['َ','ُ','ِ','ْ','']:
                        for a5 in ['ً','ٌ','ٍ','']:
                            t.append([a2+a3+a4])
    return t

# a فك المضعف-----------------------------------------------------------------
#a مدّ = مدد

def take_apart_tense(text):
    text = re.sub(FATHA+SHADDA, SHADDA+FATHA, text)
    text = re.sub(DAMMA+SHADDA, SHADDA+DAMMA, text)
    text = re.sub(KASRA+SHADDA, SHADDA+KASRA, text)
    text = re.sub(FATHATAN+SHADDA, SHADDA+FATHATAN, text)
    text = re.sub(DAMMATAN+SHADDA, SHADDA+DAMMATAN, text)
    text = re.sub(KASRATAN+SHADDA, SHADDA+KASRATAN, text)
    txt = ''
    for a in range(len(text)):
        if SHADDA == text[a]:
            txt += SUKUN
            txt += text[a-1]
        else:
            txt += text[a]
    return txt

def del_tense(text):
    text1 = take_apart_tense(text)
    text1 = stripTashkeel(text1)
    text2 = stripTashkeel(text)
    return text1, text2

#a--------------------------------------------------------------------------------
I3lal_pattern =re.compile(r"["+"".join(HAMZAT)+"".join(WEAK)+"]")

def i3lal(text):
    t1 = re.sub(I3lal_pattern, ALEF, text, 1)
    t1 = re.sub(ALEF_MAKSURA, YEH, t1, 1)
    t2 = re.sub(I3lal_pattern, YEH, text, 1)
    t2 = re.sub(ALEF_MAKSURA, YEH, t2, 1)
    t3 = re.sub(I3lal_pattern, WAW, text, 1)
    t3 = re.sub(ALEF_MAKSURA, YEH, t3, 1)
    t4 = re.sub(I3lal_pattern, ALEF_HAMZA_ABOVE, text, 1)
    t4 = re.sub(ALEF_MAKSURA, YEH, t4, 1)
    ls =[t1,]
    if t2 not in ls: ls.append(t2)
    if t3 not in ls: ls.append(t3)
    if t4 not in ls: ls.append(t4)
    
    return ls

def normalize (text):
    text = HARAKAT_pattern.sub('', text)
    text = re.sub(r'[%s]' % TATWEEL,    '', text)
    text = LIGUATURES_pattern.sub('%s%s'%(LAM,ALEF), text)
    text = ALEFAT_pattern.sub(ALEF, text)
    text = HAMZAT_pattern.sub(HAMZA, text)
    text = re.sub(r'[%s]' % TEH_MARBUTA,    HEH, text)
    text = re.sub(r'[%s]' % ALEF_MAKSURA,    YEH, text)
    return text;


if list('حمد') in list('حَمِداتن'):
    print (list('حَمِداتن'))
else: print (list('حَمِداتن'))