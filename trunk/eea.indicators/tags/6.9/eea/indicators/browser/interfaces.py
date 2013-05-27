"""The interfaces for the browser package"""

from zope.interface import Interface

class IIndicatorsPermissionsOverview(Interface):
    """Overview of indicators database permissions"""

    #def get_users_map():
    #    """Returns user-centered details about specs roles"""

    #def get_specs_map():
    #    """Returns spec-centered details about roles"""


class IIndicatorUtils(Interface):
    """This view can provide various utilities"""
    #str_to_id = Attribute(u"String to Id conversion")

    def str_to_id():
        """Convert an ordinary string (maybe title) to something that
           can be used as a DOM element ID
        """

    def field_has_value(fieldname, context):
        """Return True if the given field has a value
           for the given context object
        """
