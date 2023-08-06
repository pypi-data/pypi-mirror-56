from aldryn_forms.models import FieldPluginBase
from django.db import models
from django.utils.translation import ugettext_lazy as _


FIELD_CHOICES = [
    ('userid',      'User ID'),
    ('username',    'Username'),
    ('firstlast',   'First Last'),
    ('lastfirst',   'Last, First'),
    ('email',       'Email Address')
]


class CurrentUserFieldPlugin(FieldPluginBase):
    initial_value = models.CharField(
        verbose_name=_('Selected value'),
        max_length=255,
        blank=True,
        help_text=_('Select which value to retrieve.'),
        choices=FIELD_CHOICES
    )