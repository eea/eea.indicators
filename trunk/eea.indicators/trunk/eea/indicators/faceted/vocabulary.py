"""Vocabularies used in custom eea.facetednavigation extensions"""

from zope.interface import alsoProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

def sorting_options_vocabulary(context):
    """ vocab """
    return SimpleVocabulary([
        SimpleTerm("effective", "effective", "Publish date"),
        SimpleTerm("get_codes", "get_codes", "Indicator code")
        ])

alsoProvides(sorting_options_vocabulary, IVocabularyFactory)
