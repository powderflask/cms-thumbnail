from django.contrib import admin
from models import Preset
from forms import PresetForm

"""
   @todo - improve usability by adding custom form with fields, help, validation 
           for specifying geometry and options.
"""
class PresetAdmin(admin.ModelAdmin):
    form = PresetForm
    list_display = ('name','geometry')
    list_editable = ('geometry',)
admin.site.register(Preset, PresetAdmin)
