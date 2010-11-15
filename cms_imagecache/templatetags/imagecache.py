from django.template import Library, NodeList, TemplateSyntaxError
from sorl.thumbnail.conf import settings
from sorl.thumbnail.images import DummyImageFile
from sorl.thumbnail import default
from cms_imagecache.models import Preset
from sorl.thumbnail.templatetags.thumbnail import ThumbnailNodeBase

register = Library()

@register.tag('imagecache')
class ImageCacheNode(ThumbnailNodeBase):
    child_nodelists = ('nodelist_file', 'nodelist_empty')
    error_msg = ('Syntax error. Expected: ``imagecache source preset as var``')
    preset_error = ('Preset %s not found.')
    
    def __init__(self, parser, token):
        bits = token.split_contents()
        if len(bits) != 5 or bits[-2] != 'as':
            raise TemplateSyntaxError(self.error_msg)
        self.file_ = parser.compile_filter(bits[1])
        self.preset = parser.compile_filter(bits[2])
        self.as_var = bits[-1]
        self.nodelist_file = parser.parse(('empty', 'endimagecache',))
        if parser.next_token().contents == 'empty':
            self.nodelist_empty = parser.parse(('endimagecache',))
            parser.delete_first_token()
        else:
            self.nodelist_empty = NodeList()

    def _render(self, context):
        file_ = self.file_.resolve(context)
        preset_name = self.preset.resolve(context)
        preset = Preset.objects.get(name=preset_name)
        if settings.THUMBNAIL_DUMMY:
            thumbnail = DummyImageFile(preset.geometry)
        elif file_:
            thumbnail = default.backend.get_thumbnail(
                file_, preset.geometry, **preset.get_options()
                )
        else:
            return self.nodelist_empty.render(context)
        context.push()
        context[self.as_var] = thumbnail
        output = self.nodelist_file.render(context)
        context.pop()
        return output

    def __repr__(self):
        return "<ImageCacheNode>"

    def __iter__(self):
        for node in self.nodelist_file:
            yield node
        for node in self.nodelist_empty:
            yield node
