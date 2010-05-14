from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from Products.Five import BrowserView
from zope.interface import Interface, implements
import logging


class Sorter(BrowserView):
    """Sort objects inside an ordered folder based on new ids"""

    def __call__(self):
        new = self.request.form.get('order')
        old = self.context.objectIds()

        for i, id in enumerate(new):
            old_i = old.index(id)
            if old_i != i:
                self.context.moveObjectToPosition(id, i)
                #logging.info("Moved %s from position %s to %s", id, old_i, i)

        return "<done />"


class IIndicatorUtils(Interface):
    #str_to_id = Attribute(u"String to Id conversion")

    def str_to_id():
        """Convert an ordinary string (maybe title) to something that can be used as a DOM element ID"""

    def field_has_value(fieldname, context):
        """Return True if the given field has a value for the given context object"""


class IndicatorUtils(BrowserView):
    """Various utils for Indicators"""

    implements(IIndicatorUtils)

    def str_to_id(self, s, context):
        s = normalizeString(s, context=context)
        return s.replace(".", "_")

    def field_has_value(self, fieldname, context):
        """This is a dumb implementation that assumes only richtext for now"""
        convert = getToolByName(self.context, 'portal_transforms').convert
        value = context.schema[fieldname].getAccessor(context)()
        return convert('html_to_text', value).getData()


class ObjectDelete(BrowserView):
    """Delete objects from this container"""

    def __call__(self):
        id = self.request.form['id']
        del self.context[id]
        return "<done />"


class RelatedItems(BrowserView):
    """ Return filtered related items
    """

    def __call__(self, ctype=None):
        if ctype == None:
            return self.context.getRelatedItems()
        if type(ctype) not in (list, tuple):
            ctype = [ctype]

        return [rel for rel in self.context.getRelatedItems()
                    if rel.portal_type in ctype]


    def get_uids(self, ctype=None):
        if ctype == None:
            return self.context.getRawRelatedItems()

        if type(ctype) not in (list, tuple):
            ctype = [ctype]

        return [rel.UID() for rel in self.context.getRelatedItems() 
                if rel.portal_type in ctype]

