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
        if not self.value:
            return None
        return ["%s%s" % (v['set'], v['code'])
                                 for v in self.value]
