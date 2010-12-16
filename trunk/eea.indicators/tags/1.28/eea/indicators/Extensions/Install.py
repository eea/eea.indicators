# -*- coding: utf-8 -*-
#
# $Id$
#

"""QuickInstaller support for eea.indicators"""

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
    importcontext = 'profile-%s:default' % PROJECTNAME
    setuptool.setImportContext(importcontext)
    setuptool.runAllImportSteps()
    return out.getvalue()
