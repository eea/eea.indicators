# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
##/code-section HEAD

class IEEAData(Interface):
    """Marker interface for .EEAData.EEAData
    """

class IPublication(Interface):
    """Marker interface for .Publication.Publication
    """

class IEEAFigureFile(Interface):
    """Marker interface for .EEAFigureFile.EEAFigureFile
    """

class IEEAFigure(Interface):
    """Marker interface for .EEAFigure.EEAFigure
    """

class IImageFile(Interface):
    """Marker interface for .ImageFile.ImageFile
    """

##code-section FOOT
##/code-section FOOT