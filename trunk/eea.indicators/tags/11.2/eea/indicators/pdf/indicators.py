""" PDF View
"""
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.pdf.themes.book.collection import Body as CollectionPDFBody
from eea.pdf.themes.book.folder import Body as FolderPDFBody

class FolderBody(FolderPDFBody):
    """ Custom PDF body
    """
    template = ViewPageTemplateFile("indicators.body.pt")


class CollectionBody(CollectionPDFBody):
    """ Custom PDF body
    """
    template = ViewPageTemplateFile("indicators.body.pt")
