"""Browser utilities
"""

from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.CatalogTool import sortable_title
from Products.CMFPlone.utils import normalizeString
from Products.CompoundField.CompoundField import CompoundField
from Products.Five import BrowserView
from eea.indicators.browser.interfaces import IIndicatorUtils
from eea.versions.versions import VersionControl
from eea.workflow.interfaces import IValueProvider
from eea.workflow.utils import ATFieldValueProvider
from zope.component import getMultiAdapter, queryMultiAdapter, adapts
from zope.interface import implements, Interface
import logging

logger = logging.getLogger('eea.indicators')


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

    def adapter(self, context, fieldname):
        """get the proper IValueProvider adapter
        """
        field = context.schema[fieldname]

        vp = queryMultiAdapter((context, field), IValueProvider, 
                                name=fieldname)
        if vp is None:
            vp = getMultiAdapter((context, field), IValueProvider)
        return vp

    def str_to_id(self, s, context):
        """make an id from a string"""
        s = normalizeString(s, context=context)
        return s.replace(".", "_")

    def field_has_value(self, fieldname, context):
        """ field has value"""
        return self.adapter(context, fieldname).has_value()

    def field_value_info(self, fieldname, context):
        """complete info about the field's value
        """
        return self.adapter(context, fieldname).value_info()


class FrequencyOfUpdatesFieldValueProvider(ATFieldValueProvider):
    """An IValueProvider implementation for Text Fields"""

    adapts(Interface, CompoundField)

    def has_value(self, **kwargs):
        """ Returns true if text field has at least 2 words in it
        """

        accessor = self.field.getAccessor(self.context)
        if not accessor:
            msg = "Field %s for %s has no accessor" % (self.field, 
                                                       self.context)
            logger.warning(msg)
            return False
        value = accessor()

        #all field except ending_date are optional

        fields = ['frequency', 'starting_date']
        for f in fields:
            if not value[f]:
                return False

        for line in value['frequency']:
            if (not line['years_freq']) and (not line['time_of_year']):
                continue
            if not (line['time_of_year'] in ['Q1', 'Q2', 'Q3', 'Q4']):
                return False
            if line['time_of_year'] and not line['years_freq']:
                return False

        return True

    def value_info(self, **kwargs):
        """ Get value info
        """
        return {
            'raw_value':self.field.getAccessor(self.context)(),
            'value':self.field.getAccessor(self.context)(),
            'has_value':self.has_value(**kwargs),
            'msg':('Information about frequency of update for this '
                   'indicator is missing.') #needs i18n
        }


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


class IMSVersionControl(VersionControl):
    """Override for IVersionControl.can_version
    """

    def can_version(self):
        """custom behaviour
        """
        #relies on acquisition
        discontinued = self.context.is_discontinued()
        return not discontinued
