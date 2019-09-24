from django import forms

MODALITY_CHOICES = [
    ('US', 'US'),
    ('CR', 'CR'),
    ('NM', 'NM'),
    ('MG', 'MG'),

]


class TechNoteForm(forms.Form):
    tech_initials = forms.CharField(label='Tech Initials', max_length=5)
    modality = forms.ChoiceField(label='Modality', choices=MODALITY_CHOICES)
    procedure = forms.CharField(label='Procedure', max_length=40)
    patient_id = forms.CharField(label='Patient ID', max_length=20)
    accession = forms.CharField(label='Accession#', max_length=20)
    patient_name = forms.CharField(label='Patient Name', max_length=100)
    exam_date = forms.DateField(label='Exam Date')
    comments = forms.CharField(
        label='Comments', max_length=500, widget=forms.Textarea)


class QueryWorklistForm(forms.Form):
    accession = forms.CharField(label='Accession#', max_length=20)
