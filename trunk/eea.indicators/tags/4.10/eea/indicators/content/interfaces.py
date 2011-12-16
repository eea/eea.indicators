# -*- coding: utf-8 -*-

""" Interfaces for content types"""

from zope.interface import Interface


class IPolicyQuestion(Interface):
    """Marker interface for .PolicyQuestion.PolicyQuestion
    """

class IExternalDataSpec(Interface):
    """Marker interface for .ExternalDataSpec.ExternalDataSpec
    """

class IMethodologyReference(Interface):
    """Marker interface for .MethodologyReference.MethodologyReference
    """

class ISpecification(Interface):
    """Marker interface for .Specification.Specification
    """

class IAssessment(Interface):
    """Marker interface for .Assessment.Assessment
    """

class IRationaleReference(Interface):
    """Marker interface for .RationaleReference.RationaleReference
    """

class IAssessmentPart(Interface):
    """Marker interface for .AssessmentPart.AssessmentPart
    """

class IPolicyDocumentReference(Interface):
    """Marker interface for .PolicyDocumentReference.PolicyDocumentReference
    """

class IWorkItem(Interface):
    """Marker interface for .WorkItem.WorkItem
    """

class IFactSheetDocument(Interface):
    """Marker interface for .FactSheetDocument.FactSheetDocument
    """

class IIndicatorFactSheet(Interface):
    """Marker interface for .IndicatorFactSheet.IndicatorFactSheet
    """

class IKeyMessage(Interface):
    """Marker interface for .KeyMessage.KeyMessage
    """

class IIndicatorAssessment(Interface):
    """Marker interface for assessments objects:
         Assessment and IndicatorFactSheet
    """

class IIndicatorsDatabase(Interface):
    """Marker interface for folders storing a bunch of indicators
    """
