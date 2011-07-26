"""Base classes for eea.indicators content
"""

from AccessControl import ClassSecurityInfo
from Products.Archetypes.utils import mapply
from Products.CMFCore import permissions
from Products.CMFCore.permissions import AddPortalContent
from zope import event
from zope.lifecycleevent import ObjectModifiedEvent


class ExtendedMessage(object):
    """An string to be rendered as HTML
    
    It holds metadata about the contained information
    """

    template = None
    html     = None
    msg      = None
    status   = None

    def __init__(self, template, status, **kwds):
        self.html   = template % kwds
        self.msg    = kwds['msg']
        self.status = status

    def __str__(self):
        return self.html


class ModalFieldEditableAware(object):
    """Classes that want to allow editing of their fields in modal dialogs"""
    security = ClassSecurityInfo()

    security.declareProtected(permissions.ModifyPortalContent,
                              'simpleProcessForm')
    def simpleProcessForm(self, data=1, metadata=0, REQUEST=None, values=None):
        """Processes the schema looking for data in the form.
        """

        #customized to process a single field instead of multiple fields

        is_new_object = self.checkCreationFlag()

        request = REQUEST or self.REQUEST
        _marker = []
        if values:
            form = values
        else:
            form = request.form

        fieldname = form.get('specific_field')
        if not fieldname:
            raise ValueError("Please provide a specific field")

        field = self.schema[fieldname]
        result = field.widget.process_form(self, field, form,
                                           empty_marker=_marker)
        try:
            # Pass validating=False to inform the widget that we
            # aren't in the validation phase, IOW, the returned
            # data will be forwarded to the storage
            result = field.widget.process_form(self, field, form,
                                               empty_marker=_marker,
                                               validating=False)
        except TypeError:
            # Support for old-style process_form methods
            result = field.widget.process_form(self, field, form,
                                               empty_marker=_marker)

        # Set things by calling the mutator
        mutator = field.getMutator(self)
        __traceback_info__ = (self, field, mutator) #tiberich: is it needed?
        result[1]['field'] = field.__name__
        mapply(mutator, result[0], **result[1])

        self.reindexObject()

        self.unmarkCreationFlag()
        #NOTE: at the moment, this is not very elegant
        #the problem is that the objects, when are editing
        #in a composite manner with the aggregated edit view,
        #will change their ids after the first save. For example
        #when editing the title for a Specification, it will
        #change its id. This means that all the URLs that are
        #already on the page (for example adding a PolicyQuestion)
        #will be invalid. To solve this particular case we make
        #the page reload after editing the Title. In all other cases
        #we want to either skip this behaviour or make those objects
        #have their _at_rename_after_creation set to False
        if self._at_rename_after_creation and is_new_object \
          and fieldname == 'title':
            self._renameAfterCreation(check_auto_id=True)

        # Post create/edit hooks
        if is_new_object:
            self.at_post_create_script()
        else:
            self.at_post_edit_script()

        event.notify(ObjectModifiedEvent(self))
        return

    security.declareProtected(permissions.View, 'simple_validate')
    def simple_validate(self, REQUEST, errors=None):
        """Validate simple"""

        #customized because we don't want to validate a whole
        #schemata, because some fields are required

        if errors is None:
            errors = {}

        _marker = []
        form = REQUEST.form
        instance = self

        fieldname = form.get('specific_field')
        if not fieldname:
            raise ValueError("Could not get valid field from the request")

        fields = [(field.getName(), field) for field in
                        self.schema.filterFields(__name__=fieldname)]
        for field_info in fields:
            value = None
            field = field_info[1]
            if form:
                result = field.widget.process_form(instance, field, form,
                                                   empty_marker=_marker)
            else:
                result = None
            if result is None or result is _marker:
                accessor = field.getEditAccessor(instance) or \
                             field.getAccessor(instance)
                if accessor is not None:
                    value = accessor()
                else:
                    # can't get value to validate -- bail
                    continue
            else:
                value = result[0]

            res = field.validate(instance=instance,
                                 value=value,
                                 errors=errors,
                                 REQUEST=REQUEST)
            if res:
                errors[field.getName()] = res
        return errors


class CustomizedObjectFactory(object):
    """Content classes subclassing this want to customize how contained
         objects are created.

       These object factories are used in the Specification Aggregated Edit View
         The main method is object_factory, which reads the request to look for
         a type_name parameter. It returns a html structure with info about
         the newly created object.
    """

    security = ClassSecurityInfo()

    def _error(self, error):
        """Returns error structure"""
        return ExtendedMessage(
            u"<div class='metadata'><div class='error'>%(msg)s</div></div>", 
            'FAILURE',
            msg=error
            )

    def _success(self, **kw):
        """Returns success structure"""
        obj = kw['obj']
        subview = kw.get('subview', 'schemata_edit')
        url = obj.absolute_url() + '/' + subview
        f = kw.get('direct_edit') and "<div class='direct_edit' />" or ''

        return ExtendedMessage(
            u"<div class='metadata'>%(msg)s<div class='object_edit_url'>%(url)s</div></div>",
            'SUCCESS',
            msg=f, url=url
            )

    security.declareProtected(AddPortalContent, 'object_factory')
    def object_factory(self):
        """Create an object according to special rules for that object """

        type_name = self.REQUEST['type_name']
        factory_name = 'factory_' + type_name
        factory = getattr(self, factory_name, None)
        if factory is None:
            return self._error("Don't know how to create object "
                               "of type %s") % type_name

        info = factory()
        error = info.get('error')
        if error:
            return self._error(error)

        return self._success(**info)

    def _generic_factory(self, type_name):
        """Generic factory"""
        gid = self.generateUniqueId(type_name)
        new_id = self.invokeFactory(type_name=type_name,
                id=gid,
                base_impl=True,
                title=self.translate(
                    msgid='label-newly-created-type',
                    domain='indicators',
                    default="Newly created ${type_name}",
                    mapping={'type_name':type_name},
                    ))

        ref = self[new_id]
        return {'obj':ref,
                'error':'',
                'subview':'schemata_edit',
                'direct_edit':False}
