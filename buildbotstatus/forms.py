from django import forms
from djblets.extensions.forms import SettingsForm

class BuildbotstatusSettingsForm(SettingsForm):
    buildbot_url = forms.CharField(help_text="Buildbot URL")
