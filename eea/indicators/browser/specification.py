from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView


class IndexPage(BrowserView):
    template = ViewPageTemplateFile('templates/specification_view.pt')

    __call__ = template
