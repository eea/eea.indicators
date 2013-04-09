"""Browser utilities
"""

from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.CatalogTool import sortable_title
from Products.CMFPlone.utils import normalizeString
from Products.Five import BrowserView
from eea.indicators.browser.interfaces import IIndicatorUtils
from eea.workflow.interfaces import IValueProvider
from zope.component import getMultiAdapter
from zope.interface import implements


class Sorter(BrowserView):
    """Sort objects inside an ordered folder based on new ids"""

    def __call__(self):
        new = self.request.form.get('order')
        old = self.context.objectIds()

        for i, sid in enumerate(new):
            old_i = old.index(sid)
            if old_i != i:
                self.context.moveObjectToPosition(sid, i)
                #logging.info("Moved %s from position %s to %s", id, old_i, i)

        return "<done />"

class IndicatorUtils(BrowserView):
    """Various utils for Indicators"""

    implements(IIndicatorUtils)

    def str_to_id(self, s, context):
        """make an id from a string"""
        s = normalizeString(s, context=context)
        return s.replace(".", "_")

    def field_has_value(self, fieldname, context):
        """This is a dumb implementation that assumes only richtext for now"""

        field = context.schema[fieldname]
        vp = getMultiAdapter((context, field), IValueProvider)
        return vp.has_value()

    def field_value_info(self, fieldname, context):
        field = context.schema[fieldname]
        vp = getMultiAdapter((context, field), IValueProvider)
        return vp.value_info()


class ObjectDelete(BrowserView):
    """Delete objects from this container"""

    def __call__(self):
        oid = self.request.form['id']
        del self.context[oid]
        return "<done />"


class RelatedItems(BrowserView):
    """ Return filtered related items """

    def _get_items(self, ctype, state=None, sort=False):
        """get filtered items """

        if ctype == None:
            res = self.context.getRelatedItems()
            if sort:
                return sorted(res, key=lambda obj: sortable_title(obj)())
            return res

        if type(ctype) not in (list, tuple):
            ctype = [ctype]

        items = [rel for rel in self.context.getRelatedItems()
                    if rel.portal_type in ctype]

        if state:
            wf_tool = getToolByName(self.context, 'portal_workflow')
            items = [rell for rell in items
                      if wf_tool.getInfoFor(rell, 'review_state') in state]
        if sort:
            return sorted(items, key=lambda obj: sortable_title(obj)())

        return items

    def __call__(self, ctype=None, state=None, sort=False):
        return self._get_items(ctype, state, sort)

    def get_uids(self, ctype=None):
        """ returns uids """

        return [rel.UID() for rel in self._get_items(ctype)]


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
    """Returns if there at least one object of type 'has' in the list 'list'"""
    in_list = in_list or []
    for obj in in_list:
        if obj.meta_type in has:
            return True
    return False

