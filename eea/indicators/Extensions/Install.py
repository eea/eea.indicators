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

    setuptool = getToolByName(self, 'portal_setup')   
    importcontext = 'profile-eea.%s:default' % PROJECTNAME
    setuptool.setImportContext(importcontext)
    setuptool.runAllImportSteps()
    return out.getvalue()
