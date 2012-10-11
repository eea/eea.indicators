from eea.rdfmarshaller.archetypes.fields import ATField2Surf

class CodesField2Surf(ATFiled2Surf):
    """rdfmarshaller field adapter for the codes field
    """
    adapts(IField, Interface, ISurfSession)

    def value(self):
        if not self.value:
            return None
        return ["%s%s" % (v['set'], v['code'])
                                 for v in self.value]
