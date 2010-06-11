# -*- coding: utf-8 -*-
#
# $Id$
#
# Copyright (c) 2010 by ['Tiberiu Ichim']
# Generator: ArchGenXML Version 2.4.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Tiberiu Ichim <unknown>"""
__docformat__ = 'plaintext'


import logging
logger = logging.getLogger('indicators: setuphandlers')
from eea.indicators.config import PROJECTNAME
from eea.indicators.config import DEPENDENCIES
import os
from Products.CMFCore.utils import getToolByName
import transaction
##code-section HEAD
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from eea.indicators.config import (
    CODES,
    DPSIR,
    TYPOLOGY,
    CATEGORY_OF_USE,
    PROFILE_DEPENDENCIES
)
##/code-section HEAD

def isNotindicatorsProfile(context):
    return context.readDataFile("indicators_marker.txt") is None

def installQIDependencies(context):
    """This is for old-style products using QuickInstaller"""
    if isNotindicatorsProfile(context): return
    logger.info("installQIDependencies starting")
    site = context.getSite()
    qi = getToolByName(site, 'portal_quickinstaller')

    for dependency in DEPENDENCIES:
        if qi.isProductInstalled(dependency):
            logger.info("   re-Installing QI dependency %s:" % dependency)
            qi.reinstallProducts([dependency])
            transaction.savepoint() # is a savepoint really needed here?
            logger.debug("   re-Installed QI dependency %s:" % dependency)
        else:
            if qi.isProductInstallable(dependency):
                logger.info("   installing QI dependency %s:" % dependency)
                qi.installProduct(dependency)
                transaction.savepoint() # is a savepoint really needed here?
                logger.debug("   installed dependency %s:" % dependency)
            else:
                logger.info("   QI dependency %s not installable" % dependency)
                raise "   QI dependency %s not installable" % dependency
    logger.info("installQIDependencies finished")



def updateRoleMappings(context):
    """after workflow changed update the roles mapping. this is like pressing
    the button 'Update Security Setting' and portal_workflow"""
    if isNotindicatorsProfile(context): return
    wft = getToolByName(context.getSite(), 'portal_workflow')
    wft.updateRoleMappings()

def postInstall(context):
    """Called as at the end of the setup process. """
    # the right place for your custom code
    if isNotindicatorsProfile(context): return
    site = context.getSite()

    #install dependencies available as GS profiles

    qtool = getToolByName(site, 'portal_quickinstaller')
    installed = [package['id'] for package in qtool.listInstalledProducts()]
    for name, importcontext, install in PROFILE_DEPENDENCIES:
        if install:
            if name not in installed:
                qtool.installProduct(name)
                logger.info("Installed dependency %s" % name)
            else:
                logger.info("Skip %s, already installed" % name)
        else:
            setuptool = getToolByName(site, 'portal_setup')
            setuptool.setImportContext(importcontext)
            setuptool.runAllImportSteps()
            logger.info("Run all import steps for %s" % name)

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
    """Setup ATVocabularyManager vocabularies"""

    site = context.getSite()
    atvm = getToolByName(site, ATVOCABULARYTOOL, None)
    if atvm is None:
        raise ValueError("Could not find the ATVocabularyManager")

    # Vocabulary of indicator sets
    vkey = 'indicator_codes'
    if not hasattr(atvm, vkey):
        atvm.invokeFactory('SimpleVocabulary', vkey)
        vocab = atvm[vkey]
        for val in CODES:
            vocab.invokeFactory('SimpleVocabularyTerm', val)
            vocab[key].setTitle(val)

    # Vocabulary of indicator DPSIR
    vkey = 'indicator_dpsir'
    if not hasattr(atvm, vkey):
        atvm.invokeFactory('SimpleVocabulary', vkey)
        vocab = atvm[vkey]
        for val in DPSIR:
            vocab.invokeFactory('SimpleVocabularyTerm', val[0])
            vocab[key].setTitle(val[1])

    # Vocabulary of indicator typology
    vkey = 'indicator_typology'
    if not hasattr(atvm, vkey):
        atvm.invokeFactory('SimpleVocabulary', vkey)
        vocab = atvm[vkey]
        for val in TYPOLOGY:
            vocab.invokeFactory('SimpleVocabularyTerm', val[0])
            vocab[key].setTitle(val[1])

    # Vocabulary of indicator category of use
    vkey = 'indicator_category_of_use'
    if not hasattr(atvm, vkey):
        atvm.invokeFactory('SimpleVocabulary', vkey)
        vocab = atvm[vkey]
        for val in CATEGORY_OF_USE:
            vocab.invokeFactory('SimpleVocabularyTerm', val[0])
            vocab[key].setTitle(val[1])

def setup_misc(context):
    """ Stub step to enable setting dependent steps """

    return

def updateRoleMappings(context):
    """We don't need this actually, so we rewrite it"""
    return

##/code-section FOOT
