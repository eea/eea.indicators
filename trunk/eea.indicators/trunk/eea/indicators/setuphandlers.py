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
from eea.indicators.config import CODES, PROFILE_DEPENDENCIES
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

    setuptool = getToolByName(site, 'portal_setup')
    for name, importcontext in PROFILE_DEPENDENCIES:
        setuptool.setImportContext(importcontext)
        setuptool.runAllImportSteps()
        logger.info("Installed dependency %s" % name)

    # DCWorkflowDump doesn't yet support the 'manager_bypass'
    wf_id = 'indicators_workflow'
    wf_tool = getToolByName(site, 'portal_workflow')
    if wf_id in wf_tool.objectIds():
        wfobj = wf_tool.getWorkflowById(wf_id)
        wfobj.manager_bypass = 1
        logger.info("Set 'Manager role bypasses guards' to True for 'indicators_workflow'")

    # Enable portal_factory for given types
    factory_tool = getToolByName(site, 'portal_factory')
    factory_types = [
        "IndicatorFactSheet",
        "KeyMessage",
        "FactSheetDocument",
        ] + factory_tool.getFactoryTypes().keys()
    factory_tool.manage_setPortalFactoryTypes(listOfTypeIds=factory_types)
    logger.info("Factory tool enabled for IndicatorFactSheet, KeyMessage and FactSheetDocument")

    # Enable aliases (redirects) for eea.indicators content types
    redirection_tool = getToolByName(site, 'portal_redirection')
    ctypes = ["IndicatorFactSheet",
              "KeyMessage",
              "FactSheetDocument",
              "Specification",
              "Assessment",
              "AssessmentPart",
              "ExternalDataSpec",
              "MethodologyReference",
              "PolicyDocumentReference",
              "PolicyQuestion",
              "RationaleReference",
              "WorkItem"]
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

    vkey = 'indicator_codes'
    if hasattr(atvm, vkey):
        return

    atvm.invokeFactory('SimpleVocabulary', vkey)
    vocab = atvm[vkey]
    for key in CODES:
        vocab.invokeFactory('SimpleVocabularyTerm', key)
        vocab[key].setTitle(key)

def setup_misc(context):
    """ Stub step to enable setting dependent steps """

    return

##/code-section FOOT
