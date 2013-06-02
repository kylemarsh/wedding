from django import forms

from apps.rsvp.models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        fields = ['response', 'party', 'email', 'phone',
                  'address', 'city', 'state', 'zipcode', ]
        model = Group
