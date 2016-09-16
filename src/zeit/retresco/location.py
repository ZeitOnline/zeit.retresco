import grokcore.component as grok
import zeit.cms.tagging.interfaces
import zope.interface


class LocationList(grok.GlobalUtility):
    """Utility to retrieve locations from retresco."""

    zope.interface.implements(zeit.cms.tagging.interfaces.ILocationList)

    def search(self, term):
        tms = zope.component.getUtility(zeit.retresco.interfaces.ITMS)
        return [tag.label for tag in tms.get_locations(term)]
