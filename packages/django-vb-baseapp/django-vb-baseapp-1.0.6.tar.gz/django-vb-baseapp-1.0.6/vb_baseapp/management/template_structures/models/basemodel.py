"""
CustomBaseModel template for model generator
"""

TEMPLATE_MODEL_BASEMODEL = """import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from console import console
from vb_baseapp.models import CustomBaseModel

__all__ = ['{model_name_title}']

logger = logging.getLogger('app')
console = console(source=__name__)


class {model_name_title}(CustomBaseModel):
    title = models.CharField(max_length=255, verbose_name=_('title'))

    class Meta:
        app_label = '{app_name}'
        verbose_name = _('{model_name}')
        verbose_name_plural = _('{model_name}s')  # check pluralization

    def __str__(self):
        return self.title

"""


__all__ = ['TEMPLATE_MODEL_BASEMODEL']
