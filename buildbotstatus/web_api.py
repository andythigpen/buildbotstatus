from django.core.exceptions import ObjectDoesNotExist
from djblets.webapi.decorators import (webapi_login_required,
                                       webapi_response_errors,
                                       webapi_request_fields)
from djblets.webapi.errors import DOES_NOT_EXIST
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.resources import WebAPIResource
from reviewboard.webapi.resources.review_request import review_request_resource
from reviewboard.extensions.base import get_extension_manager
import json
from buildbot import find_builds

class BuildbotRefreshResource(WebAPIResource):
    """Resource for refreshing buildbot status"""
    name = 'buildbotstatus_refresh'
    uri_name = 'refresh'
    allowed_methods = ('POST',)

    def has_modify_permissions(self, request, *args, **kwargs):
        return review_request.is_accessible_by(request.user)

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST)
    @webapi_request_fields(
        required={
            'review_request_id': {
                'type': int,
                'description': 'The ID of the review request',
            },
        },
    )
    def create(self, request, review_request_id, *args, **kwargs):
        try:
            review_request = review_request_resource.get_object(
                request, *args, review_request_id=review_request_id, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        em = get_extension_manager()
        ext = em.get_enabled_extension('buildbotstatus.extension.Buildbotstatus')
        url = ext.settings['buildbot_url']
        if not url:
            raise Exception('No Buildbot URL configured')
        commit_id = review_request.commit_id
        statuses = find_builds(url, commit_id)

        for status in statuses:
            status['url'] = 'http://%s/builders/%s/builds/%s' % \
                    (url, status['builderName'], status['number'])
            status['cssClass'] = 'buildbot-failure'
            status['result'] = ' '.join(status['text'])
            warnings = int(status.get('warnings-count', 0))
            if warnings > 0:
                status['cssClass'] = 'buildbot-warning'
                status['result'] = '%s warnings' % warnings
            elif 'success' in status['result']:
                status['cssClass'] = 'buildbot-success'

        return 201, {
            self.item_result_key: json.dumps(statuses),
        }

buildbot_refresh_resource = BuildbotRefreshResource()
