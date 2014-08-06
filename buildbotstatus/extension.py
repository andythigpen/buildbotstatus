# buildbotstatus Extension for Review Board.

from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include
from django.template import Context, loader
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import (ReviewRequestFieldsHook,
                                          ReviewRequestActionHook)
from reviewboard.reviews.fields import (BaseEditableField,
                                        get_review_request_fieldset)
from web_api import buildbot_refresh_resource

class BuildbotstatusField(BaseEditableField):
    field_id = 'buildbotstatus_status'
    label = 'Buildbot Status'
    default_css_classes = []

    def render_change_entry_html(self, info):
        return 'refreshed'

    def should_render(self, value):
        '''Only render this field for reviews with associated commit IDs.'''
        return bool(self.review_request_details.commit_id)

    def render_value(self, value):
        t = loader.get_template('buildbotstatus/status.html')
        c = Context({"statuses" : value or []})
        html = t.render(c)
        return html


class BuildbotReviewRequestActionHook(ReviewRequestActionHook):
    def get_actions(self, context):
        """Returns the list of action information for this action."""
        request = context['request']
        review_request = context['review_request']
        perms = context['perms']
        if not review_request.commit_id:
            return []
        if request.user.pk != review_request.submitter_id:
            return []
        return self.actions


class Buildbotstatus(Extension):
    metadata = {
        'Name': 'buildbotstatus',
        'Summary': 'Displays buildbot status for a review.',
    }
    resources = [buildbot_refresh_resource]

    css_bundles = {
        'default': {
            'source_filenames': ['css/buildbotstatus.css'],
        },
    }

    js_bundles = {
        'default': {
            'source_filenames': [
                'js/buildbotstatus.js',
            ]
        },
    }

    is_configurable = True
    default_settings = {
        'buildbot_url' : '',
    }

    def patch_fieldset_order(self):
        '''
        Unfortunately, this is necessary due to a bug on the client side in
        reviewRequestEditorView.js _resizeLayout that expects the last field
        to be an editable field.
        '''
        main_fieldset = get_review_request_fieldset('main')
        field = main_fieldset.field_classes.pop()
        main_fieldset.field_classes.insert(-1, field)

    def initialize(self):
        ReviewRequestFieldsHook(self, 'main', [BuildbotstatusField])
        self.patch_fieldset_order()
        actions = [
            {
                'id': 'buildbot-status',
                'label': 'Refresh Buildbot Status',
                'url': '#',
            },
        ]
        BuildbotReviewRequestActionHook(self, actions=actions)
