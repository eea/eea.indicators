""" eea.rdfmarshaller customizations
"""

from Products.Archetypes.interfaces import IField
from eea.rdfmarshaller.archetypes.fields import ATField2Surf
from eea.rdfmarshaller.interfaces import ISurfSession
from zope.component import adapts
from zope.interface import Interface


class CodesField2Surf(ATField2Surf):
    """rdfmarshaller field adapter for the codes field
    """
    adapts(IField, Interface, ISurfSession)

    def value(self):
        """return value suitable for surf
        """
        value = self.field.getAccessor(self.context)()
        if not value:
            return None
        return ["%s%s" % (v['set'], v['code'])
                                 for v in value]
