from types import UnicodeType, StringType
from reportlab.lib.formatters import DecimalFormatter
from xml.sax.saxutils import escape
from rlextra.radxml.html_cleaner import cleanBlocks, cleanInline
from rlextra.radxml.xhtml2rml import xhtml2rml

commaFormatter = DecimalFormatter(places=0,thousandSep=',')
percentFormatter = DecimalFormatter(places=2,thousandSep='', suffix="%")

def rml(stuff, default="inline"):
    if stuff is None:
        return "-"
    else:
        if default=="inline":
            cleaned = cleanInline(stuff)
        else:
            cleaned = cleanBlocks(stuff)
        rml = xhtml2rml(cleaned, paraStyle='body')
        return rml

def esc(stuff):
    if type(stuff) is UnicodeType:
        txt = stuff.encode('utf8')
    elif type(stuff) is StringType:
        txt = stuff
    else:
        txt = str(stuff)
    return escape(txt)

def negRedTd(v,posColor=None,negColor="red", format='comma'):
    if format == 'comma':
        formatter = commaFormatter
    else:
        formatter = percentFormatter
    fca = (' fontColor="%s"' % negColor) if not v > -1e-6 else (' fontColor="%s"' % posColor) if posColor else ''
    return '<td%s>%s</td>' %(fca,formatter(v))
