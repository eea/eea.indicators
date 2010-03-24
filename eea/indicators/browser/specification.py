from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from eea.indicators.content.Specification import required_for_publication


class IndexPage(BrowserView):
    template = ViewPageTemplateFile('templates/specification_view.pt')

    __call__ = template


class SchemataCounts(BrowserView):
    """Returns the count of fields that are required for publishing"""

    def __call__(self):
        fields = required_for_publication

        schematas = {}
        for field in self.context.schema.fields():
            if not field.schemata in schematas:
                schematas[field.schemata] = []
            req = getattr(field, 'required_for_published', False)
            if req:
                if not field.getAccessor(self.context)():  #we assume that the value return is something not empty
                    schematas[field.schemata].append(field.__name__)

        return schematas
