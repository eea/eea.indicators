"""Custom import steps for eea.indicators"""

from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.CMFCore.utils import getToolByName
from eea.indicators.config import DEPENDENCIES
import logging
import transaction
from eea.indicators.config import (
    CODES,
    DPSIR,
    TYPOLOGY,
    CATEGORY_OF_USE,
    PROFILE_DEPENDENCIES
)

logger = logging.getLogger('indicators: setuphandlers')

def isNotindicatorsProfile(context):
    """ Used by GS """
    return context.readDataFile("eea.indicators.txt") is None

def postInstall(context):
    """ Called as at the end of the setup process. """

    # the right place for your custom code
    if isNotindicatorsProfile(context):
        return
    site = context.getSite()

    # Enable aliases (redirects) for eea.indicators content types
    redirection_tool = getToolByName(site, 'portal_redirection')
    ctypes = ["PolicyDocumentReference",
              "ExternalDataSpec",
              "Specification",
              "IndicatorFactSheet"]
    new_ctypes = redirection_tool.getRedirectionAllowedForTypes()
    new_ctypes.extend(ctypes)
    redirection_tool.setRedirectionAllowedForTypes(new_ctypes)
    logger.info("Redirection tool enabled for eea.indicators content types.")

##code-section FOOT
def setup_vocabularies(context):
    """ Setup ATVocabularyManager vocabularies. """

    site = context.getSite()
    atvm = getToolByName(site, ATVOCABULARYTOOL, None)
    if atvm is None:
        raise ValueError("Could not find the ATVocabularyManager")

    # Vocabulary of indicator sets
    vkey = 'indicator_codes'
    if not hasattr(atvm, vkey):
        logger.info("adding Vocabulary of indicator sets")
        atvm.invokeFactory('SimpleVocabulary', vkey)
        vocab = atvm[vkey]
        for val in CODES:
            vocab.invokeFactory('SimpleVocabularyTerm', val)
            vocab[val].setTitle(val)

    # Vocabulary of indicator DPSIR
    vkey = 'indicator_dpsir'
    if not hasattr(atvm, vkey):
        logger.info("adding Vocabulary of indicator DPSIR")
        atvm.invokeFactory('SimpleVocabulary', vkey)
        vocab = atvm[vkey]
        for val in DPSIR:
            vocab.invokeFactory('SimpleVocabularyTerm', val[0])
            vocab[val[0]].setTitle(val[1])

    # Vocabulary of indicator typology
    vkey = 'indicator_typology'
    if not hasattr(atvm, vkey):
        logger.info("adding Vocabulary of indicator typology")
        atvm.invokeFactory('SimpleVocabulary', vkey)
        vocab = atvm[vkey]
        for val in TYPOLOGY:
            vocab.invokeFactory('SimpleVocabularyTerm', val[0])
            vocab[val[0]].setTitle(val[1])

    # Vocabulary of indicator category of use
    vkey = 'indicator_category_of_use'
    if not hasattr(atvm, vkey):
        logger.info("adding Vocabulary of indicator category of use")
        atvm.invokeFactory('SimpleVocabulary', vkey)
        vocab = atvm[vkey]
        for val in CATEGORY_OF_USE:
            vocab.invokeFactory('SimpleVocabularyTerm', val[0])
            vocab[val[0]].setTitle(val[1])
