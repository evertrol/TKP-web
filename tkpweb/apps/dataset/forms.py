from django import forms


class MonitoringListForm(forms.Form):
    ra = forms.FloatField()
    dec = forms.FloatField()
