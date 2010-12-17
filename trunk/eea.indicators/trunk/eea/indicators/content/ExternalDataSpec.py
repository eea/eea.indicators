# -*- coding: utf-8 -*-
#
# $Id$
#

""" ExternalDataSpec content type
"""

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.base import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from Products.Archetypes.atapi import RichWidget, registerType, SelectionWidget
from Products.Archetypes.atapi import StringField, Schema, TextField
from Products.Archetypes.utils import shasattr
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.CMFPlone.utils import getToolByName
from eea.dataservice.vocabulary import Organisations
from eea.indicators.config import PROJECTNAME
from eea.indicators.content import interfaces
from eea.themecentre.interfaces import IThemeTagging
from zope.component import adapts
from zope.interface import implements


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
            visible={'view':'visible', 'edit':'visible'},
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
        widget=SelectionWidget(
            label="Dataset provider/owner",
            description="Organisation providing access to this dataset.",
            macro="organisation_widget",
            helper_js=("selectautocomplete_widget.js", ),
            label_msgid='indicators_label_provider_url',
            i18n_domain='indicators',
        ),
        required=True,
        required_for_published="True",
        vocabulary=Organisations(),
    ),
    StringField(
        name='dataset_url',
        widget=StringField._properties['widget'](
            label="URL where this dataset can be found",
            label_msgid='indicators_label_dataset_url',
            i18n_domain='indicators',
            description=" ",
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
        required=True,
        default_content_type="text/html",
        default_output_type="text/x-html-safe",
    ),
    TextField(
        name='timeliness',
        allowable_content_types=('text/plain', 'text/structured', 
            'text/html', 'application/msword',),
        widget=RichWidget(
            label="Timeliness",
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
            label="Entities description",
            label_msgid='indicators_label_description',
            i18n_domain='indicators',
            description=" ",
        ),
        default_content_type="text/html",
        searchable=True,
        required=True,
        required_for_published="True",
        allowable_content_types=('text/plain', 'text/structured', 
            'text/html', 'application/msword',),
        default_output_type="text/x-html-safe",
        accessor="getDescription",
    ),

),
)

schema['provider_url'].validators = ('isURL',)
schema['dataset_url'].validators = ('isURL',)

ExternalDataSpec_schema = ATContentTypeSchema.copy() + \
    getattr(ATCTContent, 'schema', Schema(())).copy() + \
    schema.copy()

ExternalDataSpec_schema.moveField('relatedItems', after='category_of_use')
finalizeATCTSchema(ExternalDataSpec_schema)

class ExternalDataSpec(ATCTContent, BrowserDefaultMixin):
    """External data spec
    """
    security = ClassSecurityInfo()

    implements(interfaces.IExternalDataSpec)

    meta_type = 'ExternalDataSpec'
    _at_rename_after_creation = True

    schema = ExternalDataSpec_schema

    security.declarePublic("Description")
    def Description(self):
        """description"""
        convert = getToolByName(self, 'portal_transforms').convert
        return convert('html_to_text', self.getDescription()).getData()

    security.declarePublic("getThemes")
    def getThemes(self):
        """Get themes"""
        themes = []
        map(
            lambda o:themes.extend(o.getThemes()), 
            filter(
                lambda o:shasattr(o, 'getThemes'), 
                self.getBRefs()
            )
        )
        return sorted(list(set(themes)))

    security.declarePublic('Subject')
    def Subject(self):
        """Overwrite standard Subject method to dynamically get all
           keywords from other specifications"""
        result = []
        map(
            lambda o:result.extend(o.Subject()), 
            filter(
                lambda o:o.portal_type=="Specification", 
                self.getBRefs()
            )
        )
        return sorted(list(set(result)))
        

registerType(ExternalDataSpec, PROJECTNAME)


class ExternalDataSpecThemes(object):
    """ExternalDataSpec themes"""

    implements(IThemeTagging)
    adapts(interfaces.IExternalDataSpec)

    def __init__(self, context):
        self.context = context

    @property
    def tags(self):
        """return tags"""
        return self.context.getThemes()
