# -*- coding: utf-8 -*-
#
# $Id$

import logging
logger = logging.getLogger('indicators')
logger.debug('Installing Product')

import os
import os.path
from Globals import package_home
from Products.Archetypes import listTypes
from Products.Archetypes.atapi import *
from Products.CMFCore import DirectoryView
from Products.CMFCore import utils as cmfutils
from config import *

DirectoryView.registerDirectory('skins', product_globals)

# temporarily add the path to the namespace package to the products path,
# so that the directory views are set up correctly
# Register our skins directory - this makes it available via portal_skins.

from Products.CMFCore import utils
from os.path import dirname
ppath = utils.ProductsPath
utils.ProductsPath.append(dirname(package_home(product_globals)))
DirectoryView.registerDirectory('skins', product_globals)
utils.ProductsPath = ppath

from zope.i18nmessageid import MessageFactory
msg_factory = MessageFactory('indicators')


def initialize(context):
    """initialize product (called by zope)"""
    # imports packages and types for registration
    import content

    # Initialize portal content
    all_content_types, all_constructors, all_ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = all_content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = all_constructors,
        fti                = all_ftis,
        ).initialize(context)

    # Give it some extra permissions to control them on a per class limit
    for i in range(0,len(all_content_types)):
        klassname=all_content_types[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue

        context.registerClass(meta_type   = all_ftis[i]['meta_type'],
                              constructors= (all_constructors[i],),
                              permission  = ADD_CONTENT_PERMISSIONS[klassname])
