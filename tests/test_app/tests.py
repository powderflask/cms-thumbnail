import os
import shutil
import unittest
from django.template.loader import render_to_string
from os.path import join as pjoin
from PIL import Image
from sorl.thumbnail.conf import settings
from sorl.thumbnail.helpers import get_module_class
from cms_imagecache.models import Preset
from test_app.models import Item


class SimpleTestCaseBase(unittest.TestCase):
    def setUp(self):
        self.backend = get_module_class(settings.THUMBNAIL_BACKEND)()
        self.engine = get_module_class(settings.THUMBNAIL_ENGINE)()
        self.kvstore = get_module_class(settings.THUMBNAIL_KVSTORE)()
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
        dims = [
            (500, 500),
            (100, 100),
        ]
        for dim in dims:
            name = '%sx%s.jpg' % dim
            fn = pjoin(settings.MEDIA_ROOT, name)
            im = Image.new('L', dim)
            im.save(fn)
            Item.objects.get_or_create(image=name)

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT)

class SimpleTestCase(SimpleTestCaseBase):
    def testSimple(self):
        item = Item.objects.get(image='500x500.jpg')
        t = self.backend.get_thumbnail(item.image, '400x300', crop='center')
        self.assertEqual(t.x, 400)
        self.assertEqual(t.y, 300)
        t = self.backend.get_thumbnail(item.image, '1200x900', crop='13% 89%')
        self.assertEqual(t.x, 1200)
        self.assertEqual(t.y, 900)

class ImagecacheTestCase(SimpleTestCaseBase):
    def setUp(self):
        super(ImagecacheTestCase, self).setUp()
        presets = [
            ("100x100", "100x100", {}),
            ("test_1",  "200x100", {'crop':"50% 50%"}),
            ("test_2", "200x100", {}),
            ("test_6", "400x400", {}),
            ("test_7", "100x100", {'crop':"center", 'upscale':"True", 'quality':70})
        ]
        for p in presets:
            Preset.objects.get_or_create(name=p[0], geometry=p[1], 
                                         defaults={'options':p[2]})

    def testModel(self):
        item = Item.objects.get(image='500x500.jpg')
        for t in ['thumbnailpreset1.html', 'thumbnailpreset1a.html']:
            val = render_to_string(t, {
                'preset': Preset.objects.get(name="test_1"),
                'item': item,
            }).strip()
            self.assertEqual(val, u'<img style="margin:0px 0px 0px 0px" width="200" height="100">')
        
        for t in ['thumbnailpreset2.html', 'thumbnailpreset2a.html']:
            val = render_to_string(t, {
                'preset': Preset.objects.get(name="test_2"),
                'item': item,
            }).strip()
            self.assertEqual(val, u'<img style="margin:0px 50px 0px 50px" width="100" height="100">')

    def test_nested(self):
        item = Item.objects.get(image='500x500.jpg')
        val = render_to_string('thumbnailpreset6.html', {
            'item': item,
        }).strip()
        self.assertEqual(val, ('<a href="/media/test/cache/57/ba/57ba10c5a6c56dc71362d9b1427cb0b4.jpg">'
                               '<img src="/media/test/cache/6c/c3/6cc32cd4aa002c577b534442c11e07d2.jpg" width="400" height="400">'
                               '</a>'))

