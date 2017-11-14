# -*- coding: utf-8 -*-
#
# $Id$
#

""" ExternalDataSpec content type
"""

import logging
from AccessControl import ClassSecurityInfo

from zope.interface import implements
from zope.component import adapts
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.base import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from Products.Archetypes.atapi import RichWidget, SelectionWidget
from Products.Archetypes.atapi import StringField, Schema, TextField
from Products.Archetypes.utils import shasattr
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFPlone.utils import getToolByName
from Products.EEAContentTypes.content.ThemeTaggable import ThemeTaggable_schema
from Products.EEAContentTypes.subtypes import ThemesSchemaExtender, \
    ExtensionThemesField
from Products.LinguaPlone.public import InAndOutWidget
from archetypes.schemaextender.interfaces import ISchemaExtender, ISchemaModifier
from eea.dataservice.widgets import OrganisationsWidget
from eea.indicators.content import interfaces
from eea.themecentre.interfaces import IThemeTagging

logger = logging.getLogger('eea.indicators.content.ExternalDataSpec')

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label="Dataset name",
            label_msgid='indicators_label_title',
            i18n_domain='indicators',
            description=" ",
        ),
        required=True,
        accessor="Title",
        searchable=True,
    ),
    StringField(
        name='provider_name',
        widget=StringField._properties['widget'](
            visible={'view':'hidden', 'edit':'hidden'},
            label="Dataset provider name",
            label_msgid='indicators_label_provider_name',
            i18n_domain='indicators',
            description=" ",
        ),
        required=False,
        searchable=True,
    ),
    StringField(
        name='provider_url',
        widget=OrganisationsWidget(
            label="Dataset provider/owner",
            description="Organisation providing access to this dataset.",
            label_msgid='indicators_label_provider_url',
            i18n_domain='indicators',
        ),
        required=True,
        required_for_published="True",
        vocabulary_factory=u'Organisations',
    ),
    StringField(
        name='dataset_url',
        widget=StringField._properties['widget'](
            label="Dataset URL",
            description="Specific URL where this dataset can be found",
            label_msgid='indicators_label_dataset_url',
            i18n_domain='indicators',
        ),
        required=True,
        searchable=True,
        required_for_published="True",
    ),
    TextField(
        name='dataset_path',
        allowable_content_types=('text/plain', 'text/structured',
            'text/html', 'application/msword',),
        widget=RichWidget(
            label="Dataset path",
            description="Further information and details needed to "
                        "get the dataset.",
            label_msgid='indicators_label_dataset_path',
            i18n_domain='indicators',
        ),
        required=False,
        default_content_type="text/html",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='timeliness',
        allowable_content_types=('text/plain', 'text/structured',
            'text/html', 'application/msword',),
        widget=RichWidget(
            label="Timeliness",
            visible={'view':'hidden', 'edit':'hidden'},
            label_msgid='indicators_label_timeliness',
            i18n_domain='indicators',
            description=" ",
        ),
        required=False,
        default_content_type="text/html",
        searchable=True,
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='other_comments',
        allowable_content_types=('text/plain', 'text/structured',
            'text/html', 'application/msword',),
        widget=RichWidget(
            label="Other Comments",
            label_msgid='indicators_label_other_comments',
            i18n_domain='indicators',
            description=" ",
        ),
        required=False,
        default_content_type="text/html",
        searchable=True,
        default_output_type="text/x-html-safe",
    ),
    StringField(
        name='category_of_use',
        widget=SelectionWidget(
            label="Category of use",
            visible={'view':'hidden', 'edit':'hidden'},
            label_msgid='indicators_label_category_of_use',
            i18n_domain='indicators',
            description=" ",
        ),
        required=False,
        vocabulary=NamedVocabulary("indicator_category_of_use"),
    ),
    TextField(
        name='description',
        widget=RichWidget(
            label="Description",
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
            description=" ",
        ),
        default_content_type="text/html",
        searchable=True,
        required=False,
        allowable_content_types=('text/plain', 'text/structured',
            'text/html', 'application/msword',),
        default_output_type="text/x-html-safe",
        accessor="getDescription",
    ),

),
)

