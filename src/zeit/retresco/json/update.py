from zeit.retresco.update import index_async
import json
import logging
import zeit.cms.browser.view

log = logging.getLogger(__name__)


class UpdateKeywords(zeit.cms.browser.view.Base):

    def __call__(self):
        status = {
            'message': '',
            'invalid': [],
            'updated': [],
            'updated_content': [],
        }

        if self.request.method != 'POST':
            status['message'] = 'Only POST supported'
            self.request.response.setStatus(405)
            return json.dumps(status)

        try:
            body = self.request.bodyStream.read(
                int(self.request['CONTENT_LENGTH']))
            doc_ids = json.loads(body)['doc_ids']
        except:
            status['message'] = (
                'JSON body with parameter doc_ids (list of uuids) required')
            self.request.response.setStatus(400)
            return json.dumps(status)

        for doc_id in doc_ids:
            try:
                content = zeit.cms.content.contentuuid.uuid_to_content(
                    zeit.cms.content.interfaces.IUUID(doc_id))
                index_async(content.uniqueId, True, True)
                status['updated'].append(doc_id)
                status['updated_content'].append(content.uniqueId)
            except (AttributeError, TypeError):
                status['invalid'].append(doc_id)
                continue
            else:
                log.info('Scheduling %s for reindex', content.uniqueId)
        status['message'] = 'Nothing updated'
        if status['updated']:
            status['message'] = 'Update successful'
        return json.dumps(status)
