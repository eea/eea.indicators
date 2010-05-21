from AccessControl import ClassSecurityInfo
from Products.Archetypes.utils import mapply
from Products.CMFCore import permissions
from zope import event
from zope.app.event import objectevent
import logging


class ModalFieldEditableAware(object):
    security = ClassSecurityInfo()

    security.declareProtected(permissions.ModifyPortalContent, 'simpleProcessForm')
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
            return

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
        __traceback_info__ = (self, field, mutator)
        result[1]['field'] = field.__name__
        mapply(mutator, result[0], **result[1])

        self.reindexObject()

        self.unmarkCreationFlag()
        if self._at_rename_after_creation and is_new_object:
            self._renameAfterCreation(check_auto_id=True)

        # Post create/edit hooks
        if is_new_object:
            self.at_post_create_script()
        else:
            self.at_post_edit_script()

        event.notify(objectevent.ObjectModifiedEvent(self))
        logging.info("SimpleProcessForm done")
        return

    security.declareProtected(permissions.View, 'simple_validate')
    def simple_validate(self, REQUEST, errors=None):

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
        for name, field in fields:
            error = 0
            value = None
            widget = field.widget
            if form:
                result = widget.process_form(instance, field, form,
                                             empty_marker=_marker)
            else:
                result = None
            if result is None or result is _marker:
                accessor = field.getEditAccessor(instance) or field.getAccessor(instance)
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
    """Content classes subclassing this want to customize how contained objects are created

    These object factories are used in the Specification Aggregated Edit View
    The main method is object_factory, which reads the request to look for a type_name
    parameter. It returns a html structure with info about the newly created object.
    """

    security = ClassSecurityInfo()

    def _error(self, error):
        return u"<div class='metadata'><div class='error'>" + error + "</div></div>"

    def _success(self, **kw):
        obj = kw['obj']
        subview = kw.get('subview', 'schemata_edit')
        url = obj.absolute_url() + '/' + subview
        f = kw.get('direct_edit') and "<div class='direct_edit' />" or ''

        return "<div class='metadata'>" + f + "<div class='object_edit_url'>" + url + "</div></div>" 

    #TODO: change permission to 'Add portal content'
    security.declareProtected(permissions.ModifyPortalContent, 'object_factory')
    def object_factory(self):
        """Create an object according to special rules for that object """

        type_name = self.REQUEST['type_name']
        factory_name = 'factory_' + type_name
        factory = getattr(self, factory_name, None)
        if factory is None:
            return self._error("Don't know how to create object of type %s" % type_name)

        info = factory()
        error = info.get('error')
        if error:
            return self._error(error)

        return self._success(**info)

    def _generic_factory(self, type_name):
        id = self.generateUniqueId(type_name)
        new_id = self.invokeFactory(type_name=type_name,
                id=id,
                title=self.translate(
                    msgid='label-newly-created-type',
                    domain='indicators',
                    default="Newly created ${type_name}",
                    mapping={'type_name':type_name},
                    ))
        
        ref = self[new_id]
        return {'obj':ref, 'error':'', 'subview':'schemata_edit', 'direct_edit':False}
