from __future__ import unicode_literals

from django.conf.urls import patterns, url
from buildbotstatus.extension import Buildbotstatus
from buildbotstatus.forms import BuildbotstatusSettingsForm

urlpatterns = patterns(
    '',

    url(r'^$',
        'reviewboard.extensions.views.configure_extension',
        {
            'ext_class': Buildbotstatus,
            'form_class': BuildbotstatusSettingsForm,
        }),
)
