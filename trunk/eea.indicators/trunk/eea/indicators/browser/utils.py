from Products.CMFPlone.utils import normalizeString
from Products.Five import BrowserView
from eea.workflow.interfaces import IValueProvider
from zope.component import getMultiAdapter
from zope.interface import Interface, implements
from Products.CMFCore.utils import getToolByName
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
#import logging


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
        """Convert an ordinary string (maybe title) to something that
           can be used as a DOM element ID
        """

    def field_has_value(fieldname, context):
        """Return True if the given field has a value
           for the given context object
        """


class IndicatorUtils(BrowserView):
    """Various utils for Indicators"""

    implements(IIndicatorUtils)

    def str_to_id(self, s, context):
        s = normalizeString(s, context=context)
        return s.replace(".", "_")

    def field_has_value(self, fieldname, context):
        """This is a dumb implementation that assumes only richtext for now"""

        field = context.schema[fieldname]
        vp = getMultiAdapter((context, field), IValueProvider)
        return vp.has_value()


class ObjectDelete(BrowserView):
    """Delete objects from this container"""

    def __call__(self):
        id = self.request.form['id']
        del self.context[id]
        return "<done />"


class RelatedItems(BrowserView):
    """ Return filtered related items
    """

    def __call__(self, ctype=None, state=None):
        if ctype == None:
            return self.context.getRelatedItems()
        if type(ctype) not in (list, tuple):
            ctype = [ctype]

        res = [rel for rel in self.context.getRelatedItems()
                    if rel.portal_type in ctype]

        if state:
            wf_tool = getToolByName(self, 'portal_workflow')
            return [rel for rel in res
                         if wf_tool.getInfoFor(rel, 'review_state') in state]
        return res

    def get_uids(self, ctype=None):
        if ctype == None:
            return self.context.getRawRelatedItems()

        if type(ctype) not in (list, tuple):
            ctype = [ctype]

        return [rel.UID() for rel in self.context.getRelatedItems()
                if rel.portal_type in ctype]


class DpsirLabel(BrowserView):
    """ Return value from DPSIR vocabulary based on key
    """

    def __call__(self, value=None):
        atvm = getToolByName(self, ATVOCABULARYTOOL)
        vocab = getattr(atvm, 'indicator_dpsir')
        value = vocab.get(value)
        if value:
            return value.Title()
        else:
            return ""


class TypologyLabel(BrowserView):
    """ Return value from Typology vocabulary based on key
    """

    def __call__(self, value=None):
        atvm = getToolByName(self, ATVOCABULARYTOOL)
        vocab = getattr(atvm, 'indicator_typology')
        value = vocab.get(value)
        if value:
            return value.Title()
        else:
            return ""


class CategoryLabel(BrowserView):
    """ Return value from Category of use vocabulary based on key
    """

    def __call__(self, value=None):
        atvm = getToolByName(self, ATVOCABULARYTOOL)
        vocab = getattr(atvm, 'indicator_category_of_use')
        value = vocab.get(value)
        if value:
            return value.Title()
        else:
            return ""


def has_one_of(has, in_list):
    for obj in in_list:
        if obj.meta_type in has:
            return True
    return False

