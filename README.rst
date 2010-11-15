==============================
Django CMS ImageCache
==============================

CMS ImageCache exposes sorl-thumbnail's image processing and caching functionality within `Django CMS <http://www.django-cms.org/>`_.

The module is inspired by `Drupal's imagecache module <http://drupal.org/project/imagecache>`_.

Currently in development - DO NOT USE for production sites!

 
Features
========

* Named "presets" define image processing rules (image geometry and options) - can be configured in settings or dynamically in DB.
* Content editors can choose which preset to display image with (or even define their own presets)
* Two plugins:
1. Picture - extends the django-cms Picture plugin to add an imagecache preset.
2. Image - works with any model that defines an ImageField - adds an imagecache preset.
* Can use each plugin independently
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

    INSTALLED_APPS = (...,  # don't need base module if presets defined in settings and not using imagecache templatetag
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

No settings are required, however, you may configure presets in settings::

    CMS_IMAGECACHE_PRESETS = {
        'preset name': {
                'geometry': '100x100',
                'options': {'crop':'top 50%'}
        },
        ...
    }


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

Defining Presets
----------------
Presets can be defined in 2 ways:

1. in the project settings.py (see Settings, above).
   This option allows a developer to define the presets used for a site, without having to add any fixtures to the DB.
   Presets defined in settings are NOT editable by the end-user.
   There is no need to include the base module in INSTALLED_APPS if all presets are defined in settings
   and you use the thumbnail rather than the imagecache template tag (see below).
2. via the Presets model.
   This option allows creating and editing of presets through the django Admin.
   Users with the right permission can edit presets.
   To use this option, you MUST include the base module in your INSTALLED_APPS


Template Tags
=============
Use either sorl-thumbnail's template tag, and pass the preset fields through::

   {% load thumbnail %}
   {% thumbnail source preset.geometry options=preset.options as var %}

OR use the imagecache template tag, which has a simplified syntax::

   {% load imagecache %}
   {% imagecache source preset as var %}
   
Both the thumbnail and imagecache tags have an optional {% empty %}
tag, which renders if the source resolves to an empty value.


Kudos
=====

* inspired by the fabulous imagecache module in Drupal  http://drupal.org/project/imagecache
* built upon the solid and flexible sorl-thumbnail app https://github.com/sorl/sorl-thumbnail
* incorporates the nifty django-picklefield  https://github.com/shrubberysoft/django-picklefield
