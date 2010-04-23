# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
from eea.indicators.content.IIndicatorAssessment import IIndicatorAssessment
##/code-section HEAD

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

##code-section FOOT
class IFactSheetDocument(Interface):
    """Marker interface for .FactSheetDocument.FactSheetDocument
    """

class IIndicatorFactSheet(Interface):
    """Marker interface for .IndicatorFactSheet.IndicatorFactSheet
    """

class IKeyMessage(Interface):
    """Marker interface for .KeyMessage.KeyMessage
    """

##/code-section FOOT
