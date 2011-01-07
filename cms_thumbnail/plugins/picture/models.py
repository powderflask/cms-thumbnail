from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.plugins.picture.models import Picture as CMSPicture
from cms_thumbnail.models import Preset


class ICPicture(CMSPicture):
    """
    Extends basic Picture plugin to add an optional cms_thumbnail preset
    """
    # @todo - add "link to full-size image" option?
    preset = models.ForeignKey(Preset, verbose_name=_("image preset"), null=True, blank=True, help_text=_("defines geometry and options for displaying image"))
