from django import forms
from .models import AudioFile

class AudioFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['title', 'audio']
        
class CSVUploadForm(forms.Form):
    file = forms.FileField()