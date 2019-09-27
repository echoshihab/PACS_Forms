from django import forms


class ServerConfigForm(forms.Form):
    workstation_ae = forms.CharField(
        label='Workstation AE', max_length=20)
    worklist_ae = forms.CharField(label='Worklist AE', max_length=20)
    worklist_ip = forms.GenericIPAddressField(label='Worklist IP')
    worklist_port = forms.IntegerField(label="Worklist Port")
    destination_ae = forms.CharField(
        label='Storage Destination AE', max_length=20)
    destination_ip = forms.GenericIPAddressField(
        label='Storage Destination IP')
    destination_port = forms.IntegerField(
        label="Storage Destination Port")
