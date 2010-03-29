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


from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from eea.indicators.config import PROJECTNAME

def install(self, reinstall=False):
    """External Method to install indicators

    This method to install a product is kept, until something better will get
    part of Plones front end, which utilize portal_setup.
    """
    out = StringIO()
    print >> out, "Installation log of %s:" % PROJECTNAME

    # eea.indicators import steps
    setuptool = getToolByName(self, 'portal_setup')
    importcontext = 'profile-eea.%s:default' % PROJECTNAME
    setuptool.setImportContext(importcontext)
    setuptool.runAllImportSteps()

    # DCWorkflowDump doesn't yet support the 'manager_bypass'
    wf_id = 'specification_workflow'
    wf_tool = getToolByName(portal, 'portal_workflow')
    if wf_id in wf_tool.objectIds():
        wfobj = wf_tool.getWorkflowById(wf_id)
        wfobj.manager_bypass = 1

    # enable portal_factory for given types
    factory_tool = getToolByName(portal, 'portal_factory')
    factory_types=[
        "Assessment",
        "AssessmentPart",
        "ExternalDataSpec",
        "MethodologyReference",
        "PolicyDocumentReference",
        "PolicyQuestion",
        "RationaleReference",
        "Specification",
        "WorkItem",
        ] + factory_tool.getFactoryTypes().keys()
    factory_tool.manage_setPortalFactoryTypes(listOfTypeIds=factory_types)

    return out.getvalue()
