import json
import mock
import zeit.cms.browser.interfaces
import zeit.cms.testing
import zeit.retresco.testing
import zope.publisher.browser


class LocationAutocompleteTest(zeit.cms.testing.ZeitCmsBrowserTestCase):

    layer = zeit.retresco.testing.ZCML_LAYER

    def test_search_location(self):
        from zeit.retresco.tag import Tag
        request = zope.publisher.browser.TestRequest(
            skin=zeit.cms.browser.interfaces.ICMSLayer,
            SERVER_URL='http://localhost/++skin++vivi')
        url = zope.component.getMultiAdapter(
            (zeit.cms.tagging.source.locationSource(None), request),
            zeit.cms.browser.interfaces.ISourceQueryURL)
        with mock.patch('zeit.retresco.connection.TMS.get_locations') as gl:
            gl.return_value = [Tag(u'Schweiz', u'location'),
                               Tag(u'Frankreich', u'location')]
            b = self.browser
            b.open(url + '?term=ei')
            result = json.loads(b.contents)
        self.assertEqual([{u'label': u'Schweiz', u'value': u'Schweiz'},
                          {u'label': u'Frankreich', u'value': u'Frankreich'}],
                         result)
