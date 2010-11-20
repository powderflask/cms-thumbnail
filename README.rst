==============================
Django CMS ImageCache
==============================

CMS ImageCache exposes sorl-thumbnail's image processing and caching functionality within `Django CMS <http://www.django-cms.org/>`_.

The module is inspired by `Drupal's imagecache module <http://drupal.org/project/imagecache>`_.

Currently in development - DO NOT USE for production sites!

NOTE: Requires fix for django-cms issue #588 (hopefully in trunk soon).
 
Features
========

* Named "presets" define image processing rules (image geometry and options).
* Content editors can choose which preset to display image with (or even define their own presets)
* Picutre plugin extends and replaces the django-cms Picture plugin to add an imagecache preset.
* Built on top of the excellent `sorl-thumbnail <https://github.com/sorl/sorl-thumbnail>`_ module - provides loads of flexibility and extensibility.

Dependencies
============

* django-cms 2.1+
* sorl-thumbnail 10.12+
* python 2.6+  (required by sorl-thumbnail)

License
=======
    Copyright (C) 2010  Driftwood Cove Designs

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    `GNU General Public License <http://github.com/powderflask/cms-imagecache/blob/master/LICENSE>`_ for more details

You are free to copy, use, or modify this software in any way you like, but please provide attribution to the original author with a link to:
https://github.com/powderflask/cms-imagecache

Author
------
`Driftwood Cove Designs <http://designs.driftwoodcove.ca>`_

Known Issues
============

see: https://github.com/powderflask/cms-imagecache/issues


Installation
============

From PyPI
---------

not yet - sorry.

Manual Download
---------------

You can download a zipped archive from http://github.com/powderflask/cms-imagecache/downloads.

Unzip the file you downloaded. Then go in your terminal and ``cd`` into the unpacked folder. Then type ``python setup.py install`` in your terminal.

Configuration
-------------
Add the base module and one or more plugins to your ``INSTALLED_APPS`` in settings.py::

    INSTALLED_APPS = (..., 
        'cms_imagecache',            # installs Preset model
        'cms_imagecache.plugins.*',  # installs all imagecache plugins
    )  

OR  pick and choose::

    INSTALLED_APPS = (...,
        'cms_imagecache.plugins.picture',  # use this instead of 'cms.plugins.picture'
        'cms_imagecache.plugins.image',
    )
                 
Don't forget to syncdb.

Templates
---------
Recommended to use the app_directories template loader::

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        ...
    )

If you aren't using the app_directories template loader, you will need to add the
templates to your TEMPLATE_DIRS settings.  The templates are at::

   cms_imagecache/plugins/<plugin-name>/templates

and can be overridden by adding a "cms_imagecache" folder to your project templates directory.
    

Settings
========

No settings specific for imagecache - see sorl-thumbnail

Presets
=======
A preset defines a set of image processing operations, which might include scaling,
cropping, etc.  The available operations are defined by sorl-thumbnail (see `thumbnail documentation <http://thumbnail.sorl.net/index.html>`_).
A preset is composed of two fields:

* geometry: a sorl-thumbnail geometry string - defines how the image will be scaled (see `thumbnail Geometry <http://thumbnail.sorl.net/template.html#geometry>`_)
* options: a dictionary of sorl-thumbnail image processing options (see `thumbnail Options <http://thumbnail.sorl.net/template.html#options>`_)

These definitions are passed directly through to sorl-thumbnail without interpretation. 
In turn, sorl-thumbnail passes the options directly through to the backend image library engine,
which provides enormous flexibility and extensibility.


Template Tags
=============
Use either sorl-thumbnail's template tag, and pass the preset fields through::

   {% load thumbnail %}
   {% thumbnail source preset.geometry options=preset.options as var %}

OR, equivalently,  use the imagecache template tag, which simplifies the syntax::

   {% load imagecache %}
   {% imagecache source preset as var %}
   
Both the thumbnail and imagecache tags have an optional {% empty %}
tag, which renders if the source resolves to an empty value.  

Margin Filter
-------------
There is also an ic_margin filter which exposes the `sorl-thumbnail margin filter <http://thumbnail.sorl.net/template.html#margin>`_.
It simply takes a preset object or preset name as a parameter and delegates to the sorl-thumbnail margin filter using the preset geometry::

   {% load imagecache %}
   {% imagecache profile.photo profile.preset as im %}
        <img src="{{ im.url }}" style="margin:{{ im|ic_margin:profile.preset }}">
   {% endimagecache %}
   
The two tag libraries don't conflict, so mix and match as you like.


Kudos
=====

* inspired by the fabulous imagecache module in Drupal  http://drupal.org/project/imagecache
* built upon the solid and flexible sorl-thumbnail app https://github.com/sorl/sorl-thumbnail
* incorporates the nifty django-picklefield  https://github.com/shrubberysoft/django-picklefield
