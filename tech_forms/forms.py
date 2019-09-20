from django.forms import ModelForm, ModelChoiceField
from .models import TechNote, Modality


class TechNoteForm(ModelForm):
    modality = ModelChoiceField(queryset=Modality.objects.all(), initial=0)

    class Meta:
        model = TechNote
        fields = ['patient_name', 'exam_date', 'tech_initials',
                  'patient_age', 'accession', 'comments']