schema['provider_url'].validators = ('isURL',)
schema['dataset_url'].validators = ('isURL',)
schema = schema + ThemeTaggable_schema.copy()
schema['themes'].visible = {'view':'hidden', 'edit':'hidden'}

ExternalDataSpec_schema = ATContentTypeSchema.copy() + \
    getattr(ATCTContent, 'schema', Schema(())).copy() + \
    schema.copy()

ExternalDataSpec_schema.moveField('relatedItems', after='category_of_use')
finalizeATCTSchema(ExternalDataSpec_schema)

class ExternalDataSpec(ATCTContent, BrowserDefaultMixin):
    """ External data spec
    """
    security = ClassSecurityInfo()

    implements(interfaces.IExternalDataSpec)

    meta_type = 'ExternalDataSpec'
    _at_rename_after_creation = True

    schema = ExternalDataSpec_schema

    security.declarePublic("Description")
    def Description(self):
        """ Get description
        """
        convert = getToolByName(self, 'portal_transforms').convert
        text = convert('html_to_text', self.getDescription()).getData()
        try:
            text = text.decode('utf-8', 'replace')
        except UnicodeDecodeError, err:
            logger.info(err)
        return text

    security.declarePublic("getThemes")
    def getThemes(self):
        """ Get themes
        """
        themes = []
        for ref in self.getBRefs():
            if not shasattr(ref, 'getThemes'):
                continue
            themes.extend(ref.getThemes())
        return sorted(list(set(themes)))

    security.declarePublic('Subject')
    def Subject(self):
        """ Overwrite standard Subject method to dynamically get all
            keywords from other specifications
        """
        result = []
        for ref in self.getBRefs():
            if not ref or ref.portal_type != "Specification":
                continue
            result.extend(ref.Subject())
        return sorted(list(set(result)))

    def getOrganisationByUrl(self, url):
        """ get Organisation by given url
        """
        cat = getToolByName(self, 'portal_catalog')
        brains = cat.searchResults({
            'portal_type' : 'Organisation',
            'getUrl': url
        })
        if brains:
            return brains[0]

    security.declarePublic('getDataOwner')
    def getDataOwner(self):
        """ Return provider_url to be indexed under getDataOwner index
            Used under Organisations view
        """
        return self.getProvider_url()


class ExternalDataSpecThemes(object):
    """ ExternalDataSpec themes
    """

    implements(IThemeTagging)
    adapts(interfaces.IExternalDataSpec)

    def __init__(self, context):
        self.context = context


    def _get_tags(self):
        """ Return tags
        """
        return self.context.getThemes()

    def _set_tags(self, value):
        """ Tags is read-only
        """
        return

    tags = property(_get_tags, _set_tags)


class ExternalDataSpecThemesExtender(ThemesSchemaExtender):
    """ ExternalDataSpec themes adapter Refs #89852
    """
    implements(ISchemaExtender)

    fields = (
        ExtensionThemesField(
            name='themes',
            schemata='categorization',
            validators=('maxValues',),
            required=False,
            widget=InAndOutWidget(
                maxValues=0,
                label="Themes",
                description=u"Topics are inherited from the related objects "
                            u"using this as data source. If you want to change "
                            u"topics you need to change the topics on the "
                            u"related objects.",
                required=False,
            ),
            languageIndependent=True,
            vocabulary_factory=u"Allowed themes for edit",
            default=[],
        ),
    )


class ExternalDataSpecThemesSchemaModifier(object):
    """ ExternalDataSpec schema modifier for the themes field in order to make
    it not required Refs #89852
    """
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, dataspec_schema):
        # first i make a copy of the themes field otherwise the changes
        # will apply for all content types
        dataspec_schema['themes'] = dataspec_schema['themes'].copy()

        # set required_for_published and required to False
        dataspec_schema['themes'].required_for_published = False
        dataspec_schema['themes'].required = False