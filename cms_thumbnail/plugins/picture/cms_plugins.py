from cms.plugin_pool import plugin_pool
#from cms.plugin_base import CMSPluginBase
from cms.plugins.picture.cms_plugins import PicturePlugin as CMSPicturePlugin
from cms_thumbnail.plugins.picture.models import ICPicture
from django.conf import settings

class ICPicturePlugin(CMSPicturePlugin):
    model = ICPicture
    #name = "Thumbnail"  # @todo: remove this!
    render_template = "cms_thumbnail/picture.html"

    def render(self, context, instance, placeholder):
        if instance.preset and not instance.url and not instance.page_link:
            instance.url = instance.image.url
        return super(ICPicturePlugin, self).render(context, instance, placeholder)
    
    def icon_src(self, instance):
        # TODO - possibly use 'instance' and provide a thumbnail image
        return settings.CMS_MEDIA_URL + u"images/plugins/image.png"
 
plugin_pool.register_plugin(ICPicturePlugin)
