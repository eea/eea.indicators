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


PROJECTNAME = "eea.indicators"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))
ADD_CONTENT_PERMISSIONS = {
    'PolicyQuestion': 'Add portal content',
    'ExternalDataSpec': 'Add portal content',
    'MethodologyReference': 'Add portal content',
    'Specification': 'Add portal content',
    'Assessment': 'Add portal content',
    'RationaleReference': 'Add portal content',
    'AssessmentPart': 'Add portal content',
    'PolicyDocumentReference': 'Add portal content',
    'WorkItem': 'Add portal content',
}

setDefaultRoles('Add portal content', ('Manager','Owner'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
# override in custom configuration
DEPENDENCIES = []

# Dependend products - not quick-installed - used in testcase
# override in custom configuration
PRODUCT_DEPENDENCIES = []

##code-section config-bottom #fill in your manual code here
import os
from Globals import package_home
templates_dir =  os.path.join(package_home(product_globals), 'browser/templates')

CODES = [
        'APE',
        'CLIM',
        'EECCA',
        'ENER',
        'Outlook',
        'SEBI',
        'TERM',
        'WBSCI',
        'CSI',
        'IRENA',
        ]

DPSIR = [
    ('None', 'N/A'),
    ('D', 'Driving force'),
    ('P', 'Pressure'),
    ('S', 'State'),
    ('I', 'Impact'),
    ('R', 'Response')
    ]

TYPOLOGY = [
    ('None', 'N/A'),
    ('A', 'Descriptive indicator (Type A – What is happening to the environment and to humans?)'),
    ('B', 'Performance indicator (Type B – Does it matter?)'),
    ('C', 'Efficiency indicator (Type C – Are we improving?)'),
    ('D', 'Policy-effectiveness indicator (Type D)'),
    ('E', 'Total welfare indicator (Type E – Are we on whole better off?)')
    ]

CATEGORY_OF_USE = [
     ("None", "N/A"),
     ('DataUseCategory_01','Main dataset'),
     ('DataUseCategory_02','Dataset for gapfilling'),
     ('DataUseCategory_03','Dataset for normalizing'),
     ('DataUseCategory_04','Indicator dataset')
    ]

# These are the profiles that installed as dependencies on install
#True = QuickInstaller, False: GenericSetup
PROFILE_DEPENDENCIES = (
         ('DataGridField', 'profile-Products.DataGridField:default_25x', True),
         ('UserAndGroupSelectionWidget',  'profile-Products.UserAndGroupSelectionWidget:default', False),
         ('eea.workflow', 'profile-eea.workflow:default', False),
         ('eea.dataservice', 'profile-eea.dataservice:default', True),
         ('eea.relations', 'profile-eea.relations:a', True),
         #('eea.relations', 'profile-eea.relations:b', True),
         ('eea.versions', 'profile-eea.versions:default', False),
    )


#this is the role that people need to receive to become a manager over a specification
MANAGER_ROLE = 'ContentManager'
##/code-section config-bottom


# Load custom configuration not managed by archgenxml
try:
    from eea.indicators.AppConfig import *
except ImportError:
    pass