from django import forms
from sorl.thumbnail.parsers import ThumbnailParseError, parse_geometry, parse_crop
from models import Preset, deserialize_options

class PresetForm(forms.ModelForm):
    options = forms.CharField(widget=forms.Textarea, required=False, max_length=100, help_text="thumbnail options:  key1=value1 key2=value2...  E.g,. crop='center top'")

    class Meta:
        model = Preset

    def __init__(self, *args, **kwargs):
        super(PresetForm, self).__init__(*args, **kwargs)
 
        # Set the form fields based on the model object
        if kwargs.has_key('instance'):
            instance = kwargs['instance']
            self.initial['options'] = instance.serialize_options()
        
    def clean_geometry(self):
        data = self.cleaned_data['geometry']
        try:
            parse_geometry(data)
        except ThumbnailParseError, e:
            raise forms.ValidationError(str(e))
        
        return data

    def clean_options(self):
        data = self.cleaned_data['options']
        try:
            data = deserialize_options(data)
        except ThumbnailParseError, e:
            raise forms.ValidationError(str(e))
        
        return data

    def save(self, commit=True):
        model = super(PresetForm, self).save(commit=False)
 
        # Save the latitude and longitude based on the form fields
        model.options = self.cleaned_data['options']
 
        if commit:
            model.save()
 
        return model
        