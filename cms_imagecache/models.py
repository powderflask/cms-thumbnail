import re
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import smart_split
from django.utils.encoding import smart_str

kw_pat = re.compile(r'^(?P<key>[\w]+)=[\"\']+(?P<value>.+)[\"\']+$')

class Preset(models.Model):
    """
       @todo:
         - would be more efficient / simpler to store options as a pickled dictionary?
         - on save, clear cache of the old preset images if anything changed.
    """
    name = models.CharField(_("preset name"), unique=True, db_index=True, max_length=50)
    geometry = models.CharField(_("thumbnail geometry"), max_length=12, help_text=_("Geometry Format: WIDTHxHEIGHT or WIDTH or xHEIGHT"))
    options = models.TextField(_("thumbnail options"), help_text=_("thumbnail options.  E.g., crop='80% top'"))

    class Meta:
        verbose_name = _("ImageCache Preset")
        verbose_name_plural = _("ImageCache Presets")

    def __unicode__(self):
        return self.name

    def get_options(self):
        options = {}
        bits = iter(smart_split(self.options))
        for bit in bits:
            m = kw_pat.match(bit)
            if not m:  # @todo - add custom validation - this should never happen
                raise Exception("Invalid preset option: "%bit)
            key = smart_str(m.group('key'))
            value = smart_str(m.group('value'))
            options[key] = value
        return options
