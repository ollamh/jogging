# encoding: utf-8

from tastypie.models import create_api_key

import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class JoggingEntry(models.Model):
    """
    Entry model
    """
    date = models.DateField(verbose_name=_('Date of jogging'))
    duration = timedelta.fields.TimedeltaField(verbose_name=_('Duration'))
    distance = models.FloatField(verbose_name=_('Distance'))
    user = models.ForeignKey(User, related_name='entries')

    @property
    def average_speed(self):
        """
        Returns speed in kmph
        """
        return self.distance/(self.duration.total_seconds()/3600)

models.signals.post_save.connect(create_api_key, sender=User)