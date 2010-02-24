# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
##/code-section HEAD

class ISpecification(Interface):
    """Marker interface for .Specification.Specification
    """

class ISpecificationsFolder(Interface):
    """Marker interface for .SpecificationsFolder.SpecificationsFolder
    """

class IAssessment(Interface):
    """Marker interface for .Assessment.Assessment
    """

class IPolicyQuestion(Interface):
    """Marker interface for .PolicyQuestion.PolicyQuestion
    """

class IRationaleReference(Interface):
    """Marker interface for .RationaleReference.RationaleReference
    """

class IQuestionAssesment(Interface):
    """Marker interface for .QuestionAssesment.QuestionAssesment
    """

class IExternalDataSpec(Interface):
    """Marker interface for .ExternalDataSpec.ExternalDataSpec
    """

class IMethodologyReference(Interface):
    """Marker interface for .MethodologyReference.MethodologyReference
    """

class IWorkItem(Interface):
    """Marker interface for .WorkItem.WorkItem
    """

class IEEAData(Interface):
    """Marker interface for .EEAData.EEAData
    """

class IEEAFigure(Interface):
    """Marker interface for .EEAFigure.EEAFigure
    """

class IPublication(Interface):
    """Marker interface for .Publication.Publication
    """

##code-section FOOT
##/code-section FOOT