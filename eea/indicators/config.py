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


# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.
#
# If you wish to perform custom configuration, you may put a file
# AppConfig.py in your product's root directory. The items in there
# will be included (by importing) in this file if found.

from Products.CMFCore.permissions import setDefaultRoles
##code-section config-head #fill in your manual code here
##/code-section config-head


PROJECTNAME = "indicators"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))
ADD_CONTENT_PERMISSIONS = {
    'PolicyQuestion': 'indicators: Add PolicyQuestion',
    'SpecificationsFolder': 'indicators: Add SpecificationsFolder',
    'ExternalDataSpec': 'indicators: Add ExternalDataSpec',
    'MethodologyReference': 'indicators: Add MethodologyReference',
    'Specification': 'indicators: Add Specification',
    'Assessment': 'indicators: Add Assessment',
    'RationaleReference': 'indicators: Add RationaleReference',
    'AssessmentPart': 'indicators: Add AssessmentPart',
    'PolicyDocumentReference': 'indicators: Add PolicyDocumentReference',
}

setDefaultRoles('indicators: Add PolicyQuestion', ('Manager','Owner'))
setDefaultRoles('indicators: Add SpecificationsFolder', ('Manager','Owner'))
setDefaultRoles('indicators: Add ExternalDataSpec', ('Manager','Owner'))
setDefaultRoles('indicators: Add MethodologyReference', ('Manager','Owner'))
setDefaultRoles('indicators: Add Specification', ('Manager','Owner'))
setDefaultRoles('indicators: Add Assessment', ('Manager','Owner'))
setDefaultRoles('indicators: Add RationaleReference', ('Manager','Owner'))
setDefaultRoles('indicators: Add AssessmentPart', ('Manager','Owner'))
setDefaultRoles('indicators: Add PolicyDocumentReference', ('Manager','Owner'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

##code-section config-bottom #fill in your manual code here
##/code-section config-bottom


# Load custom configuration not managed by archgenxml
try:
    from eea.indicators.AppConfig import *
except ImportError:
    pass
