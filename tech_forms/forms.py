from django import forms

MODALITY_CHOICES = [
    ('US', 'US'),
    ('CR', 'CR'),
    ('NM', 'NM'),
    ('MG', 'MG'),

]


class TechNoteForm(forms.Form):
    tech_initials = forms.CharField(label='Tech Initials', max_length=5)
    modality = forms.ChoiceField(choices=MODALITY_CHOICES)
    patient_name = forms.CharField(label='Patient Name', max_length=100)
    exam_date = forms.DateField()
    accession = forms.CharField(label='Accession#', max_length=20)
    comments = forms.CharField(
        label='Comments', max_length=500, widget=forms.Textarea)
