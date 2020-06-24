from django import forms
from .models import Assignments

class AssignmentDocumentForm(forms.ModelForm):
    class Meta:
        model=Assignments
        fields=('level','types','country','description','document','deadline','more_info')

class AssignmentEditForm(forms.ModelForm):
    class Meta:
        model=Assignments
        fields=('level','types','country','description','document','deadline')