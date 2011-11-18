# -*- coding: utf-8 -*-
#
# $Id$
#

""" The content types package
"""
from Products.validation import validation
from Products.Archetypes.atapi import registerType

from eea.indicators.config import PROJECTNAME
from eea.indicators.content.PolicyQuestion import PolicyQuestion
from eea.indicators.content.ExternalDataSpec import ExternalDataSpec
from eea.indicators.content.MethodologyReference import MethodologyReference
from eea.indicators.content.Specification import Specification
from eea.indicators.content.Assessment import Assessment
from eea.indicators.content.RationaleReference import RationaleReference
from eea.indicators.content.AssessmentPart import AssessmentPart
from eea.indicators.content.WorkItem import WorkItem
from eea.indicators.content.FactSheetDocument import FactSheetDocument
from eea.indicators.content.IndicatorFactSheet import IndicatorFactSheet
from eea.indicators.content.KeyMessage import KeyMessage
from eea.indicators.content.PolicyDocumentReference import (
    PolicyDocumentReference,
)

from eea.indicators.content.validators import (
    UniquePolicyDocTitleValidator,
    UniquePolicyDocUrlValidator,
    OneAssessmentPartPerQuestionValidator,
)

def register():
    """ Register custom content
    """
    # Validators
    validation.register(
        UniquePolicyDocTitleValidator('unique_policy_title_validator'))
    validation.register(
        UniquePolicyDocUrlValidator('unique_policy_url_validator'))
    validation.register(
        OneAssessmentPartPerQuestionValidator('one_assessment_per_question'))

    # Content
    registerType(PolicyQuestion, PROJECTNAME)
    registerType(ExternalDataSpec, PROJECTNAME)
    registerType(MethodologyReference, PROJECTNAME)
    registerType(Specification, PROJECTNAME)
    registerType(Assessment, PROJECTNAME)
    registerType(RationaleReference, PROJECTNAME)
    registerType(AssessmentPart, PROJECTNAME)
    registerType(PolicyDocumentReference, PROJECTNAME)
    registerType(WorkItem, PROJECTNAME)

    # V1 content
    registerType(FactSheetDocument, PROJECTNAME)
    registerType(IndicatorFactSheet, PROJECTNAME)
    registerType(KeyMessage, PROJECTNAME)
