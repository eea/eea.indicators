# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
##/code-section HEAD

class IPolicyQuestion(Interface):
    """Marker interface for .PolicyQuestion.PolicyQuestion
    """

class ISpecificationsFolder(Interface):
    """Marker interface for .SpecificationsFolder.SpecificationsFolder
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

##code-section FOOT
##/code-section FOOT