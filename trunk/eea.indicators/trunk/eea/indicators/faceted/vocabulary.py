"""Vocabularies used in custom eea.facetednavigation extensions"""

from zope.interface import alsoProvides
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

def sorting_options_vocabulary(context):
    return SimpleVocabulary([
        SimpleTerm("effective", "effective", "Publish date"),
        SimpleTerm("get_codes", "get_codes", "Indicator code")
        ])

alsoProvides(sorting_options_vocabulary, IVocabularyFactory)
