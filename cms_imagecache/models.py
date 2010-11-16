import re
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import smart_split
from django.utils.encoding import smart_str
from sorl.thumbnail.parsers import ThumbnailParseError, parse_crop
from sorl.thumbnail.templatetags.thumbnail import kw_pat
from picklefield.fields import PickledObjectField

# kw_pat = re.compile(r'^(?P<key>[\w]+)=[\"\']?(?P<value>.+)[\"\']?$')

def deserialize_options(option_string):
    """ 
       Split out options from option_string and return them as a dict 
       Raise ThumbnailParseError if any syntax errors are discovered.
    """
    options = {}
    bits = iter(smart_split(option_string))
    for bit in bits:
        m = kw_pat.match(bit)
        if not m:
            raise ThumbnailParseError("Invalid thumbnail option: %s"%bit)
        key = smart_str(m.group('key'))
        value = smart_str(m.group('value')).strip("\"'")
        
        # if the key is "crop" then validate the crop options - raises ThumbnailParseError is invalid
        if key == "crop":
            parse_crop(value, [0,0], [0,0])
            
        options[key] = value
    return options


class Preset(models.Model):
    """
       @todo:
         - on save, clear cache of the old preset images if anything changed.
    """
    name = models.CharField(_("preset name"), unique=True, db_index=True, max_length=50)
    geometry = models.CharField(_("thumbnail geometry"), max_length=12, help_text=_("Geometry Format: WIDTHxHEIGHT or WIDTH or xHEIGHT"))
    options = PickledObjectField(_("thumbnail options"), null=True, help_text=_("thumbnail options:  key1=value1 key2=value2...  E.g., crop='center top'"))

    class Meta:
        verbose_name = _("Preset")
        verbose_name_plural = _("Presets")

    def __unicode__(self):
        return self.name

    def get_options(self):
        return self.options
    
    def serialize_options(self):
        """ Return a serialized version of options, suitable for editing """
        str = ""
        if self.options:
            for key,value in self.options.iteritems():
                str = str + "%s='%s'\n"%(key, value)
        return str
