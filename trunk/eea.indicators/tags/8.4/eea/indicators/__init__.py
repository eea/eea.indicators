# -*- coding: utf-8 -*-
#
# $Id$

"""The eea.indicators package"""
from Products.Archetypes import listTypes
from Products.Archetypes.atapi import process_types
from Products.CMFCore import utils
from eea.indicators.config import PROJECTNAME
from eea.indicators.config import DEFAULT_ADD_CONTENT_PERMISSION
from eea.indicators.config import ADD_CONTENT_PERMISSIONS
from zope.i18nmessageid import MessageFactory
msg_factory = MessageFactory('indicators')


def initialize(context):
    """initialize product (called by zope)"""
    # imports packages and types for registration
    from eea.indicators import content
    content.register()

    # Initialize portal content
    all_content_types, all_constructors, all_ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = all_content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = all_constructors,
        fti                = all_ftis,
        ).initialize(context)

    # Give it some extra permissions to control them on a per class limit
    for i in range(0, len(all_content_types)):
        klassname = all_content_types[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue

        context.registerClass(meta_type   = all_ftis[i]['meta_type'],
                              constructors= (all_constructors[i],),
                              permission  = ADD_CONTENT_PERMISSIONS[klassname])

